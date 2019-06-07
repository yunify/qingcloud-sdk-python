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


class LoadBalancerAction(object):

    def __init__(self, conn):
        self.conn = conn

    def describe_loadbalancers(self, loadbalancers=None,
                               status=None,
                               verbose=0,
                               owner=None,
                               search_word=None,
                               offset=None,
                               limit=None,
                               tags=None,
                               **ignore):
        """ Describe loadbalancers filtered by condition.
        @param loadbalancers : the array of load balancer IDs.
        @param status: pending, active, stopped, deleted, suspended, ceased
        @param verbose: the number to specify the verbose level, larger the number, the more detailed information will be returned.
        @param search_word: search word column.
        @param offset: the starting offset of the returning results.
        @param limit: specify the number of the returning results.
        @param tags : the array of IDs of tags.
        """
        action = const.ACTION_DESCRIBE_LOADBALANCERS
        valid_keys = ['loadbalancers', 'status', 'verbose', 'search_word',
                      'offset', 'limit', 'tags', 'owner']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=[],
                                                  integer_params=[
                                                      'offset', 'limit'],
                                                  list_params=[
                                                      'loadbalancers', 'status', 'tags']
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def create_loadbalancer(self,
                            eips=None,
                            loadbalancer_name=None,
                            security_group=None,
                            node_count=None,
                            loadbalancer_type=const.LB_TYPE_MAXCONN_5k,
                            vxnet=None,
                            private_ip=None,
                            target_user=None,
                            mode=None,
                            **ignore):
        """ Create new load balancer.
        @param eips: the IDs of the eips that will be associated to load balancer.
        @param loadbalancer_name: the name of the loadbalancer.
        @param security_group: the id of the security_group you want to apply to loadbalancer,
        use `default security` group as default.
        @param target_user: ID of user who will own this resource, should be one of your sub-accounts
        """
        action = const.ACTION_CREATE_LOADBALANCER
        valid_keys = ['eips', 'loadbalancer_name', 'loadbalancer_type',
                      'security_group', 'node_count', 'vxnet', 'private_ip',
                      'target_user', 'mode',
                      ]
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=[],
                                                  integer_params=['node_count', 'mode'],
                                                  list_params=['eips']
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def delete_loadbalancers(self, loadbalancers,
                             **ignore):
        """ Delete one or more load balancers.
        @param loadbalancers: the IDs of load balancers you want to delete.
        """
        action = const.ACTION_DELETE_LOADBALANCERS
        body = {'loadbalancers': loadbalancers}
        if not self.conn.req_checker.check_params(body,
                                                  required_params=['loadbalancers'],
                                                  integer_params=[],
                                                  list_params=[]
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def stop_loadbalancers(self, loadbalancers,
                           **ignore):
        """ Stop one or more load balancers.
        @param loadbalancers: the array of load balancer IDs.
        """
        action = const.ACTION_STOP_LOADBALANCERS
        body = {'loadbalancers': loadbalancers}
        if not self.conn.req_checker.check_params(body,
                                                  required_params=['loadbalancers'],
                                                  integer_params=[],
                                                  list_params=['loadbalancers']
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def start_loadbalancers(self, loadbalancers,
                            **ignore):
        """ Start one or more load balancers.
        @param loadbalancers: the array of load balancer IDs.
        """
        action = const.ACTION_START_LOADBALANCERS
        body = {'loadbalancers': loadbalancers}
        if not self.conn.req_checker.check_params(body,
                                                  required_params=['loadbalancers'],
                                                  integer_params=[],
                                                  list_params=['loadbalancers']
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def update_loadbalancers(self, loadbalancers, target_user=None,
                             **ignore):
        """ Update one or more load balancers.
        @param loadbalancers: the array of load balancer IDs.
        @param target_user: ID of user who will own this resource, should be one of your sub-accounts
        """
        action = const.ACTION_UPDATE_LOADBALANCERS
        body = {'loadbalancers': loadbalancers}
        if target_user:
            body['target_user'] = target_user
        if not self.conn.req_checker.check_params(body,
                                                  required_params=['loadbalancers'],
                                                  integer_params=[],
                                                  list_params=['loadbalancers']
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def associate_eips_to_loadbalancer(self, loadbalancer,
                                       eips,
                                       **ignore):
        """ Associate one or more eips to load balancer.
        @param loadbalancer: the ID of load balancer.
        @param eips: the array of eip IDs.
        """
        action = const.ACTION_ASSOCIATE_EIPS_TO_LOADBALANCER
        body = {'loadbalancer': loadbalancer, 'eips': eips}
        if not self.conn.req_checker.check_params(body,
                                                  required_params=[
                                                      'loadbalancer', 'eips'],
                                                  integer_params=[],
                                                  list_params=['eips']
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def dissociate_eips_from_loadbalancer(self, loadbalancer,
                                          eips,
                                          **ignore):
        """ Dissociate one or more eips from load balancer.
        @param loadbalancer: the ID of load balancer.
        @param eips: the array of eip IDs.
        """
        action = const.ACTION_DISSOCIATE_EIPS_FROM_LOADBALANCER
        body = {'loadbalancer': loadbalancer, 'eips': eips}
        if not self.conn.req_checker.check_params(body,
                                                  required_params=[
                                                      'loadbalancer', 'eips'],
                                                  integer_params=[],
                                                  list_params=['eips']
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def modify_loadbalancer_attributes(self, loadbalancer,
                                       security_group=None,
                                       loadbalancer_name=None,
                                       description=None,
                                       **ignore):
        """ Modify load balancer attributes.
        @param loadbalancer: the ID of loadbalancer you want to modify.
        @param security_group: the ID of the security_group.
        @param loadbalancer_name: the name of the loadbalancer.
        @param description: the description of the loadbalancer.
        """
        action = const.ACTION_MODIFY_LOADBALANCER_ATTRIBUTES
        valid_keys = ['loadbalancer', 'security_group', 'loadbalancer_name',
                      'description']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=['loadbalancer'],
                                                  integer_params=[],
                                                  list_params=[]
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def describe_loadbalancer_listeners(self, loadbalancer_listeners=None,
                                        loadbalancer=None,
                                        verbose=0,
                                        limit=None,
                                        offset=None,
                                        **ignore):
        """ Describe load balancer listeners by filter condition.
        @param loadbalancer_listeners: filter by load balancer listener IDs.
        @param loadbalancer: filter by loadbalancer ID.
        @param verbose: the number to specify the verbose level, larger the number, the more detailed information will be returned.
        @param offset: the starting offset of the returning results.
        @param limit: specify the number of the returning results.
        """
        action = const.ACTION_DESCRIBE_LOADBALANCER_LISTENERS
        valid_keys = ['loadbalancer_listeners', 'loadbalancer', 'verbose',
                      'limit', 'offset']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=[],
                                                  integer_params=[
                                                      'verbose', 'limit', 'offset'],
                                                  list_params=[
                                                      'loadbalancer_listeners']
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def add_listeners_to_loadbalancer(self, loadbalancer,
                                      listeners,
                                      target_user=None,
                                      **ignore):
        """ Add listeners to load balancer.
        @param loadbalancer: The ID of loadbalancer.
        @param listeners: the listeners to add.
        @param target_user: ID of user who will own this resource, should be one of your sub-accounts
        """
        action = const.ACTION_ADD_LOADBALANCER_LISTENERS
        valid_keys = ['listeners', 'loadbalancer', 'target_user']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=[
                                                      'loadbalancer', 'listeners'],
                                                  integer_params=[],
                                                  list_params=['listeners']
                                                  ):
            return None

        self.conn.req_checker.check_lb_listeners(listeners)

        return self.conn.send_request(action, body)

    def delete_loadbalancer_listeners(self, loadbalancer_listeners,
                                      **ignore):
        """ Delete load balancer listeners.
        @param loadbalancer_listeners: the array of listener IDs.
        """
        action = const.ACTION_DELETE_LOADBALANCER_LISTENERS
        body = {'loadbalancer_listeners': loadbalancer_listeners}
        if not self.conn.req_checker.check_params(body,
                                                  required_params=[],
                                                  integer_params=[],
                                                  list_params=[
                                                      'loadbalancer_listeners']
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def describe_loadbalancer_backends(self, loadbalancer_backends=None,
                                       loadbalancer_listener=None,
                                       loadbalancer=None,
                                       verbose=0,
                                       limit=None,
                                       offset=None,
                                       **ignore):
        """ Describe load balancer backends.
        @param loadbalancer_backends: filter by load balancer backends ID.
        @param loadbalancer_listener: filter by load balancer listener ID.
        @param loadbalancer: filter by load balancer ID.
        @param verbose: the number to specify the verbose level, larger the number, the more detailed information will be returned.
        @param offset: the starting offset of the returning results.
        @param limit: specify the number of the returning results.
        """
        action = const.ACTION_DESCRIBE_LOADBALANCER_BACKENDS
        valid_keys = ['loadbalancer_backends', 'loadbalancer_listener',
                      'loadbalancer', 'verbose', 'limit', 'offset']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=[],
                                                  integer_params=[
                                                      'verbose', 'limit', 'offset'],
                                                  list_params=[
                                                      'loadbalancer_backends']
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def add_backends_to_listener(self, loadbalancer_listener,
                                 backends,
                                 target_user=None,
                                 **ignore):
        """ Add one or more backends to load balancer listener.
        @param loadbalancer_listener: the ID of load balancer listener
        @param backends: the load balancer backends to add
        @param target_user: ID of user who will own this resource, should be one of your sub-accounts
        """
        action = const.ACTION_ADD_LOADBALANCER_BACKENDS
        body = {'loadbalancer_listener': loadbalancer_listener,
                'backends': backends}
        if target_user:
            body['target_user'] = target_user
        if not self.conn.req_checker.check_params(body,
                                                  required_params=[
                                                      'loadbalancer_listener', 'backends'],
                                                  integer_params=[],
                                                  list_params=['backends']
                                                  ):
            return None

        self.conn.req_checker.check_lb_backends(backends)

        return self.conn.send_request(action, body)

    def delete_loadbalancer_backends(self, loadbalancer_backends,
                                     **ignore):
        """ Delete load balancer backends.
        @param loadbalancer_backends: the array of backends IDs.
        """
        action = const.ACTION_DELETE_LOADBALANCER_BACKENDS
        body = {'loadbalancer_backends': loadbalancer_backends}
        if not self.conn.req_checker.check_params(body,
                                                  required_params=[
                                                      'loadbalancer_backends'],
                                                  integer_params=[],
                                                  list_params=[
                                                      'loadbalancer_backends']
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def modify_loadbalancer_backend_attributes(self, loadbalancer_backend,
                                               loadbalancer_backend_name=None,
                                               port=None,
                                               weight=None,
                                               disabled=None,
                                               **ignore):
        """ Modify load balancer backend attributes.
        @param loadbalancer_backend: the ID of backend.
        @param loadbalancer_backend_name: the name of the backend.
        @param port: backend server listen port.
        @param weight: backend server weight, valid range is from 1 to 100.
        """
        action = const.ACTION_MODIFY_LOADBALANCER_BACKEND_ATTRIBUTES
        valid_keys = ['loadbalancer_backend', 'loadbalancer_backend_name',
                      'port', 'weight', 'disabled']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=[
                                                      'loadbalancer_backend'],
                                                  integer_params=[
                                                      'port', 'weight', 'disabled'],
                                                  list_params=[]
                                                  ):
            return None

        if 'port' in body:
            self.conn.req_checker.check_lb_backend_port(body['port'])
        if 'weight' in body:
            self.conn.req_checker.check_lb_backend_weight(body['weight'])

        return self.conn.send_request(action, body)

    def modify_loadbalancer_listener_attributes(self, loadbalancer_listener,
                                                loadbalancer_listener_name=None,
                                                balance_mode=None,
                                                forwardfor=None,
                                                healthy_check_method=None,
                                                healthy_check_option=None,
                                                session_sticky=None,
                                                server_certificate_id=None,
                                                **ignore):
        """ Modify load balancer listener attributes
        @param loadbalancer_listener: the ID of listener.
        @param loadbalancer_listener_name: the name of the listener.
        @param balance_mode: defined in constants.py,
        BALANCE_ROUNDROBIN, BALANCE_LEASTCONN
        @param forwardfor: extra http headers, represented as bitwise flag defined in constants.py,
        HEADER_QC_LB_IP, HEADER_QC_LB_ID and HEADER_X_FORWARD_FOR.
        Example: if you need X-Forwarded-For and QC-LB-IP in http header,
        then forwardfor should be HEADER_X_FORWARD_FOR | HEADER_QC_LB_IP.
        @param description: the description of the listener.
        @param server_certificate_id: the ID of server certificate.
        """
        action = const.ACTION_MODIFY_LOADBALANCER_LISTENER_ATTRIBUTES
        valid_keys = ['loadbalancer_listener', 'loadbalancer_listener_name',
                      'balance_mode', 'forwardfor', 'healthy_check_method',
                      'healthy_check_option', 'session_sticky',
                      'server_certificate_id']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=[
                                                      'loadbalancer_listener'],
                                                  integer_params=['forwardfor'],
                                                  list_params=[]
                                                  ):
            return None

        if 'healthy_check_method' in body:
            self.conn.req_checker.check_lb_listener_healthy_check_method(
                body['healthy_check_method'])
        if 'healthy_check_option' in body:
            self.conn.req_checker.check_lb_listener_healthy_check_option(
                body['healthy_check_option'])

        return self.conn.send_request(action, body)

    def create_loadbalancer_policy(self, loadbalancer_policy_name=None,
                                   operator=None,
                                   **ignore):
        """ Create loadbalancer policy
        @param loadbalancer_name: the name of policy.
        @param operator: operation for policy, value is 'and','or'.
        default is 'or'
        """
        action = const.ACTION_CREATE_LOADBALANCER_POLICY
        valid_keys = ['loadbalancer_policy_name', 'operator']
        body = filter_out_none(locals(), valid_keys)

        if not self.conn.req_checker.check_params(body,
                                                  required_params=[],
                                                  integer_params=[],
                                                  list_params=[]
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def describe_loadbalancer_policies(self, loadbalancer_policies=None,
                                       verbose=0,
                                       offset=None,
                                       limit=None,
                                       **ignore):
        """  Describe load balancer policies.
        @param loadbalancer_policies: filter by load balancer policy ID.
        @param verbose: the number to specify the verbose level, larger the number, the more detailed information will be returned.
        @param offset: the starting offset of the returning results.
        @param limit: specify the number of the returning results.
        """

        action = const.ACTION_DESCRIBE_LOADBALANCER_POLICIES
        valid_keys = ['loadbalancer_policies',
                      'verbose', 'offset', 'limit']
        body = filter_out_none(locals(), valid_keys)

        if not self.conn.req_checker.check_params(body,
                                                  required_params=[],
                                                  integer_params=['offset', 'limit'],
                                                  list_params=['loadbalancer_policies']
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def modify_loadbalancer_policy_attributes(self,
                                              loadbalancer_policy=None,
                                              loadbalancer_policy_name=None,
                                              operator=None,
                                              **ignore):
        """ Modify load balancer policy attributes
        @param loadbalancer_policy: the ID of policy.
        @param loadbalancer_policy_name: the name of policy.
        @param operator: operation for policy, value is 'and','or'.
        :return:
        """

        action = const.ACTION_MODIFY_LOADBALANCER_POLICY_ATTRIBUTES
        valid_keys = ['loadbalancer_policy', 'loadbalancer_policy_name', 'operator']
        body = filter_out_none(locals(), valid_keys)

        if not self.conn.req_checker.check_params(body,
                                                  required_params=['loadbalancer_policy'],
                                                  integer_params=[],
                                                  list_params=[]
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def apply_loadbalancer_policy(self, loadbalancer_policy=None, **ignore):
        """ apply load balancer policy change
        @param loadbalancer_policy:  the ID of policy.
        """
        action = const.ACTION_APPLY_LOADBALANCER_POLICY
        valid_keys = ['loadbalancer_policy']
        body = filter_out_none(locals(), valid_keys)

        if not self.conn.req_checker.check_params(body,
                                                  required_params=['loadbalancer_policy'],
                                                  integer_params=[],
                                                  list_params=[]
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def delete_loadbalancer_policies(self, loadbalancer_policies,
                                     **ignore):
        """ Delete load balancer policies.
        @param loadbalancer_policies: the array of policies IDs.
        """
        action = const.ACTION_DELETE_LOADBALANCER_POLICIES
        body = {'loadbalancer_policies': loadbalancer_policies}
        if not self.conn.req_checker.check_params(body,
                                                  required_params=[
                                                      'loadbalancer_policies'],
                                                  integer_params=[],
                                                  list_params=[
                                                      'loadbalancer_policies']
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def add_loadbalancer_policy_rules(self, loadbalancer_policy,
                                      rules, **ignore):
        """ Add one or more rules to load balancer policy.
        @param loadbalancer_policy: the ID of load balancer policy
        @param rules: the load balancer policy rules to add
        """
        action = const.ACTION_ADD_LOADBALANCER_POLICY_RULES
        body = {'loadbalancer_policy': loadbalancer_policy,
                'rules': rules}
        if not self.conn.req_checker.check_params(body,
                                                  required_params=[
                                                      'loadbalancer_policy', 'rules'],
                                                  integer_params=[],
                                                  list_params=['rules']
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def describe_loadbalancer_policy_rules(self, loadbalancer_policy_rules=None,
                                           loadbalancer_policy=None,
                                           offset=None,
                                           limit=None,
                                           **ignore):
        """  Describe load balancer policy rules.
        @param loadbalancer_policy_rules: filter by load balancer rules ID.
        @param offset: the starting offset of the returning results.
        @param limit: specify the number of the returning results.
        """

        action = const.ACTION_DESCRIBE_LOADBALANCER_POLICY_RULES
        valid_keys = ['loadbalancer_policy_rules', 'loadbalancer_policy',
                      'offset', 'limit']
        body = filter_out_none(locals(), valid_keys)

        if not self.conn.req_checker.check_params(body,
                                                  required_params=[],
                                                  integer_params=['offset', 'limit'],
                                                  list_params=['loadbalancer_policy_rules']
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def modify_loadbalancer_policy_rule_attributes(self,
                                                   loadbalancer_policy_rule=None,
                                                   loadbalancer_policy_rule_name=None,
                                                   val=None,
                                                   **ignore):
        """ Modify load balancer policy rule attributes
        @param loadbalancer_policy: the ID of rule.
        @param loadbalancer_policy_name: the name of policy.
        @param val: rule new value.
        :return:
        """

        action = const.ACTION_MODIFY_LOADBALANCER_POLICY_RULE_ATTRIBUTES
        valid_keys = ['loadbalancer_policy_rule', 'loadbalancer_policy_rule_name', 'val']
        body = filter_out_none(locals(), valid_keys)

        if not self.conn.req_checker.check_params(body,
                                                  required_params=['loadbalancer_policy_rule'],
                                                  integer_params=[],
                                                  list_params=[]
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def delete_loadbalancer_policy_rules(self, loadbalancer_policy_rules,
                                         **ignore):
        """ Delete load balancer policy rules.
        @param loadbalancer_policy_rules: the array of policy rule IDs.
        """
        action = const.ACTION_DELETE_LOADBALANCER_POLICY_RULES
        body = {'loadbalancer_policy_rules': loadbalancer_policy_rules}
        if not self.conn.req_checker.check_params(body,
                                                  required_params=[
                                                      'loadbalancer_policy_rules'],
                                                  integer_params=[],
                                                  list_params=[
                                                      'loadbalancer_policy_rules']
                                                  ):
            return None

        return self.conn.send_request(action, body)
