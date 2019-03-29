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


class InstanceGroupsAction(object):

    def __init__(self, conn):
        self.conn = conn

    def create_instance_groups(self, relation,
                               instance_group_name=None,
                               description=None,
                               **ignore):
        """ Create an instance group.
        @param relation: Define the relation between instances in the same group.
                        "repel" means these instances prefer distributing on the different physical units.
                        "attract" means these instances prefer converging on the same physical unit.
        @param instance_group_name: The name of this group.
        @param description: The description of this group.
        """
        action = const.ACTION_CREATE_INSTANCE_GROUPS
        valid_keys = ['relation', 'instance_group_name', 'description']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=['relation'],
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def delete_instance_groups(self, instance_groups,
                               **ignore):
        """ Delete the specific instance group.
        @param instance_groups: An id list contains the group(s) id which will be deleted.
        """
        action = const.ACTION_DELETE_INSTANCE_GROUPS
        valid_keys = ['instance_groups']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=['instance_groups'],
                                                  list_params=['instance_groups']
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def join_instance_group(self, instances,
                            instance_group,
                            **ignore):
        """ Add the instance(s) to the instance group.
        @param instances: An id list contains the instances(s) that will be added in the specific group.
        @param instance_group: The group id.
        """
        action = const.ACTION_JOIN_INSTANCE_GROUP
        valid_keys = ['instances', 'instance_group']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=['instances', 'instance_group'],
                                                  list_params=['instances']
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def leave_instance_group(self, instances,
                             instance_group,
                             **ignore):
        """ Delete the specific instance(s) from the group.
        @param instances: An id list contains the instance(s) who want to leave the instance group.
        @param instance_group: The instance group id.
        """
        action = const.ACTION_LEAVE_INSTANCE_GROUP
        valid_keys = ['instances', 'instance_group']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=['instances', 'instance_group'],
                                                  list_params=['instances']
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def describe_instance_groups(self, instance_groups=[],
                                 relation=None,
                                 tags=None,
                                 owner=None,
                                 verbose=0,
                                 offset=0,
                                 limit=20,
                                 **ignore):
        """ Describe the instance groups filtered by conditions.
        @param instance_groups: If this param was given, only return the group(s) info in this given list.
        @param relation: Filter by the relation type.
        @param tags: Filter by the tag id.
        @param owner: Filter by the owner id.
        @param verbose: Whether return the verbose information.
        @param offset: The offset of the item cursor and its default value is 0.
        @param limit: The number of items that will be displayed. Default is 20, maximum is 100.
        """
        action = const.ACTION_DESCRIBE_INSTANCE_GROUPS
        valid_keys = ['instance_groups', 'relation', 'tags', 'owner',
                      'verbose', 'offset', 'limit']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  list_params=['instance_groups', 'tags'],
                                                  integer_params=['limit', 'verbose', 'offset']
                                                  ):
            return None

        return self.conn.send_request(action, body)
