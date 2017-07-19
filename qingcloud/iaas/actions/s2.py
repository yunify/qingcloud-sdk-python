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


class S2Action(object):
    def __init__(self, conn):
        self.conn = conn

    def create_s2_server(self,
                         vxnet,
                         service_type,
                         s2_server_name=None,
                         s2_server_type=None,
                         private_ip=None,
                         description=None,
                         s2_class=None,
                         **ignore):
        """ Create S2 server

        :param vxnet: the ID of vxnet.
        :param service_type: valid values is vsan or vnas.
        :param s2_server_name: the name of s2 server.
        :param s2_server_type: valid values includes 0, 1, 2, 3.
        :param private_ip: you may specify the ip address of this server.
        :param description: the detailed description of the resource.
        :param s2_class: valid values includes 0, 1.
        """
        action = const.ACTION_CREATE_S2_SERVER
        valid_keys = [
            'vxnet', 'service_type', 's2_server_name', 's2_server_type',
            'private_ip', 'description', 's2_class',
        ]
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(
                body,
                integer_params=["s2_server_type", "s2_class"],
        ):
            return None

        return self.conn.send_request(action, body)

    def describe_s2_servers(self,
                            s2_servers=None,
                            service_types=None,
                            status=None,
                            search_word=None,
                            tags=None,
                            verbose=None,
                            offset=None,
                            limit=None,
                            **ignore):
        """ Describe S2 servers

        :param s2_servers: the IDs of s2 server you want to describe.
        :param service_types: the type of service, valid value is 'vsan' or 'vnas'.
        :param status: valid values include pending, active, poweroffed, suspended, deleted, ceased.
        :param search_word: you may use this field to search from id, name and description.
        :param tags: the array of IDs of tags.
        :param verbose: the number to specify the verbose level, larger the number, the more detailed information will be returned.
        :param offset: the starting offset of the returning results.
        :param limit: specify the number of the returning results.
        """
        action = const.ACTION_DESCRIBE_S2_SERVERS
        valid_keys = [
            's2_servers', 'service_types', 'status', 'search_word',
            'tags', 'verbose', 'offset', 'limit',
        ]
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(
                body,
                integer_params=["offset", "limit", "verbose"],
                list_params=["s2_servers", "service_types", "tags", "status"],
        ):
            return None

        return self.conn.send_request(action, body)

    def modify_s2_server(self,
                         s2_server,
                         s2_server_name=None,
                         description=None,
                         **ignore):
        """ Modify S2 server

        :param s2_server: the ID of s2 server.
        :param s2_server_name: the new name you want to use.
        :param description: the new value of description.
        """
        action = const.ACTION_MODIFY_S2_SERVER
        valid_keys = [
            's2_server', 's2_server_name', 'description',
        ]
        body = filter_out_none(locals(), valid_keys)

        return self.conn.send_request(action, body)

    def resize_s2_servers(self,
                          s2_servers,
                          s2_server_type,
                          **ignore):
        """ Resize S2 servers

        :param s2_servers: the IDs of s2 servers you want to resize.
        :param s2_server_type: valid values includes 0, 1, 2, 3.
        """
        action = const.ACTION_RESIZE_S2_SERVERS
        valid_keys = [
            's2_servers', 's2_server_type'
        ]
        body = filter_out_none(locals(), valid_keys)

        if not self.conn.req_checker.check_params(
                body,
                integer_params=['s2_server_type'],
                list_params=['s2_servers'],
        ):
            return None

        return self.conn.send_request(action, body)

    def delete_s2_servers(self,
                          s2_servers,
                          **ignore):
        """ Delete S2 servers

        :param s2_servers: the IDs of s2 servers you want to delete.
        """
        action = const.ACTION_DELETE_S2_SERVERS
        valid_keys = [
            's2_servers'
        ]
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(
                body,
                list_params=['s2_servers'],
        ):
            return None

        return self.conn.send_request(action, body)

    def poweron_s2_servers(self,
                           s2_servers,
                           **ignore):
        """ PowerOn S2 servers

        :param s2_servers: the IDs of s2 servers you want to power on.
        """
        action = const.ACTION_POWERON_S2_SERVERS
        valid_keys = [
            's2_servers',
        ]
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(
                body,
                list_params=['s2_servers'],
        ):
            return None

        return self.conn.send_request(action, body)

    def poweroff_s2_servers(self,
                            s2_servers,
                            **ignore):
        """ PowerOff S2 servers

        :param s2_servers: the IDs of s2 servers you want to power off.
        """
        action = const.ACTION_POWEROFF_S2_SERVERS
        valid_keys = [
            's2_servers',
        ]
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(
                body,
                list_params=['s2_servers'],
        ):
            return None

        return self.conn.send_request(action, body)

    def update_s2_servers(self,
                          s2_servers,
                          **ignore):
        """ Update S2 servers

        :param s2_servers: the IDs of s2 servers you want to update.
        """
        action = const.ACTION_UPDATE_S2_SERVERS
        valid_keys = [
            's2_servers',
        ]
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(
                body,
                list_params=['s2_servers'],
        ):
            return None

        return self.conn.send_request(action, body)

    def change_s2_server_vxnet(self,
                               s2_server,
                               vxnet,
                               private_ip=None,
                               **ignore):
        """ Change S2 server vxnet

        :param s2_server: the ID of s2 server.
        :param vxnet: the ID of vxnet.
        :param private_ip: you may specify the ip address of this server.
        """
        action = const.ACTION_CHANGE_S2_SERVER_VXNET
        valid_keys = [
            's2_server', 'vxnet', 'private_ip',
        ]
        body = filter_out_none(locals(), valid_keys)

        return self.conn.send_request(action, body)

    def create_s2_shared_target(self,
                                s2_server_id,
                                export_name,
                                target_type,
                                description=None,
                                volumes=None,
                                initiator_names=None,
                                **ignore):
        """ Create S2 shared target

        :param s2_server_id: the ID of s2 server.
        :param export_name: the name of shared target.
        :param target_type: valid values includes 'ISCSI', 'FCoE','NFS' and 'SMB'.
        :param description: the detailed description of the resource.
        :param volumes: the IDs of volumes will be attached as backstore.
        :param initiator_names: specify client IQN, available in vsan.
        """
        action = const.ACTION_CREATE_S2_SHARED_TARGET
        valid_keys = [
            's2_server_id', 'export_name', 'target_type',
            'description', 'volumes', 'initiator_names',
        ]
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(
                body,
                list_params=['volumes', 'initiator_names'],
        ):
            return None

        return self.conn.send_request(action, body)

    def describe_s2_shared_targets(self,
                                   shared_targets=None,
                                   target_types=None,
                                   s2_server_id=None,
                                   export_name=None,
                                   search_word=None,
                                   verbose=None,
                                   offset=None,
                                   limit=None,
                                   **ignore):
        """ Describe S2 servers

        :param shared_targets: the IDs of shared targets.
        :param target_types: valid values includes 'ISCSI', 'FCoE','NFS' and 'SMB'.
        :param s2_server_id: the ID of s2 server.
        :param export_name: the name of shared target.
        :param search_word: you may use this field to search from export_name or description.
        :param verbose: the number to specify the verbose level, larger the number, the more detailed information will be returned.
        :param offset: the starting offset of the returning results.
        :param limit: specify the number of the returning results.
        """
        action = const.ACTION_DESCRIBE_S2_SHARED_TARGETS
        valid_keys = [
            'shared_targets', 'target_types', 's2_server_id', 'export_name',
            'search_word', 'verbose', 'offset', 'limit',
        ]
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(
                body,
                integer_params=["limit", "offset", "verbose"],
                list_params=["shared_targets", "target_types"],
        ):
            return None

        return self.conn.send_request(action, body)

    def delete_s2_shared_targets(self,
                                 shared_targets,
                                 **ignore):
        """ Delete S2 shared targets

        :param shared_targets: the IDs of shared targets you want to delete.
        """
        action = const.ACTION_DELETE_S2_SHARED_TARGETS
        valid_keys = [
            'shared_targets',
        ]
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(
                body,
                list_params=['shared_targets'],
        ):
            return None

        return self.conn.send_request(action, body)

    def enable_s2_shared_targets(self,
                                 shared_targets,
                                 **ignore):
        """ Enable S2 shared targets

        :param shared_targets: the IDs of shared targets you want to enable.
        """
        action = const.ACTION_ENABLE_S2_SHARED_TARGETS
        valid_keys = [
            'shared_targets',
        ]
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(
                body,
                list_params=['shared_targets'],
        ):
            return None

        return self.conn.send_request(action, body)

    def disable_s2_shared_targets(self,
                                  shared_targets,
                                  **ignore):
        """ Disable S2 shared targets

        :param shared_targets: the IDs of shared targets you want to disable.
        """
        action = const.ACTION_DISABLE_S2_SHARED_TARGETS
        valid_keys = [
            'shared_targets',
        ]
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(
                body,
                list_params=['shared_targets'],
        ):
            return None

        return self.conn.send_request(action, body)

    def modify_s2_shared_target_attributes(self,
                                           shared_target,
                                           operation,
                                           parameters=None,
                                           initiator_names=None,
                                           s2_group=None,
                                           export_name=None,
                                           **ignore):
        """ Modify S2 shared target attributes

        :param shared_target: the ID of shared target.
        :param operation: valid values includes add, modify, delete, set.
        :param parameters: please refer https://docs.qingcloud.com/api/s2/describle_s2_default_parameters.html
        :param initiator_names: client IQN.
        :param s2_group: the ID of permission group.
        :param export_name: the name of shared target, available in vnas.
        """
        action = const.ACTION_MODIFY_S2_SHARED_TARGET
        valid_keys = [
            'shared_target', 'operation', 'parameters',
            'initiator_names', 's2_group', 'export_name',
        ]
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(
                body,
                list_params=["initiator_names", "parameters"],
        ):
            return None

        return self.conn.send_request(action, body)

    def attach_to_s2_shared_target(self,
                                   shared_target,
                                   volumes,
                                   **ignore):
        """ Attach to S2 shared target

        :param shared_target: the ID of shared target.
        :param volumes: the IDs of volumes.
        """
        action = const.ACTION_ATTACH_TO_S2_SHARED_TARGET
        valid_keys = [
            'shared_target', 'volumes',
        ]
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(
                body,
                list_params=['volumes'],
        ):
            return None

        return self.conn.send_request(action, body)

    def detach_from_s2_shared_target(self,
                                     shared_target,
                                     volumes,
                                     **ignore):
        """ Detach from s2 shared target

        :param shared_target: the ID of shared target.
        :param volumes: the IDs of volumes.
        """
        action = const.ACTION_DETACH_FROM_S2_SHARED_TARGET
        valid_keys = [
            'shared_target', 'volumes',
        ]
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(
                body,
                list_params=['volumes'],
        ):
            return None

        return self.conn.send_request(action, body)

    def describe_s2_default_parameters(self,
                                       service_type=None,
                                       target_type=None,
                                       offset=None,
                                       limit=None,
                                       **ignore):
        """ Describe S2 default parameters

        :param service_type: valid values is vsan or vnas.
        :param target_type: valid values is ISCSI, FCoE, NFS or SMB.
        :param offset: the starting offset of the returning results.
        :param limit: specify the number of the returning results.
        """
        action = const.ACTION_DESCRIBE_S2_DEFAULT_PARAMETERS
        valid_keys = [
            'service_type', 'target_type', 'offset', 'limit',
        ]
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(
                body,
                integer_params=['offset', 'limit'],
        ):
            return None

        return self.conn.send_request(action, body)

    def create_s2_group(self,
                        group_type,
                        group_name=None,
                        s2_accounts=None,
                        description=None,
                        **ignore):
        """ Create S2 group

        :param group_type: valid values is NFS_GROUP or SMB_GROUP.
        :param group_name: the name of group.
        :param s2_accounts: the IDs of s2 accounts.
        :param description: the detailed description of the resource.
        """
        action = const.ACTION_CREATE_S2_GROUP
        valid_keys = [
            'group_type', 'group_name', 's2_accounts', 'description',
        ]
        body = filter_out_none(locals(), valid_keys)

        return self.conn.send_request(action, body)

    def describe_s2_groups(self,
                           s2_groups=None,
                           group_types=None,
                           group_name=None,
                           search_word=None,
                           verbose=None,
                           offset=None,
                           limit=None,
                           **ignore):
        """ Describe S2 groups

        :param s2_groups: the IDs of s2 groups.
        :param group_types: valid values is NFS_GROUP or SMB_GROUP.
        :param group_name: the name of group.
        :param search_word: you may use this field to search from id or name.
        :param verbose: the number to specify the verbose level, larger the number, the more detailed information will be returned.
        :param offset: the starting offset of the returning results.
        :param limit: specify the number of the returning results.
        """
        action = const.ACTION_DESCRIBE_S2_GROUPS
        valid_keys = [
            's2_groups', 'group_types', 'account_name', 'search_word',
            'verbose', 'offset', 'limit',
        ]
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(
                body,
                integer_params=['offset', 'limit', 'verbose'],
                list_params=['s2_groups', 'group_types'],
        ):
            return None

        return self.conn.send_request(action, body)

    def modify_s2_group(self,
                        s2_group,
                        group_name=None,
                        s2_accounts=None,
                        description=None,
                        **ignore):
        """ Modify S2 group

        :param s2_group: the ID of group.
        :param group_name: the name of group.
        :param s2_accounts: the IDs of accounts.
        :param description: the new value of description.
        """
        action = const.ACTION_MODIFY_S2_GROUP
        valid_keys = [
            's2_group', 'group_name', 's2_accounts', 'description',
        ]
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(
                body,
                list_params=['s2_accounts'],
        ):
            return None

        return self.conn.send_request(action, body)

    def delete_s2_group(self,
                        s2_groups,
                        **ignore):
        """ Delete S2 groups

        :param s2_groups: the IDs of groups.
        """
        action = const.ACTION_DELETE_S2_GROUPS
        valid_keys = [
            's2_groups',
        ]
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(
                body,
                list_params=['s2_groups'],
        ):
            return None

        return self.conn.send_request(action, body)

    def create_s2_account(self,
                          account_type,
                          account_name=None,
                          smb_name=None,
                          smb_passwd=None,
                          nfs_ipaddr=None,
                          s2_groups=None,
                          opt_parameters=None,
                          description=None,
                          **ignore):
        """ Create S2 account

        :param account_type: valid values is NFS or SMB.
        :param account_name: the name of account.
        :param smb_name: the user name of smb.
        :param smb_passwd: the password of smb.
        :param nfs_ipaddr: ip address available in NFS.
        :param s2_groups: the JSON form of groups. e.g. '[{"group_id":"s2g-xxxx", "rw_flag": "rw"}]'
        :param opt_parameters: options parameters for NFS.
        :param description: the detailed description of the resource.
        """
        action = const.ACTION_CREATE_S2_ACCOUNT
        valid_keys = [
            'account_type', 'account_name', 'smb_name', 'smb_passwd',
            'nfs_ipaddr', 's2_groups', 'opt_parameters', 'description',
        ]
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(
                body,
                list_params=["s2_groups"],
        ):
            return None

        return self.conn.send_request(action, body)

    def describe_s2_accounts(self,
                             s2_accounts=None,
                             account_types=None,
                             account_name=None,
                             search_word=None,
                             verbose=None,
                             offset=None,
                             limit=None,
                             **ignore):
        """ Describe S2 accounts

        :param s2_accounts: the IDs of accounts.
        :param account_types: valid values is NFS or SMB.
        :param account_name: the name of account.
        :param search_word: you may use this field to search from id, account_name nfs_ipaddr or smb_name.
        :param verbose: the number to specify the verbose level, larger the number, the more detailed information will be returned.
        :param offset: the starting offset of the returning results.
        :param limit: specify the number of the returning results.
        """
        action = const.ACTION_DESCRIBE_S2_ACCOUNTS
        valid_keys = [
            's2_accounts', 'account_types', 'account_name', 'search_word',
            'verbose', 'offset', 'limit',
        ]
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(
                body,
                integer_params=["limit", "offset", "verbose"],
                list_params=["s2_accounts", "account_types"],
        ):
            return None

        return self.conn.send_request(action, body)

    def modify_s2_account(self,
                          s2_account,
                          opt_parameters=None,
                          account_name=None,
                          smb_passwd=None,
                          nfs_ipaddr=None,
                          description=None,
                          **ignore):
        """ Modify S2 account

        :param s2_account: the ID of account.
        :param opt_parameters: the options parameters.
        :param account_name: the new value of account name.
        :param smb_passwd: the new password.
        :param nfs_ipaddr: the new ip address.
        :param description: the new value of description.
        """
        action = const.ACTION_MODIFY_S2_ACCOUNT
        valid_keys = [
            's2_account', 'opt_parameters', 'account_name', 'smb_passwd',
            'nfs_ipaddr', 'description',
        ]
        body = filter_out_none(locals(), valid_keys)

        return self.conn.send_request(action, body)

    def delete_s2_accounts(self,
                           s2_accounts,
                           **ignore):
        """ Delete S2 accounts

        :param s2_accounts: the IDs of accounts.
        """
        action = const.ACTION_DELETE_S2_ACCOUNTS
        valid_keys = [
            's2_accounts'
        ]
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(
                body,
                list_params=['s2_accounts'],
        ):
            return None

        return self.conn.send_request(action, body)

    def associate_s2_account_group(self,
                                   s2_group,
                                   s2_accounts,
                                   **ignore):
        """ Associate S2 account group

        :param s2_group: the ID of group.
        :param s2_accounts: the JSON form of accounts. e.g. '[{"account_id": "s2a-xxxx", "rw_flag": "rw"}]'
        """
        action = const.ACTION_ASSOCIATE_S2_ACCOUNT_GROUP
        valid_keys = [
            's2_group', 's2_accounts',
        ]
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(
                body,
                list_params=['s2_accounts'],
        ):
            return None

        return self.conn.send_request(action, body)

    def dissociate_s2_account_group(self,
                                    s2_groups,
                                    s2_accounts,
                                    **ignore):
        """ Dissociate S2 account group

        :param s2_groups: the IDs of groups.
        :param s2_accounts: the IDs of accounts.
        """
        action = const.ACTION_DISSOCIATE_S2_ACCOUNT_GROUP
        valid_keys = [
            's2_groups', 's2_accounts',
        ]
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(
                body,
                list_params=['s2_groups', 's2_accounts'],
        ):
            return None

        return self.conn.send_request(action, body)
