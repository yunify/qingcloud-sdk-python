import unittest

from qingcloud.iaas.sg_rule import SecurityGroupRuleFactory, _RuleForTCP, _RuleForGRE

class SecurityGroupRuleFactoryTestCase(unittest.TestCase):

    start_port = 10
    end_port = 200
    ip_network = '192.168.2.0/24'
    icmp_type = 8
    icmp_code = 0

    def test_tcp_rule_structure(self):
        rule = SecurityGroupRuleFactory.create(
                SecurityGroupRuleFactory.PROTOCOL_TCP, 0,
                security_group_rule_name='unittest',
                start_port=self.start_port, end_port=self.end_port,
                ip_network=self.ip_network)

        json_data = rule.to_json()
        self.assertEqual(json_data['val1'], self.start_port)
        self.assertEqual(json_data['val2'], self.end_port)
        self.assertEqual(json_data['val3'], self.ip_network)

    def test_udp_rule_structure(self):
        rule = SecurityGroupRuleFactory.create(
                SecurityGroupRuleFactory.PROTOCOL_UDP, 0,
                start_port=self.start_port, end_port=self.end_port,
                ip_network=self.ip_network)

        json_data = rule.to_json()
        self.assertEqual(json_data['val1'], self.start_port)
        self.assertEqual(json_data['val2'], self.end_port)
        self.assertEqual(json_data['val3'], self.ip_network)

    def test_icmp_rule_structure(self):
        rule = SecurityGroupRuleFactory.create(
                SecurityGroupRuleFactory.PROTOCOL_ICMP, 0,
                icmp_type=self.icmp_type, icmp_code=self.icmp_code,
                ip_network=self.ip_network)

        json_data = rule.to_json()
        self.assertEqual(json_data['val1'], self.icmp_type)
        self.assertEqual(json_data['val2'], self.icmp_code)
        self.assertEqual(json_data['val3'], self.ip_network)

    def test_gre_rule_structure(self):
        rule = SecurityGroupRuleFactory.create(
                SecurityGroupRuleFactory.PROTOCOL_GRE, 0, direction=1,
                action='drop', security_group_rule_name='unittest',
                ip_network=self.ip_network)

        json_data = rule.to_json()
        self.assertEqual(json_data['val3'], self.ip_network)

    def test_rule_with_existing_id(self):
        rule = SecurityGroupRuleFactory.create('gre', 0,
                security_group_rule_id='fakeid')

        json_data = rule.to_json()
        self.assertEqual(json_data['security_group_rule_id'], 'fakeid')

    def test_unsupported_protocol(self):
        rule = SecurityGroupRuleFactory.create('notsupport', 0)
        self.assertFalse(rule)

    def test_invalid_priority(self):
        rule = SecurityGroupRuleFactory.create(SecurityGroupRuleFactory.PROTOCOL_UDP, -1)
        self.assertFalse(rule)
        rule = SecurityGroupRuleFactory.create(SecurityGroupRuleFactory.PROTOCOL_UDP, 101)
        self.assertFalse(rule)
        rule = SecurityGroupRuleFactory.create(SecurityGroupRuleFactory.PROTOCOL_UDP, 'str')
        self.assertFalse(rule)

        rule = SecurityGroupRuleFactory.create(SecurityGroupRuleFactory.PROTOCOL_UDP, 0)
        self.assertTrue(rule)
        rule = SecurityGroupRuleFactory.create(SecurityGroupRuleFactory.PROTOCOL_UDP, 100)
        self.assertTrue(rule)

    def test_create_from_string(self):
        string = '''
        [{"direction": 0, "protocol": "tcp", "console_id": "qingcloud",
        "priority": 1, "action": "accept", "controller": "self",
        "security_group_rule_id": "sgr-sx5xrr5h", "val1": "1",
        "owner": "usr-F5iqdERj", "val2": "100", "val3": "",
        "security_group_rule_name": "", "security_group_id": "sg-0xegewrh"
        },

        {"direction": 0, "protocol": "gre", "console_id": "qingcloud",
        "priority": 1, "action": "accept", "controller": "self",
        "security_group_rule_id": "sgr-0cv8wkew", "val1": "",
        "owner": "usr-F5iqdERj", "val2": "", "val3": "",
        "security_group_rule_name": "", "security_group_id": "sg-0xegewrh"
        }]
        '''
        sgrs = SecurityGroupRuleFactory.create_from_string(string)
        self.assertEqual(len(sgrs), 2)
        self.assertTrue(isinstance(sgrs[0], _RuleForTCP))
        self.assertTrue(isinstance(sgrs[1], _RuleForGRE))
