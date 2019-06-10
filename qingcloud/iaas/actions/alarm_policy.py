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


class AlarmPolicy(object):

    def __init__(self, conn):
        self.conn = conn

    def describe_alarm_policies(self,
                                alarm_policies=None,
                                tags=None,
                                alarm_policy_name=None,
                                alarm_policy_type=None,
                                search_word=None,
                                resource=None,
                                status=None,
                                verbose=None,
                                offset=None,
                                limit=None,
                                **ignore):
        """ Describe alarm policies

        :param alarm_policies: id IDs of alarm policies you want to describe.
        :param tags: the array of IDs of tags.
        :param alarm_policy_name: the name of alarm policy.
        :param alarm_policy_type: valid values includes instance, eip, router, loadbalancer_listener_http, loadbalancer_listener_tcp, loadbalancer_backend_http, loadbalancer_backend_tcp.
        :param search_word: you can use this field to search from id or name.
        :param resource: the ID of resource associated to this policy.
        :param status: valid values includes active, suspended.
        :param verbose: the number to specify the verbose level,
                        larger the number, the more detailed information will be returned.
        :param offset: the starting offset of the returning results.
        :param limit: specify the number of the returning results.
        """
        action = const.ACTION_DESCRIBE_ALARM_POLICIES
        valid_keys = [
            'alarm_policies', 'alarm_policy_name',
            'alarm_policy_type', 'search_word', 'resource',
            'status', 'verbose', 'offset', 'limit', 'tags',
        ]
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(
            body,
            integer_params=['offset', 'limit', 'verbose'],
            list_params=['alarm_policies', 'status', 'tags'],
        ):
            return None

        return self.conn.send_request(action, body)

    def create_alarm_policy(self, alarm_policy_type,
                            period,
                            alarm_policy_name=None,
                            **ignore):
        """ Create an alarm policy.
        @param alarm_policy_type : the type of alarm_policy.
        @param period: the period of alarm_policy. For example: One minute : 1m.
        @param alarm_policy_name: the name of alarm_policy.
        """
        action = const.ACTION_CREATE_ALARM_POLICY
        valid_keys = ['alarm_policy_type', 'period', 'alarm_policy_name']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                             required_params=['alarm_policy_type', 'period']
                                             ):
            return None

        return self.conn.send_request(action, body)

    def modify_alarm_policy_attributes(self, alarm_policy,
                                       alarm_policy_name=None,
                                       period=None,
                                       description=None,
                                       **ignore):
        """ Modify alarm policy attributes.
        @param alarm_policy : the ID of alarm_policy.
        @param alarm_policy_name : the name of alarm_policy.
        @param period: the check period of alarm_policy.
        @param description: the description of alarm_policy.
        """
        action = const.ACTION_MODIFY_ALARM_POLICY_ATTRIBUTES
        valid_keys = ['alarm_policy', 'alarm_policy_name', 'period', 'description']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                             required_params=['alarm_policy']
                                             ):
            return None

        return self.conn.send_request(action, body)

    def delete_alarm_policies(self, alarm_policies,
                              **ignore):
        """ Delete one or more alarm policies.
        @param alarm_policies : the array of IDs of alarm policies.
        """
        action = const.ACTION_DELETE_ALARM_POLICIES
        valid_keys = ['alarm_policies']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                             required_params=['alarm_policies'],
                                             list_params=['alarm_policies']
                                             ):
            return None

        return self.conn.send_request(action, body)

    def describe_alarm_policy_rules(self, alarm_policy=None,
                                    alarm_policy_rules=None,
                                    offset=None,
                                    limit=None,
                                    **ignore):
        """ Describe alarm policy rules filtered by conditions.
        @param alarm_policy : the ID of alarm_policy.
        @param alarm_policy_rules : the array of IDs of alarm policy rules.
        @param offset: the starting offset of the returning results.
        @param limit: specify the number of the returning results.
        """
        action = const.ACTION_DESCRIBE_ALARM_POLICY_RULES
        valid_keys = ['alarm_policy', 'alarm_policy_rules', 'offset', 'limit']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                             integer_params=['offset', 'limit'],
                                             list_params=['alarm_policy_rules']
                                             ):
            return None

        return self.conn.send_request(action, body)

    def add_alarm_policy_rules(self, alarm_policy,
                               rules,
                               **ignore):
        """ Add rules to alarm policy.
        @param alarm_policy: the ID of the alarm policy whose rules you
                               want to add.
        @param rules: a list of rules you want to add.
        """
        action = const.ACTION_ADD_ALARM_POLICY_RULES
        valid_keys = ['alarm_policy', 'rules']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                             required_params=['alarm_policy', 'rules'],
                                             list_params=['rules']
                                             ):
            return None

        if not self.conn.req_checker.check_sg_rules(body.get('rules', [])):
            return None

        return self.conn.send_request(action, body)

    def modify_alarm_policy_rule_attributes(self, alarm_policy_rule,
                                            condition_type,
                                            thresholds=None,
                                            alarm_policy_rule_name=None,
                                            data_processor=None,
                                            consecutive_periods=None,
                                            **ignore):
        """ Modify alarm policy rule attributes.
        @param alarm_policy_rule: the ID of the alarm policy rule whose content you
                               want to update.
        @param condition_type: gt for greater than, lt for less than.
        @param thresholds: the thresholds of alarm.
        @param alarm_policy_rule_name: the name of the alarm policy rule.
        @param data_processor: raw for use the monitoring data raw value, percent only for IP bandwidth monitoring.
        @param consecutive_periods: during several consecutive inspection periods, the monitoring data reaches the alarm threshold,
                                    then will trigger the alarm behavior.
        """
        action = const.ACTION_MODIFY_ALARM_POLICY_RULE_ATTRIBUTES
        valid_keys = ['alarm_policy_rule', 'condition_type', 'thresholds',
                      'alarm_policy_rule_name', 'data_processor', 'consecutive_periods']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                             required_params=['alarm_policy_rule', 'condition_type']
                                             ):
            return None

        return self.conn.send_request(action, body)

    def delete_alarm_policy_rules(self, alarm_policy_rules,
                                  **ignore):
        """ Delete one or more alarm policy rules.
        @param alarm_policy_rules : the array of IDs of alarm policy rules.
        """
        action = const.ACTION_DELETE_ALARM_POLICY_RULES
        valid_keys = ['alarm_policy_rules']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                             required_params=['alarm_policy_rules'],
                                             list_params=['alarm_policy_rules']
                                             ):
            return None

        return self.conn.send_request(action, body)

    def describe_alarm_policy_actions(self, alarm_policy=None,
                                      alarm_policy_actions=None,
                                      offset=None,
                                      limit=None,
                                      **ignore):
        """ Describe alarm policy actions filtered by conditions.
        @param alarm_policy : the ID of alarm_policy.
        @param alarm_policy_actions : the array of IDs of alarm policy rules.
        @param offset: the starting offset of the returning results.
        @param limit: specify the number of the returning results.
        """
        action = const.ACTION_DESCRIBE_ALARM_POLICY_ACTIONS
        valid_keys = ['alarm_policy', 'alarm_policy_actions', 'offset', 'limit']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                             integer_params=['offset', 'limit'],
                                             list_params=['alarm_policy_actions']
                                             ):
            return None

        return self.conn.send_request(action, body)

    def add_alarm_policy_actions(self, alarm_policy,
                                 actions,
                                 **ignore):
        """ Add actions to alarm policy.
        @param alarm_policy: the ID of the alarm policy whose actions you
                               want to add.
        @param actions: a list of actions you want to add.
        """
        action = const.ACTION_ADD_ALARM_POLICY_ACTIONS
        valid_keys = ['alarm_policy', 'actions']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                             required_params=['alarm_policy', 'actions'],
                                             list_params=['actions']
                                             ):
            return None

        if not self.conn.req_checker.check_sg_rules(body.get('actions', [])):
            return None

        return self.conn.send_request(action, body)

    def modify_alarm_policy_action_attributes(self, alarm_policy_action,
                                              trigger_action=None,
                                              trigger_status=None,
                                              **ignore):
        """ Modify alarm policy action attributes.
        @param alarm_policy_action: the ID of the alarm policy action whose content you
                                    want to update.
        @param trigger_action: the ID of the trigger action.
        @param trigger_status: when the monitor alarm state becomes 'ok' or 'alarm', the message will be sent to this trigger list.
        """
        action = const.ACTION_MODIFY_ALARM_POLICY_ACTION_ATTRIBUTES
        valid_keys = ['alarm_policy_action', 'trigger_action', 'trigger_status']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                             required_params=['alarm_policy_action']
                                             ):
            return None

        return self.conn.send_request(action, body)

    def delete_alarm_policy_actions(self, alarm_policy_actions,
                                    **ignore):
        """ Delete one or more alarm policy actions.
        @param alarm_policy_actions : the array of IDs of alarm policy actions.
        """
        action = const.ACTION_DELETE_ALARM_POLICY_ACTIONS
        valid_keys = ['alarm_policy_actions']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                             required_params=['alarm_policy_actions'],
                                             list_params=['alarm_policy_actions']
                                             ):
            return None

        return self.conn.send_request(action, body)

    def associate_alarm_policy(self, alarm_policy,
                               resources,
                               related_resource=None,
                               **ignore):
        """ Associate an alarm_policy on one or more resources.
        @param alarm_policy: The id of alarm policy you want to associate with resources.
        @param resources: the id of resources you want to associate alarm policy.
        @param related_resource: when the network load balancer is bound,
                                 related_resource needs to specify a public network IP ID associated with this load balancer.
        """
        action = const.ACTION_ASSOCIATE_ALARM_POLICY
        valid_keys = ['alarm_policy', 'resources', 'related_resource']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                             required_params=['alarm_policy', 'resources'],
                                             list_params=['resources']
                                             ):
            return None

        return self.conn.send_request(action, body)

    def dissociate_alarm_policy(self, alarm_policy,
                                resources=None,
                                related_resource=None,
                                **ignore):
        """ Dissociate alarm policy.
        @param alarm_policy: The id of alarm policy you want to associate with resources.
        @param resources: the id of resources you want to associate alarm policy.
        @param related_resource: when the network load balancer is bound,
                                 related_resource needs to specify a public network IP ID associated with this load balancer.
        """
        action = const.ACTION_DISSOCIATE_ALARM_POLICY
        valid_keys = ['alarm_policy', 'resources', 'related_resource']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                             required_params=['alarm_policy'],
                                             list_params=['resources']
                                             ):
            return None

        return self.conn.send_request(action, body)

    def apply_alarm_policy(self, alarm_policy,
                           **ignore):
        """ Apply alarm policy.
        @param alarm_policy: the ID of alarm policy which would be applied effective.
        """
        action = const.ACTION_APPLY_ALARM_POLICY
        valid_keys = ['alarm_policy']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                             required_params=['alarm_policy']
                                             ):
            return None
        return self.conn.send_request(action, body)

    def describe_alarms(self, alarms=None,
                        policy=None,
                        status=None,
                        resource=None,
                        offset=None,
                        limit=None,
                        **ignore):
        """ Describe alarms filtered by condition.
        @param alarms: an array including IDs of the alarms you want to list.
        @param policy: the ID of alarm policy.
        @param status: ok stand for normal, alarm stand for alarming, insufficient stand for monitoring data cannot be collected.
        @param resource: The ID of resource which associated with the alarm.
        @param offset: the starting offset of the returning results.
        @param limit: specify the number of the returning results.
        """
        action = const.ACTION_DESCRIBE_ALARMS
        valid_keys = ['alarms', 'policy', 'status', 'resource', 'offset', 'limit']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                             integer_params=['offset', 'limit'],
                                             list_params=['alarms']
                                             ):
            return None

        return self.conn.send_request(action, body)

    def describe_alarm_history(self, alarm,
                               history_type=None,
                               offset=None,
                               limit=None,
                               **ignore):
        """ Describe alarm history filtered by condition.
        @param alarm: the ID of the resource alarm entity.
        @param history_type: the types including trigger_action, status_change, config_update.
        @param offset: the starting offset of the returning results.
        @param limit: specify the number of the returning results.
        """
        action = const.ACTION_DESCRIBE_ALARM_HISTORY
        valid_keys = ['alarm', 'history_type', 'offset', 'limit']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                             required_params=['alarm'],
                                             integer_params=['offset', 'limit']
                                             ):
            return None

        return self.conn.send_request(action, body)

