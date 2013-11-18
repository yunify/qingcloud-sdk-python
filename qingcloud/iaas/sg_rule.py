# coding: utf-8

import json

class SecurityGroupRuleFactory(object):

    PROTOCOL_TCP = 'tcp'
    PROTOCOL_UDP = 'udp'
    PROTOCOL_ICMP = 'icmp'
    PROTOCOL_GRE = 'gre'

    @classmethod
    def create(cls, protocol, priority, direction=0, action='accept',
            security_group_rule_id='', security_group_rule_name='',
            **kw):
        clazz = RULE_MAPPER.get(protocol)
        if not clazz:
            return None
        if not isinstance(priority, int) or priority < 0 or priority > 100:
            return None

        inst = clazz(**kw)
        inst.priority = priority
        inst.direction = direction
        inst.action = action
        inst.security_group_rule_id = security_group_rule_id
        inst.security_group_rule_name = security_group_rule_name
        return inst

    @classmethod
    def create_from_string(cls, string):
        if not isinstance(string, basestring):
            return string
        data = json.loads(string)
        if isinstance(data, dict):
            return cls.create(**data)
        if isinstance(data, list):
            return [cls.create(**item) for item in data]


class _SecurityGroupRule(object):
    """
    _SecurityGroupRule is used to define a rule in security group.
    """

    security_group_rule_id = None
    security_group_rule_name = None
    priority = None
    direction = None # 0: inbound, 1: outbound
    action = None
    protocol = None

    def extra_props(self):
        raise NotImplementedError

    def to_json(self):
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
        self.start_port = start_port if start_port != '' else kw.get('val1', '')
        self.end_port = end_port if end_port != '' else kw.get('val2', '')
        self.ip_network = ip_network if ip_network != '' else kw.get('val3', '')

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
        self.start_port = start_port if start_port != '' else kw.get('val1', '')
        self.end_port = end_port if end_port != '' else kw.get('val2', '')
        self.ip_network = ip_network if ip_network != '' else kw.get('val3', '')

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
        self.ip_network = ip_network if ip_network != '' else kw.get('val3', '')

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
