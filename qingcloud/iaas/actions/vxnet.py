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


class VxnetAction(object):

    def __init__(self, conn):
        self.conn = conn

    def describe_vxnets(self, vxnets=None,
                        search_word=None,
                        verbose=0,
                        owner=None,
                        limit=None,
                        offset=None,
                        tags=None,
                        vxnet_type=None,
                        mode=None,
                        **ignore):
        """ Describe vxnets filtered by condition.
        @param vxnets: the IDs of vxnets you want to describe.
        @param verbose: the number to specify the verbose level, larger the number, the more detailed information will be returned.
        @param offset: the starting offset of the returning results.
        @param limit: specify the number of the returning results.
        @param tags : the array of IDs of tags.
        @param vxnet_type: the vxnet of type you want to describe.
        @param mode: the vxnet mode. 0: gre+ovs, 1: vxlan+bridge.
        """
        action = const.ACTION_DESCRIBE_VXNETS
        valid_keys = ['vxnets', 'search_word', 'verbose', 'limit', 'offset',
                      'tags', 'vxnet_type', 'owner', 'mode']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=[],
                                                  integer_params=[
                                                      'limit', 'offset', 'verbose',
                                                      'vxnet_type', 'mode',
                                                  ],
                                                  list_params=['vxnets', 'tags']
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def create_vxnets(self, vxnet_name=None,
                      vxnet_type=const.VXNET_TYPE_MANAGED,
                      count=1,
                      mode=0,
                      **ignore):
        """ Create one or more vxnets.
        @param vxnet_name: the name of vxnet you want to create.
        @param vxnet_type: vxnet type: unmanaged or managed.
        @param count : the number of vxnet you want to create.
        @param mode: the vxnet mode. 0: gre+ovs, 1: vxlan+bridge.
        """
        action = const.ACTION_CREATE_VXNETS
        valid_keys = ['vxnet_name', 'vxnet_type', 'count', 'mode']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=['vxnet_type'],
                                                  integer_params=[
                                                      'vxnet_type', 'count', 'mode',
                                                  ],
                                                  list_params=[]
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def join_vxnet(self, vxnet,
                   instances,
                   **ignore):
        """ One or more instances join the vxnet.
        @param vxnet : the id of vxnet you want the instances to join.
        @param instances : the IDs of instances that will join vxnet.
        """

        action = const.ACTION_JOIN_VXNET
        valid_keys = ['vxnet', 'instances']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=[
                                                      'vxnet', 'instances'],
                                                  integer_params=[],
                                                  list_params=['instances']
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def leave_vxnet(self, vxnet,
                    instances,
                    **ignore):
        """ One or more instances leave the vxnet.
        @param vxnet : The id of vxnet that the instances will leave.
        @param instances : the IDs of instances that will leave vxnet.
        """
        action = const.ACTION_LEAVE_VXNET
        valid_keys = ['vxnet', 'instances']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=[
                                                      'vxnet', 'instances'],
                                                  integer_params=[],
                                                  list_params=['instances']
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def delete_vxnets(self, vxnets,
                      **ignore):
        """ Delete one or more vxnets.
        @param vxnets: the IDs of vxnets you want to delete.
        """
        action = const.ACTION_DELETE_VXNETS
        body = {'vxnets': vxnets}
        if not self.conn.req_checker.check_params(body,
                                                  required_params=['vxnets'],
                                                  integer_params=[],
                                                  list_params=['vxnets']
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def modify_vxnet_attributes(self, vxnet,
                                vxnet_name=None,
                                description=None,
                                **ignore):
        """ Modify vxnet attributes
        @param vxnet: the ID of vxnet you want to modify its attributes.
        @param vxnet_name: the new name of vxnet.
        @param description: The detailed description of the resource.
        """
        action = const.ACTION_MODIFY_VXNET_ATTRIBUTES
        valid_keys = ['vxnet', 'vxnet_name', 'description']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=['vxnet'],
                                                  integer_params=[],
                                                  list_params=[]
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def describe_vxnet_instances(self, vxnet,
                                 instances=None,
                                 image=None,
                                 instance_type=None,
                                 status=None,
                                 limit=None,
                                 offset=None,
                                 **ignore):
        """ Describe instances in vxnet.
        @param vxnet: the ID of vxnet whose instances you want to describe.
        @param image: filter by image ID.
        @param instances: filter by instance ID.
        @param instance_type: filter by instance type
        See: https://docs.qingcloud.com/api/common/includes/instance_type.html
        @param status: filter by status
        @param offset: the starting offset of the returning results.
        @param limit: specify the number of the returning results.
        """
        action = const.ACTION_DESCRIBE_VXNET_INSTANCES
        valid_keys = ['vxnet', 'instances', 'image', 'instance_type', 'status',
                      'limit', 'offset']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=['vxnet'],
                                                  integer_params=[
                                                      'limit', 'offset'],
                                                  list_params=['instances']
                                                  ):
            return None

        return self.conn.send_request(action, body)
