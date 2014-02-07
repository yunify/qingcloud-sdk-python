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

import unittest

from qingcloud.iaas.errors import InvalidSecurityGroupRule
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
        self.assertRaises(InvalidSecurityGroupRule, SecurityGroupRuleFactory.create, 'unsupported', 0)

    def test_invalid_priority(self):
        self.assertRaises(InvalidSecurityGroupRule, SecurityGroupRuleFactory.create,
                SecurityGroupRuleFactory.PROTOCOL_UDP, -1)
        self.assertRaises(InvalidSecurityGroupRule, SecurityGroupRuleFactory.create,
                SecurityGroupRuleFactory.PROTOCOL_UDP, 101)
        self.assertRaises(InvalidSecurityGroupRule, SecurityGroupRuleFactory.create,
                SecurityGroupRuleFactory.PROTOCOL_UDP, '10')

        rule = SecurityGroupRuleFactory.create(SecurityGroupRuleFactory.PROTOCOL_UDP, 0)
        self.assertTrue(rule)
        rule = SecurityGroupRuleFactory.create(SecurityGroupRuleFactory.PROTOCOL_UDP, 100)
        self.assertTrue(rule)

    def test_create_multiple_rules_from_string(self):
        string = '''
        [{"direction": 0, "protocol": "tcp",
        "priority": 1, "action": "accept", "controller": "self",
        "security_group_rule_id": "sgr-sx5xrr5h", "val1": "1",
        "owner": "usr-F5iqdERj", "val2": "100", "val3": "",
        "security_group_rule_name": "", "security_group_id": "sg-0xegewrh"
        },

        {"direction": 0, "protocol": "gre",
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

    def test_create_single_rule_from_string(self):
        string = '''
        {"direction": 0, "protocol": "tcp",
        "priority": 1, "action": "accept", "controller": "self",
        "security_group_rule_id": "sgr-sx5xrr5h", "val1": "1",
        "owner": "usr-F5iqdERj", "val2": "100", "val3": "",
        "security_group_rule_name": "", "security_group_id": "sg-0xegewrh"
        }
        '''
        sgr = SecurityGroupRuleFactory.create_from_string(string)
        self.assertTrue(isinstance(sgr, _RuleForTCP))
