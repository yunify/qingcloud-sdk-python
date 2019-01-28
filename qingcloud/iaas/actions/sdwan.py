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
        '''
        action = const.ACTION_DESCRIBE_WAN_ACCESS
        valid_keys = ['wan_accesss', 'wan_access_name', 'wan_nets',
                      'wan_pops', 'status', 'access_type', 'location_nation',
                      'location_province', 'location_city', 'owner',
                      'search_word', 'offset', 'limit']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(
                body,
                integer_params=["offset", "limit"],
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
                                'bandwidth_remote']
              ):
            return None

        return self.conn.send_request(action, body)
