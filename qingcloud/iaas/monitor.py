# =========================================================================
# Copyright 2012-present Yunify, Inc.
# -------------------------------------------------------------------------
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this work except in compliance with the License.
# You may obtain a copy of the License in the LICENSE file, or at:
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =========================================================================

from copy import deepcopy
from qingcloud.misc.utils import local_ts

NA = 'NA'
STEPS = {
    '5m': 300,
    '15m': 900,
    '30m': 1800,
    '1h': 3600,
    '2h': 7200,
    '1d': 24 * 3600,
}


class MonitorProcessor(object):
    """ Process monitoring data.
    """

    def __init__(self, raw_meter_set, start_time, end_time, step):
        self.raw_meter_set = raw_meter_set
        self.start_time = local_ts(start_time)
        self.end_time = local_ts(end_time)
        self.step = STEPS.get(step)

    def _is_invalid(self, value):
        if isinstance(value, list):
            return any(v == NA for v in value)
        else:
            return value == NA

    def _get_empty_item(self, sample_item):
        """ Return empty item which is used as supplemental data.
        """
        if isinstance(sample_item, list):
            return [None] * len(sample_item)
        else:
            return None

    def _fill_vacancies(self, value, from_ts, to_ts):
        ret = []
        t = from_ts
        while t < to_ts:
            ret.append([t, value])
            t += self.step
        return ret

    def _decompress_meter_data(self, data):
        """ Decompress meter data like:
            [
                [1391854500, 3],  # first item with timestamp
                4,                # normal value
                [200, 3],         # [timestamp_offset, value]
                NA,               # Not Avaliable
                ....
            ]
        """
        if not data or not self.step or not self.start_time:
            return data

        empty_item = self._get_empty_item(data[0][1])
        first_time = data[0][0]
        decompress_data = self._fill_vacancies(
            empty_item, self.start_time, first_time)

        decompress_data.append(data[0])
        t = first_time + self.step
        for item in data[1:]:
            if self._is_invalid(item):
                item = empty_item

            # sometimes item like [timestamp_offset, value]
            elif isinstance(item, list) and len(item) > 1:
                if not isinstance(empty_item, list) or isinstance(item[1], list):
                    t -= self.step
                    decompress_data += self._fill_vacancies(
                        empty_item, t + self.step, t + item[0])
                    t += item[0]
                    item = item[1]

            decompress_data.append([t, item])
            t += self.step

        return decompress_data

    def decompress_monitoring_data(self):
        """ Decompress instance/eip/volume monitoring data.
        """
        meter_set = deepcopy(self.raw_meter_set)
        for meter in meter_set:
            data = meter['data']
            if not data:
                continue
            meter['data'] = self._decompress_meter_data(data)
        return meter_set

    def decompress_lb_monitoring_data(self):
        """ Decompress load balancer related monitoring data.
        """
        meter_set = deepcopy(self.raw_meter_set)
        for meter in meter_set:
            for data_item in meter['data_set']:
                data = data_item['data']
                if not data:
                    continue
                data_item['data'] = self._decompress_meter_data(data)
        return meter_set
