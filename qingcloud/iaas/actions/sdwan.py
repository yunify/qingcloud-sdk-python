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

from qingcloud.iaas import constants as const
from qingcloud.misc.utils import filter_out_none


class SdwanAction(object):

    def __init__(self, conn):
        self.conn = conn

    def change_wan_access_bandwidth(self,
                                    wan_access,
                                    bandwidth_type,
                                    bandwidth=None,
                                    bandwidth_local=None,
                                    bandwidth_remote=None,
                                    **params):
        """ change wan accesss bandwidth.
        @param wan_access: the IDs of wan access.
        @param bandwidth_type: wan access bandwitdth type eg: elastic.
        @param bandwidth: the new bandwidth for all, unit in Mbps.
        @param bandwidth_local: the new bandwidth for local city, unit in Mbps.
        @param bandwidth_remote : the new bandwidth for remote city,
        unit in Mbps.
        """
        action = const.ACTION_CHANGE_WAN_ACCESS_BANDWIDTH
        valid_keys = ['wan_access', 'bandwidth_type', 'bandwidth',
                      'bandwidth_local', 'bandwidth_remote']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(
                body,
                required_params=['wan_access',
                                 'bandwidth_type'],
                integer_params=['bandwidth',
                                'bandwidth_local',
                                'bandwidth_remote'],
                str_params=['wan_access', 'bandwidth_type']
              ):
            return None

        return self.conn.send_request(action, body)
