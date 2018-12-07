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


class EipAction(object):

    def __init__(self, conn):
        self.conn = conn

    def describe_eips(self, eips=None,
                      status=None,
                      instance_id=None,
                      search_word=None,
                      owner=None,
                      offset=None,
                      limit=None,
                      tags=None,
                      **ignore):
        """ Describe eips filtered by condition.
        @param eips: IDs of the eip you want describe.
        @param status: filter eips by status
        @param instance_id: filter eips by instance.
        @param search_word: search word column.
        @param offset: the starting offset of the returning results.
        @param limit: specify the number of the returning results.
        @param tags : the array of IDs of tags.
        """
        action = const.ACTION_DESCRIBE_EIPS
        valid_keys = ['eips', 'status', 'instance_id', 'search_word',
                      'offset', 'limit', 'tags', 'owner']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=[],
                                                  integer_params=[
                                                      'offset', 'limit'],
                                                  list_params=[
                                                      'status', 'eips', 'tags']
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def associate_eip(self, eip,
                      instance,
                      **ignore):
        """ Associate an eip on an instance.
        @param eip: The id of eip you want to associate with instance.
        @param instance: the id of instance you want to associate eip.
        """
        action = const.ACTION_ASSOCIATE_EIP
        body = {'eip': eip, 'instance': instance}
        if not self.conn.req_checker.check_params(body,
                                                  required_params=[
                                                      'eip', 'instance'],
                                                  integer_params=[],
                                                  list_params=[]
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def dissociate_eips(self, eips,
                        **ignore):
        """ Dissociate one or more eips.
        @param eips: The ids of eips you want to dissociate with instance.
        """
        action = const.ACTION_DISSOCIATE_EIPS
        body = {'eips': eips}
        if not self.conn.req_checker.check_params(body,
                                                  required_params=['eips'],
                                                  integer_params=[],
                                                  list_params=['eips']
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def allocate_eips(self, bandwidth,
                      billing_mode=const.EIP_BILLING_MODE_BANDWIDTH,
                      count=1,
                      need_icp=0,
                      eip_name='',
                      target_user=None,
                      associate_mode=0,
                      **ignore):
        """ Allocate one or more eips.
        @param count: the number of eips you want to allocate.
        @param bandwidth: the bandwidth of the eip in Mbps.
        @param need_icp: 0 - no need, 1 - need
        @param eip_name : the short name of eip
        @param target_user: ID of user who will own this resource, should be one of your sub-accounts
        @param associate_mode: 0 - associate ip addr to virtual gateway, 1 - associate ip addr to vm
        """
        action = const.ACTION_ALLOCATE_EIPS
        valid_keys = ['bandwidth', 'billing_mode',
                      'count', 'need_icp', 'eip_name',
                      'target_user', 'associate_mode']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=['bandwidth'],
                                                  integer_params=['bandwidth', 'count',
                                                                  'need_icp', 'associate_mode'],
                                                  list_params=[]
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def release_eips(self, eips,
                     force=0,
                     **ignore):
        """ Release one or more eips.
        @param eips : The ids of eips that you want to release
        @param force : Whether to force release the eip that needs icp codes.
        """
        action = const.ACTION_RELEASE_EIPS
        body = {'eips': eips, 'force': int(force != 0)}
        if not self.conn.req_checker.check_params(body,
                                                  required_params=['eips'],
                                                  integer_params=['force'],
                                                  list_params=['eips']
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def change_eips_bandwidth(self, eips,
                              bandwidth,
                              **ignore):
        """ Change one or more eips bandwidth.
        @param eips: The IDs of the eips whose bandwidth you want to change.
        @param bandwidth: the new bandwidth of the eip in MB.
        """
        action = const.ACTION_CHANGE_EIPS_BANDWIDTH
        body = {'eips': eips, 'bandwidth': bandwidth}
        if not self.conn.req_checker.check_params(body,
                                                  required_params=[
                                                      'eips', 'bandwidth'],
                                                  integer_params=['bandwidth'],
                                                  list_params=['eips']
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def change_eips_billing_mode(self, eips,
                                 billing_mode,
                                 **ignore):
        """ Change one or more eips billing mode.
        @param eips: The IDs of the eips whose billing mode you want to change.
        @param billing_mode: the new billing mode, "bandwidth" or "traffic".
        """
        action = const.ACTION_CHANGE_EIPS_BILLING_MODE
        body = {'eips': eips, 'billing_mode': billing_mode}
        if not self.conn.req_checker.check_params(body,
                                                  required_params=[
                                                      'eips', 'billing_mode'],
                                                  list_params=['eips']
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def modify_eip_attributes(self, eip,
                              eip_name=None,
                              description=None,
                              **ignore):
        """ Modify eip attributes.
        If you want to modify eip's bandwidth, use `change_eips_bandwidth`.
        @param eip : the ID of eip that you want to modify
        @param eip_name : the name of eip
        @param description : the eip description
        """
        action = const.ACTION_MODIFY_EIP_ATTRIBUTES
        valid_keys = ['eip', 'eip_name', 'description']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=['eip'],
                                                  integer_params=[],
                                                  list_params=[]
                                                  ):
            return None

        return self.conn.send_request(action, body)
