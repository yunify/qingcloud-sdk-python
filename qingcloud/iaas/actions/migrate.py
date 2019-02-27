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


class MigrateAction(object):

    def __init__(self, conn):
        self.conn = conn

    def migrate_resources(self, resources,
                          src_zone,
                          dst_zone,
                          **ignore):
        """ Migrate resources.
        @param resources: the IDs of resources you want to migrate.
        @param src_zone: the zone of the resources.
        @param dst_zone: the destination zone of the resources migrate.
        """
        action = const.ACTION_MIGRATE_RESOURCES
        valid_keys = ['resources', 'src_zone', 'dst_zone']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=["resources", "src_zone", "dst_zone"],
                                                  integer_params=[],
                                                  list_params=[]
                                                  ):
            return None

        return self.conn.send_request(action, body)
