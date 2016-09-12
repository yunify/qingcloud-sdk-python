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

import unittest
from qingcloud.iaas.monitor import MonitorProcessor, NA


class MonitorProcessorTestCase(unittest.TestCase):

    def _get_processor(self, meter_set=None, start_time=None, end_time=None, step=None):
        start_time = start_time or '2014-02-08T12:00:00Z'
        end_time = end_time or '2014-02-08T13:00:00Z'
        step = step or '15m'
        return MonitorProcessor(meter_set, start_time, end_time, step)

    def test_init_processor(self):
        p = self._get_processor()
        self.assertTrue(p.start_time)
        self.assertTrue(p.end_time)
        self.assertTrue(p.step)

    def test_init_processor_with_invalid_step(self):
        p = self._get_processor(step='1m')
        self.assertFalse(p.step)

    def test_init_processor_with_invalid_time_format(self):
        p = self._get_processor(start_time='2011-10-16 10:58:00')
        self.assertFalse(p.start_time)

    def test_is_invalid(self):
        p = self._get_processor()
        self.assertTrue(p._is_invalid(NA))
        self.assertTrue(p._is_invalid([1, 2, NA]))
        self.assertFalse(p._is_invalid(1))
        self.assertFalse(p._is_invalid(range(4)))

    def test_get_empty_item(self):
        p = self._get_processor()
        sample_item = 2
        expected = None
        self.assertEquals(p._get_empty_item(sample_item), expected)

        sample_item = [7, 11]
        expected = [None, None]
        self.assertEquals(p._get_empty_item(sample_item), expected)

    def test_fill_vacancies(self):
        p = self._get_processor(step='5m')
        value = 7
        from_ts, to_ts = 1000, 2000
        expected = [[1000, 7], [1300, 7], [1600, 7], [1900, 7]]
        self.assertEquals(p._fill_vacancies(value, from_ts, to_ts), expected)

    def test_decompress_meter_data(self):
        p = self._get_processor()
        data = []
        self.assertEquals(p._decompress_meter_data(data), [])

        first_time = p.start_time + 1000
        data = [
            [first_time, 3],
            4,
            NA,
            5,
            [1000, 3],
            10,
            [100, 3],
        ]
        expected = [
            [p.start_time, None],
            [p.start_time + p.step, None],
            [first_time, 3],
            [first_time + p.step * 1, 4],
            [first_time + p.step * 2, None],
            [first_time + p.step * 3, 5],
            [first_time + p.step * 4, None],
            [first_time + p.step * 3 + 1000, 3],
            [first_time + p.step * 4 + 1000, 10],
            [first_time + p.step * 4 + 1000 + 100, 3],
        ]
        self.assertEquals(p._decompress_meter_data(data), expected)

    def test_decompress_lb_monitoring_data(self):
        start_time = '2014-02-09T11:22:49.888Z'
        end_time = '2014-02-09T17:22:49.888Z'
        step = '5m'
        meter_set = [{
            "data_set": [{"eip_id": "eip-kqpkxm8f", "data": [[1391945100, [23, 29]],
                                                             [17, 30], [19, 29], [20, 31], [22, 29], [
                                                                 20, 29], [23, 30], [19, 27],
                                                             [23, 30], [16, 29], [30, 33], [15, 29], [
                19, 30], [23, 30], [27, 29],
                [29, 29], [23, 29], [25, 31], [34, 30], [
                29, 29], [25, 33], [16, 29],
                [17, 31], [17, 31], [16, 29], [25, 28], [
                17, 31], [21, 33], [16, 29],
                [18, 30], [18, 31], [43, 28], [43, 29], [
                24, 29], [17, 31], [15, 29],
                [19, 30], [19, 29], [21, 28], [19, 31], [
                15, 29], [15, 29], [20, 29],
                [20, 29], [19, 31], [18, 31], [18, 29], [
                18, 29], [26, 31], [23, 29],
                [52, 29], [21, 29], [17, 30], [16, 29], [
                23, 30], [22, 31], [17, 29],
                [25, 29], [16, 29], [17, 31], [16, 29], [
                24, 31], [20, 29], [23, 31],
                [16, 29], [17, 30], [16, 29], [19, 31], [
                17, 31], [17, 29], [18, 29],
                [17, 30]]}],
            "meter_id":"traffic"
        }]
        p = self._get_processor(meter_set, start_time, end_time, step)
        meter_set = p.decompress_lb_monitoring_data()
        for meter in meter_set:
            for item in meter['data_set'][0]['data']:
                self.assertTrue(isinstance(item, list))
                self.assertEquals(len(item), 2)

    def test_decompress_monitoring_data(self):
        start_time = '2014-02-09T12:01:49.032Z'
        end_time = '2014-02-09T18:01:49.032Z'
        step = '5m'
        meter_set = [
            {"data": [[1391947500, [12, 12]], [14, 13], [16, 13], [20, 12], [13, 13],
                      [12, 12], [12, 12], [13, 13], [13, 13], [
                          12, 12], [12, 12], [16, 13],
                      [14, 13], [13, 13], [15, 13], [15, 13], [
                12, 12], [13, 13], [12, 12],
                [13, 13], [12, 12], [13, 13], [14, 12], [
                14, 12], [14, 13], [18, 12],
                [15, 12], [32, 13], [12, 12], [13, 13], [
                15, 12], [13, 13], [12, 12],
                [12, 12], [12, 12], [14, 13], [12, 12], [
                19, 13], [40, 12], [39, 12],
                [13, 12], [13, 13], [13, 13], [17, 13], [
                12, 12], [12, 12], [13, 13],
                [14, 13], [12, 12], [15, 12], [12, 12], [
                12, 12], [12, 12], [12, 12],
                [14, 12], [3000, [11, 10]], [16, 12], [
                15, 13], [12, 12], [18, 15],
                [15, 12], [12, 12], [13, 13]], "vxnet_id":"vxnet-0",
             "meter_id":"if-52:54:b3:0c:30:89", "sequence":0
             },
            {"data": [[1391947500, [0, 2799]], [0, 2441], [0, 2473], [0, 2320],
                      [0, 2475], [0, 2216], [0, 2405], [
                0, 2372], [0, 2490], [0, 2387],
                [0, 2492], [0, 2315], [0, 2834], [
                0, 2523], [0, 2287], [0, 2573],
                [0, 2336], [0, 2439], [0, 2232], [
                0, 2422], [0, 2184], [0, 2457],
                [0, 2507], [0, 2368], [0, 2606], [
                0, 2459], [0, 2424], [0, 2456],
                [0, 2286], [0, 2575], [0, 2338], [
                0, 2490], [0, 2524], [0, 2200],
                [0, 2406], [0, 2540], [0, 2406], [
                0, 2304], [0, 2424], [0, 2216],
                [0, 2403], [0, 2404], [0, 2525], [
                0, 2525], [0, 2303], [0, 2473],
                [0, 2422], [0, 2341], [0, 2781], [
                0, 2406], [0, 2252], [0, 2320],
                [0, 2457], [0, 2202], [0, 2543], [
                3000, [921302, 11145]], [0, 2717],
                [0, 2943], [0, 2519], [0, 2911], [0, 2673], [0, 2648], [0, 2671]],
             "meter_id":"disk-os"
             },
            {"data": [[1391947500, 3], 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
                      3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
                      3, 3, 3, 3, 3, 3, [3000, 532], 3, 3, 3, 3, 3, 3, 3], "meter_id":"cpu"
             },
            {"data": [[1391947500, 93], 93, 93, 93, 93, 93, 93, 93, 93, 93, 93, 93, 93,
                      93, 93, 93, 93, 93, 93, 93, 93, 93, 93, 93, 93, 93, 93, 93, 93, 93, 93, 93,
                      93, 93, 93, 93, 93, 93, 93, 93, 93, 93, 93, 93, 93, 93, 93, 93, 93, 93, 93,
                      93, 93, 93, 93, [3000, 57], 56, 56, 56, 56, 56, 56, 56], "meter_id":"memory"
             }
        ]
        p = self._get_processor(meter_set, start_time, end_time, step)
        meter_set = p.decompress_monitoring_data()
        for meter in meter_set:
            for item in meter['data']:
                self.assertTrue(isinstance(item, list))
                self.assertEquals(len(item), 2)
