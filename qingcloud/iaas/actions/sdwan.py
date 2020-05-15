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

    def describe_wan_accesss(self,
                             wan_accesss=None,
                             wan_access_name=None,
                             wan_nets=None,
                             wan_pops=None,
                             status=None,
                             access_type=None,
                             location_nation=None,
                             location_province=None,
                             location_city=None,
                             owner=None,
                             search_word=None,
                             offset=None,
                             limit=None,
                             verbose=0,
                             **params):
        ''' Action: DescribeWanAccesss
            @param wan_accesss: IDs of the wan accesss you want describe.
            @param wan_access_name: the name of the wan access.
            @param wan_nets: ID of wan net which wan accesss belong to
            @param wan_pops: ID of wan pop which wan accesss belong to
            @param status: status of wan access
            @param access_type: access type eg: line,vpc,cpe.
            @param location_nation: The nation of access location.
            @param location_province: The province of access location.
            @param location_city: The city of access location.
            @param owner: the owner IDs of resource.
            @param search_word: the search_word of resource
            @param offset: the starting offset of the returning results.
            @param limit: specify the number of the returning results.
            @param verbose: the number to specify the verbose level. eg: 0/1
        '''
        action = const.ACTION_DESCRIBE_WAN_ACCESS
        valid_keys = ['wan_accesss', 'wan_access_name', 'wan_nets',
                      'wan_pops', 'status', 'access_type', 'location_nation',
                      'location_province', 'location_city', 'owner',
                      'search_word', 'offset', 'limit', 'verbose']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(
                body,
                integer_params=["offset", "limit", "verbose"],
                list_params=["wan_accesss",
                             "wan_nets",
                             "wan_pops",
                             "access_type", "status"]):
            return None

        return self.conn.send_request(action, body)

    def change_wan_access_bandwidth(self,
                                    wan_access,
                                    bandwidth_type,
                                    bandwidth=None,
                                    **params):
        """ change wan accesss bandwidth.
        @param wan_access: the IDs of wan access.
        @param bandwidth_type: wan access bandwitdth type eg: elastic.
        @param bandwidth: the new bandwidth for all, unit in Mbps.
        """
        action = const.ACTION_CHANGE_WAN_ACCESS_BANDWIDTH
        valid_keys = ['wan_access', 'bandwidth_type', 'bandwidth']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(
                body,
                required_params=['wan_access',
                                 'bandwidth_type'],
                integer_params=['bandwidth']
        ):
            return None

        return self.conn.send_request(action, body)

    def upgrade_wan_access(self,
                           wan_accesss,
                           bandwidth=None,
                           **params):
        """ upgrade_wan_access.
        @param wan_access: the IDs of wan access.
        @param bandwidth: the new bandwidth for all, unit in Mbps.
        unit in Mbps.
        """
        action = const.ACTION_UPGRADE_WAN_ACCESS
        valid_keys = ['wan_accesss', 'bandwidth']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(
                body,
                required_params=['wan_accesss'],
                integer_params=['bandwidth'],
        ):
            return None

        return self.conn.send_request(action, body)

    def get_wan_monitor(self,
                        resource=None,
                        access_type=None,
                        meters=None,
                        step=None,
                        start_time=None,
                        end_time=None,
                        interface_name=None,
                        monitor_type=None,
                        ha_member_index=None,
                        **params):
        """ Action: GetWanMonitor
            @param resource: the ID of resource whose monitoring data
                             you want to get.
            @param access_type: the wan access type. eg: line, vpc, cpe.
            @param meters: a list of metering types you want to get.
                           e.g. "flow", "pps"
            @param step: the metering time step. e.g. "1m", "5m", "15m",
                         "30m", "1h", "2h", "1d"
            @param start_time: the starting time stamp.
            @param end_time: the ending time stamp.
            @param interface_name: interface name, eg: eth0, eth1
            @param monitor_type: CPE's monitor type, eg: internet, pop
            @param ha_member_index: the ha member index. eg: 0/1
        """
        action = const.ACTION_GET_WAN_MONITOR
        valid_keys = ['resource', 'access_type', 'meters', 'step',
                      'start_time', 'end_time', 'interface_name',
                      'monitor_type', 'ha_member_index']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(
                body,
                required_params=["resource", "access_type",
                                 "meters", "step",
                                 "start_time", "end_time"],
                list_params=["meters"],
                datetime_params=["start_time", "end_time"]
        ):
            return None

        return self.conn.send_request(action, body)

    def get_wan_info(self,
                     resources=None,
                     info_type=None,
                     **params):
        """ Action: GetWanInfo
            @param resources: the comma separated IDs of wan resource.
            @param info_type: the info type. eg: cpe_mobile_info.
        """
        action = const.ACTION_GET_WAN_INFO
        valid_keys = ['resources', 'info_type']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(
                body,
                required_params=["resources", "info_type"],
                list_params=["resources"],
        ):
            return None

        return self.conn.send_request(action, body)
