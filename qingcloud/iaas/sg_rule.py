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

import json

from qingcloud.iaas.errors import InvalidSecurityGroupRule


class SecurityGroupRuleFactory(object):
    """ Factory for security group rule

        Example:
            conn = qingcloud.iaas.connect_to_zone(....)
            security_group_id = 'sg-xxxxx'

            # Add security group rule
            ping_rule = SecurityGroupRuleFactory.create(
                protocol = SecurityGroupRuleFactory.PROTOCOL_ICMP,
                priority = 1,
                direction = SecurityGroupRuleFactory.INBOUND,
                action = 'accept',
                security_group_rule_name = 'ECHO',
                val1 = '8',
                val2 = '0'
                )
            ping_rule = ping_rule.to_json()
            conn.add_security_group_rules(security_group_id, ping_rule)

            # Modify security group rule
            rules = conn.describe_security_group_rules(security_group_id)
            assert(rules['security_group_rule_set'])
            rule = rules['security_group_rule_set'][0]
            conn.modify_security_group_rule_attributes(
                rule['security_group_rule_id'],
                priority=5,
                )

    """

    PROTOCOL_TCP = 'tcp'
    PROTOCOL_UDP = 'udp'
    PROTOCOL_ICMP = 'icmp'
    PROTOCOL_GRE = 'gre'

    INBOUND = 0
    OUTBOUND = 1

    @classmethod
    def create(cls, protocol, priority, direction=INBOUND, action='accept',
               security_group_rule_id='', security_group_rule_name='',
               **kw):
        """ Create security group rule.
        @param protocol: support protocol.
        @param priority: should be between 0 and 100.
        """
        if protocol not in RULE_MAPPER:
            raise InvalidSecurityGroupRule("invalid protocol[%s]" % protocol)
        if not isinstance(priority, int) or priority < 0 or priority > 100:
            raise InvalidSecurityGroupRule("invalid priority[%s]" % priority)

        clazz = RULE_MAPPER[protocol]
        inst = clazz(**kw)
        inst.priority = priority
        inst.direction = direction
        inst.action = action
        inst.security_group_rule_id = security_group_rule_id
        inst.security_group_rule_name = security_group_rule_name
        return inst

    @classmethod
    def create_from_string(cls, string):
        """ Create security group rule from json formatted string.
        """
        data = json.loads(string)
        if isinstance(data, dict):
            return cls.create(**data)
        if isinstance(data, list):
            return [cls.create(**item) for item in data]


class _SecurityGroupRule(object):
    """ _SecurityGroupRule is used to define a rule in security group.
    """

    security_group_rule_id = None
    security_group_rule_name = None
    priority = None
    direction = None
    action = None
    protocol = None

    def extra_props(self):
        raise NotImplementedError

    def to_json(self):
        """ Format SecurityGroupRule to JSON string
            NOTE: call this method when passing SecurityGroupRule instance as API parameter
        """
        props = {
            'security_group_rule_id': self.security_group_rule_id,
            'security_group_rule_name': self.security_group_rule_name,
            'priority': self.priority,
            'direction': self.direction,
            'action': self.action,
            'protocol': self.protocol,
        }
        props.update(self.extra_props())
        return props

    def __repr__(self):
        return '<%s>%s' % (self.__class__.__name__, self.to_json())


class _RuleForTCP(_SecurityGroupRule):

    protocol = SecurityGroupRuleFactory.PROTOCOL_TCP

    def __init__(self, start_port='', end_port='', ip_network='', **kw):
        super(_RuleForTCP, self).__init__()
        self.start_port = start_port if start_port != '' else kw.get(
            'val1', '')
        self.end_port = end_port if end_port != '' else kw.get('val2', '')
        self.ip_network = ip_network if ip_network != '' else kw.get(
            'val3', '')

    def extra_props(self):
        return {
            'val1': self.start_port,
            'val2': self.end_port,
            'val3': self.ip_network,
        }


class _RuleForUDP(_SecurityGroupRule):

    protocol = SecurityGroupRuleFactory.PROTOCOL_UDP

    def __init__(self, start_port='', end_port='', ip_network='', **kw):
        super(_RuleForUDP, self).__init__()
        self.start_port = start_port if start_port != '' else kw.get(
            'val1', '')
        self.end_port = end_port if end_port != '' else kw.get('val2', '')
        self.ip_network = ip_network if ip_network != '' else kw.get(
            'val3', '')

    def extra_props(self):
        return {
            'val1': self.start_port,
            'val2': self.end_port,
            'val3': self.ip_network,
        }


class _RuleForICMP(_SecurityGroupRule):

    protocol = SecurityGroupRuleFactory.PROTOCOL_ICMP

    def __init__(self, icmp_type='', icmp_code='', ip_network='', **kw):
        super(_RuleForICMP, self).__init__()
        self.icmp_type = icmp_type if icmp_type != '' else kw.get('val1', '')
        self.icmp_code = icmp_code if icmp_code != '' else kw.get('val2', '')
        self.ip_network = ip_network if ip_network != '' else kw.get(
            'val3', '')

    def extra_props(self):
        return {
            'val1': self.icmp_type,
            'val2': self.icmp_code,
            'val3': self.ip_network,
        }


class _RuleForGRE(_SecurityGroupRule):

    protocol = SecurityGroupRuleFactory.PROTOCOL_GRE

    def __init__(self, ip_network='', **kw):
        super(_RuleForGRE, self).__init__()
        self.ip_network = ip_network or kw.get('val3', '')

    def extra_props(self):
        return {
            'val3': self.ip_network,
        }

RULE_MAPPER = {
    SecurityGroupRuleFactory.PROTOCOL_TCP: _RuleForTCP,
    SecurityGroupRuleFactory.PROTOCOL_UDP: _RuleForUDP,
    SecurityGroupRuleFactory.PROTOCOL_ICMP: _RuleForICMP,
    SecurityGroupRuleFactory.PROTOCOL_GRE: _RuleForGRE,
}
