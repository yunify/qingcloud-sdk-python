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


class KeypairAction(object):

    def __init__(self, conn):
        self.conn = conn

    def describe_key_pairs(self, keypairs=None,
                           encrypt_method=None,
                           search_word=None,
                           owner=None,
                           verbose=0,
                           offset=None,
                           limit=None,
                           tags=None,
                           **ignore):
        """ Describe key-pairs filtered by condition
        @param keypairs: IDs of the keypairs you want to describe.
        @param encrypt_method: encrypt method.
        @param verbose: the number to specify the verbose level, larger the number, the more detailed information will be returned.
        @param offset: the starting offset of the returning results.
        @param limit: specify the number of the returning results.
        @param tags : the array of IDs of tags.
        """
        action = const.ACTION_DESCRIBE_KEY_PAIRS
        valid_keys = ['keypairs', 'encrypt_method', 'search_word', 'verbose',
                      'offset', 'limit', 'tags', 'owner']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=[],
                                                  integer_params=[
                                                      'offset', 'limit', 'verbose'],
                                                  list_params=['keypairs', 'tags']
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def attach_keypairs(self, keypairs,
                        instances,
                        **ignore):
        """ Attach one or more keypairs to instances.
        @param keypairs: IDs of the keypairs you want to attach to instance .
        @param instances: IDs of the instances the keypairs will be attached to.
        """
        action = const.ACTION_ATTACH_KEY_PAIRS
        valid_keys = ['keypairs', 'instances']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=[
                                                      'keypairs', 'instances'],
                                                  integer_params=[],
                                                  list_params=[
                                                      'keypairs', 'instances']
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def detach_keypairs(self, keypairs,
                        instances,
                        **ignore):
        """ Detach one or more keypairs from instances.
        @param keypairs: IDs of the keypairs you want to detach from instance .
        @param instances: IDs of the instances the keypairs will be detached from.
        """
        action = const.ACTION_DETACH_KEY_PAIRS
        valid_keys = ['keypairs', 'instances']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=[
                                                      "keypairs", "instances"],
                                                  integer_params=[],
                                                  list_params=[
                                                      "keypairs", "instances"]
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def create_keypair(self, keypair_name,
                       mode='system',
                       encrypt_method="ssh-rsa",
                       public_key=None,
                       target_user=None,
                       **ignore):
        """ Create a keypair.
        @param keypair_name: the name of the keypair you want to create.
        @param mode: the keypair creation mode, "system" or "user".
        @param encrypt_method: the encrypt method, supported methods "ssh-rsa", "ssh-dss".
        @param public_key: provide your public key. (need "user" mode)
        @param target_user: ID of user who will own this resource, should be one of your sub-accounts
        """
        action = const.ACTION_CREATE_KEY_PAIR
        valid_keys = ['keypair_name', 'mode', 'encrypt_method', 'public_key', 'target_user']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=['keypair_name'],
                                                  integer_params=[],
                                                  list_params=[]
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def delete_keypairs(self, keypairs,
                        **ignore):
        """ Delete one or more keypairs.
        @param keypairs: IDs of the keypairs you want to delete.
        """
        action = const.ACTION_DELETE_KEY_PAIRS
        body = {'keypairs': keypairs}
        if not self.conn.req_checker.check_params(body,
                                                  required_params=['keypairs'],
                                                  integer_params=[],
                                                  list_params=['keypairs']
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def modify_keypair_attributes(self, keypair,
                                  keypair_name=None,
                                  description=None,
                                  **ignore):
        """ Modify keypair attributes.
        @param keypair: the ID of keypair you want to modify its attributes.
        @param keypair_name: the new name of keypair.
        @param description: The detailed description of the resource.
        """
        action = const.ACTION_MODIFY_KEYPAIR_ATTRIBUTES
        valid_keys = ['keypair', 'keypair_name', 'description']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=['keypair'],
                                                  integer_params=[],
                                                  list_params=[]
                                                  ):
            return None

        return self.conn.send_request(action, body)
