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


class SecurityGroupAction(object):

    def __init__(self, conn):
        self.conn = conn

    def describe_security_groups(self, security_groups=None,
                                 security_group_name=None,
                                 search_word=None,
                                 owner=None,
                                 verbose=0,
                                 offset=None,
                                 limit=None,
                                 tags=None,
                                 **ignore):
        """ Describe security groups filtered by condition
        @param security_groups: IDs of the security groups you want to describe.
        @param security_group_name: the name of the security group.
        @param verbose: the number to specify the verbose level, larger the number, the more detailed information will be returned.
        @param offset: the starting offset of the returning results.
        @param limit: specify the number of the returning results.
        @param tags : the array of IDs of tags.
        """
        action = const.ACTION_DESCRIBE_SECURITY_GROUPS
        valid_keys = ['security_groups', 'security_group_name', 'search_word',
                      'verbose', 'offset', 'limit', 'tags', 'owner']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=[],
                                                  integer_params=[
                                                      'offset', 'limit', 'verbose'],
                                                  list_params=[
                                                      'security_groups', 'tags']
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def create_security_group(self, security_group_name, target_user=None,
                              **ignore):
        """ Create a new security group without any rule.
        @param security_group_name: the name of the security group you want to create.
        @param target_user: ID of user who will own this resource, should be one of your sub-accounts
        """
        action = const.ACTION_CREATE_SECURITY_GROUP
        body = {'security_group_name': security_group_name}
        if target_user:
            body['target_user'] = target_user
        if not self.conn.req_checker.check_params(body,
                                                  required_params=[
                                                      'security_group_name'],
                                                  integer_params=[],
                                                  list_params=[]
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def modify_security_group_attributes(self, security_group,
                                         security_group_name=None,
                                         description=None,
                                         **ignore):
        """ Modify security group attributes.
        @param security_group: the ID of the security group whose content you
        want to update.
        @param security_group_name: the new group name you want to update.
        @param description: The detailed description of the resource.
        """
        action = const.ACTION_MODIFY_SECURITY_GROUP_ATTRIBUTES
        valid_keys = ['security_group', 'security_group_name', 'description']
        body = filter_out_none(locals(), valid_keys)
        body['security_group'] = security_group
        if not self.conn.req_checker.check_params(body,
                                                  required_params=[
                                                      'security_group'],
                                                  integer_params=[],
                                                  list_params=[]
                                                  ):
            return None

        if not self.conn.req_checker.check_sg_rules(body.get('rules', [])):
            return None

        return self.conn.send_request(action, body)

    def apply_security_group(self, security_group,
                             instances=None,
                             target_user=None,
                             **ignore):
        """ Apply a security group with current rules.
        If `instances` specified, apply the security group to them,
        or will affect all instances that has applied this security group.
        @param security_group: the ID of the security group that you
        want to apply to instances.
        @param instances: the IDs of the instances you want to apply the security group.
        @param target_user: ID of user who will own this resource, should be one of your sub-accounts
        """
        action = const.ACTION_APPLY_SECURITY_GROUP
        valid_keys = ['security_group', 'instances', 'target_user']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=[
                                                      'security_group'],
                                                  integer_params=[],
                                                  list_params=['instances']
                                                  ):
            return None
        return self.conn.send_request(action, body)

    def remove_security_group(self,
                              instances,
                              **ignore):
        """ Remove security group from instances.
        @param instances: the IDs of the instances you want to remove the security group.
        """
        action = const.ACTION_REMOVE_SECURITY_GROUP
        valid_keys = ['instances']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=[
                                                      'instances'],
                                                  integer_params=[],
                                                  list_params=['instances']
                                                  ):
            return None
        return self.conn.send_request(action, body)

    def delete_security_groups(self, security_groups,
                               **ignore):
        """ Delete one or more security groups.
        @param security_groups: the IDs of the security groups you want to delete.
        """
        action = const.ACTION_DELETE_SECURITY_GROUPS
        body = {'security_groups': security_groups}
        if not self.conn.req_checker.check_params(body,
                                                  required_params=[
                                                      'security_groups'],
                                                  integer_params=[],
                                                  list_params=['security_groups']
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def describe_security_group_rules(self, security_group=None,
                                      security_group_rules=None,
                                      direction=None,
                                      offset=None,
                                      limit=None,
                                      **ignore):
        """ Describe security group rules filtered by condition.
        @param security_group: the ID of the security group whose rules you want to describe.
        @param security_group_rules: the IDs of the security group rules you want to describe.
        @param direction: 0 for inbound; 1 for outbound
        @param offset: the starting offset of the returning results.
        @param limit: specify the number of the returning results.
        """
        action = const.ACTION_DESCRIBE_SECURITY_GROUP_RULES
        valid_keys = ['security_group', 'security_group_rules', 'direction',
                      'offset', 'limit']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=[],
                                                  integer_params=[
                                                      'direction', 'offset', 'limit'],
                                                  list_params=[
                                                      'security_group_rules']
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def add_security_group_rules(self, security_group,
                                 rules,
                                 target_user=None,
                                 **ignore):
        """ Add rules to security group.
        @param security_group: the ID of the security group whose rules you
        want to add.
        @param rules: a list of rules you want to add,
        can be created by SecurityGroupRuleFactory.
        @param target_user: ID of user who will own this resource, should be one of your sub-accounts
        """
        action = const.ACTION_ADD_SECURITY_GROUP_RULES
        valid_keys = ['security_group', 'rules', 'target_user']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=[
                                                      'security_group', 'rules'],
                                                  integer_params=[],
                                                  list_params=['rules']
                                                  ):
            return None

        if not self.conn.req_checker.check_sg_rules(body.get('rules', [])):
            return None

        return self.conn.send_request(action, body)

    def delete_security_group_rules(self, security_group_rules,
                                    **ignore):
        """ Delete one or more security group rules.
        @param security_group_rules: the IDs of rules you want to delete.
        """
        action = const.ACTION_DELETE_SECURITY_GROUP_RULES
        body = {'security_group_rules': security_group_rules}
        if not self.conn.req_checker.check_params(body,
                                                  required_params=[
                                                      'security_group_rules'],
                                                  integer_params=[],
                                                  list_params=[
                                                      'security_group_rules']
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def modify_security_group_rule_attributes(self, security_group_rule,
                                              priority=None,
                                              security_group_rule_name=None,
                                              rule_action=None,
                                              direction=None,
                                              protocol=None,
                                              val1=None,
                                              val2=None,
                                              val3=None,
                                              disabled=None,
                                              **ignore):
        """ Modify security group rule attributes.
        @param security_group_rule: the ID of the security group rule whose attributes you
        want to update.
        @param priority: priority [0 - 100].
        @param security_group_rule_name: name of the rule.
        @param rule_action: "accept" or "drop".
        @param direction: 0 for inbound; 1 for outbound.
        @param protocol: supported protocols are "icmp", "tcp", "udp", "gre".
        @param val1: for "icmp" protocol, this field is "icmp type";
        for "tcp/udp", it's "start port", empty means all.
        @param val2: for "icmp" protocol, this field is "icmp code";
        for "tcp/udp", it's "end port", empty means all.
        @param val3: ip network, e.g "1.2.3.0/24"
        """
        action = const.ACTION_MODIFY_SECURITY_GROUP_RULE_ATTRIBUTES
        valid_keys = ['security_group_rule', 'priority', 'security_group_rule_name',
                      'rule_action', 'direction', 'protocol', 'val1', 'val2', 'val3',
                      'disabled']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=[
                                                      'security_group_rule'],
                                                  integer_params=['priority'],
                                                  list_params=[]
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def describe_security_group_ipsets(self,
                                       security_group_ipsets=None,
                                       ipset_type=None,
                                       security_group_ipset_name=None,
                                       offset=None,
                                       limit=None,
                                       **ignore):
        """ Describe security group ipsets filtered by condition.
        @param security_group_ipsets: the ID of the security group ipsets.
        @param ipset_type: 0 for ip; 1 for port
        @param security_group_ipset_name: filter by name
        @param offset: the starting offset of the returning results.
        @param limit: specify the number of the returning results.
        """
        action = const.ACTION_DESCRIBE_SECURITY_GROUP_IPSETS
        valid_keys = ['security_group_ipsets', 'ipset_type',
                      'security_group_ipset_name',
                      'offset', 'limit']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=[],
                                                  integer_params=[
                                                      'ipset_type', 'offset', 'limit'],
                                                  list_params=[
                                                      'security_group_rules']
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def create_security_group_ipset(self,
                                    ipset_type, val,
                                    security_group_ipset_name=None,
                                    target_user=None,
                                    **ignore):
        """ Create security group ipset.
        @param ipset_type: 0 for ip; 1 for port
        @param val: such as 192.168.1.0/24 or 10000-15000
        @param security_group_ipset_name: the name of the security group ipsets
        @param target_user: ID of user who will own this resource, should be one of your sub-accounts
        """
        action = const.ACTION_CREATE_SECURITY_GROUP_IPSET
        valid_keys = ['security_group_ipset_name', 'ipset_type', 'val', 'target_user']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=[
                                                      'ipset_type', 'val'],
                                                  integer_params=['ipset_type'],
                                                  list_params=[]
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def delete_security_group_ipsets(self,
                                     security_group_ipsets,
                                     **ignore):
        """ Delete one or more security group ipsets.
        @param security_group_ipsets: the IDs of ipsets you want to delete.
        """
        action = const.ACTION_DELETE_SECURITY_GROUP_IPSETS
        body = {'security_group_ipsets': security_group_ipsets}
        if not self.conn.req_checker.check_params(body,
                                                  required_params=[
                                                      'security_group_ipsets'],
                                                  integer_params=[],
                                                  list_params=[
                                                      'security_group_ipsets']
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def modify_security_group_ipset_attributes(self,
                                               security_group_ipset,
                                               security_group_ipset_name=None,
                                               description=None,
                                               val=None,
                                               **ignore):
        """ Modify security group ipset attributes.
        @param security_group_ipset: the ID of the security group ipset whose attributes you
        want to update.
        @param security_group_ipset_name: name of the ipset.
        @param description: The detailed description of the resource.
        @param val1: for "ip", this field is like:  192.168.1.0/24
        for "port", this field is like: 10000-15000
        """
        action = const.ACTION_MODIFY_SECURITY_GROUP_IPSET_ATTRIBUTES
        valid_keys = ['security_group_ipset', 'security_group_ipset_name',
                      'description', 'val']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=[
                                                      'security_group_ipset'],
                                                  integer_params=[],
                                                  list_params=[]
                                                  ):
            return None

        return self.conn.send_request(action, body)
