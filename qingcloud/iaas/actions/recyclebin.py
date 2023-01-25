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


class RecycleBinAction(object):

    def __init__(self, conn):
        self.conn = conn

    def describe_recycle_resources(self,
                                   zones=None,
                                   owner=None,
                                   user=None,
                                   status=None,
                                   offset=None,
                                   limit=None,
                                   resource_types=None,
                                   recycle_status=None,
                                   resources=None,
                                   **ignore):
        """
        @param zones: zone to be filtered;
        @param owner: sender user_id;
        @param user: Users who need to filter queries;
        @param status: filter queries by resource status;
        @param resource_types: filter queries by resource resource_types;
        @param recycle_status: filter queries by resource recycle_status;
        @param status: filter queries by resource status;
        @param resources: IDs of the resources;
        @param offset: the starting offset of the returning results;
        @param limit: specify the number of the returning results;
        """
        action = const.ACTION_DESCRIBE_RECYCLE_RESOURCES
        valid_keys = ['zones', 'user', 'owner', 'status', 'resource_types', 'recycle_status',
                      'resources', 'offset', 'limit', 'zone']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  list_params=["status", "resource_types", "zones", "resources"],
                                                  integer_params=["limit", "offset"]):
            return None

        return self.conn.send_request(action, body)

    def cease_recycle_resources(self,
                                resources,
                                owner=None,
                                destroy_mode=0,
                                **ignore):
        """
        @param resources: IDs of the resources;
        @param owner: sender user_id;
        @param destroy_mode: recycle bin resources destroy mode;
        """
        action = const.ACTION_CEASE_RECYCLE_RESOURCES
        valid_keys = ['resources', 'owner', 'destroy_mode', 'zone']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=["resources"],
                                                  list_params=["resources"],
                                                  integer_params=["destroy_mode"]):
            return None
        return self.conn.send_request(action, body)

    def recover_recycle_resources(self,
                                  resources,
                                  owner=None,
                                  **ignore):
        """
        @param resources: IDs of the resources;
        @param owner: sender user_id;
        """
        action = const.ACTION_RECOVER_RECYCLE_RESOURCES
        valid_keys = ['resources', 'owner', 'zone']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=["resources"],
                                                  list_params=["resources"]):
            return None
        return self.conn.send_request(action, body)
