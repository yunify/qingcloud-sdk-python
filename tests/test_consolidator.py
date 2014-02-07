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

from qingcloud.iaas.errors import InvalidParameterError
from qingcloud.iaas.consolidator import RequestChecker
from qingcloud.iaas.router_static import RouterStaticFactory

class ConsolidatorTestCase(unittest.TestCase):

    checker = RequestChecker()

    def test_check_params_with_valid_directive(self):
        directive = {}
        self.assertTrue(self.checker.check_params(directive))

    def test_check_params_with_invalid_directive(self):
        directive = 'invalid directive'
        self.assertRaises(InvalidParameterError, self.checker.check_params,
                directive)

    def test_is_integer(self):
        self.assertTrue(self.checker.is_integer(1))
        self.assertTrue(self.checker.is_integer('1'))
        self.assertTrue(self.checker.is_integer(False))
        self.assertFalse(self.checker.is_integer('s'))

    def test_is_integer_param(self):
        directive = {'name': 'donkey', 'age': '10'}
        self.checker.check_integer_params(directive, ['age'])
        self.assertRaises(InvalidParameterError,
                self.checker.check_integer_params, directive, ['name', 'age'])

    def test_check_required_param(self):
        directive = {'name': 'donkey', 'age': '10'}
        self.checker.check_required_params(directive, ['name', 'age'])
        self.assertRaises(InvalidParameterError,
                self.checker.check_required_params, directive, ['name', 'non-exist'])

    def test_check_list_param(self):
        directive = {'name': 'donkey', 'friends': ['horse', 'ox', 'sheep']}
        self.checker.check_list_params(directive, ['friends', 'notexist'])
        self.assertRaises(InvalidParameterError,
                self.checker.check_list_params, directive, ['name'])

    def test_check_sg_rules(self):
        rules = [{'protocol': 'tcp', 'priority': 2, 'val1': 22}]
        self.checker.check_sg_rules(rules)

        rules = [{'protocol': 'tcp'}]
        self.assertRaises(InvalidParameterError, self.checker.check_sg_rules,
                rules)

    def test_check_router_statics(self):
        statics = [
                {'static_type': RouterStaticFactory.TYPE_PORT_FORWARDING,
                    'val1': '10', 'val2': '', 'val3': '20'},
                {'static_type': RouterStaticFactory.TYPE_VPN, 'val1': 'pptp'},
                {'static_type': RouterStaticFactory.TYPE_TUNNEL, 'vxnet_id': '', 'val1': ''},
                {'static_type': RouterStaticFactory.TYPE_FILTERING, 'val1': ''},
                ]
        self.checker.check_router_statics(statics)

        invalid_statics = [{'static_type': RouterStaticFactory.TYPE_PORT_FORWARDING}]
        self.assertRaises(InvalidParameterError, self.checker.check_router_statics,
                invalid_statics)
        invalid_statics = [{'static_type': RouterStaticFactory.TYPE_VPN}]
        self.assertRaises(InvalidParameterError, self.checker.check_router_statics,
                invalid_statics)

    def test_check_lb_listener_port(self):
        valid_ports = [25, 80, 443] + range(1024, 65535)
        for port in valid_ports:
            self.checker.check_lb_listener_port(port)

        self.assertRaises(InvalidParameterError,
                self.checker.check_lb_listener_port, 20)
        self.assertRaises(InvalidParameterError,
                self.checker.check_lb_listener_port, 65536)
        self.assertRaises(InvalidParameterError,
                self.checker.check_lb_listener_port, 1023)

    def test_check_lb_listener_healthy_check_method(self):
        self.checker.check_lb_listener_healthy_check_method('tcp')
        self.checker.check_lb_listener_healthy_check_method('http|/url|host')

        self.assertRaises(InvalidParameterError,
                self.checker.check_lb_listener_healthy_check_method, 'invalid')
        self.assertRaises(InvalidParameterError,
                self.checker.check_lb_listener_healthy_check_method, 'http')
        self.assertRaises(InvalidParameterError,
                self.checker.check_lb_listener_healthy_check_method, 'http|url|host')

    def test_check_lb_listener_healthy_check_option(self):
        option = '2|5|2|2'
        self.checker.check_lb_listener_healthy_check_option(option)
        option = '60|300|10|10'
        self.checker.check_lb_listener_healthy_check_option(option)

        option = '1|5|2|2'
        self.assertRaises(InvalidParameterError,
                self.checker.check_lb_listener_healthy_check_option, option)
        option = '61|5|2|2'
        self.assertRaises(InvalidParameterError,
                self.checker.check_lb_listener_healthy_check_option, option)
        option = '2|4|2|2'
        self.assertRaises(InvalidParameterError,
                self.checker.check_lb_listener_healthy_check_option, option)
        option = '2|301|2|2'
        self.assertRaises(InvalidParameterError,
                self.checker.check_lb_listener_healthy_check_option, option)
        option = '2|5|1|2'
        self.assertRaises(InvalidParameterError,
                self.checker.check_lb_listener_healthy_check_option, option)
        option = '2|5|11|2'
        self.assertRaises(InvalidParameterError,
                self.checker.check_lb_listener_healthy_check_option, option)
        option = '2|5|2|1'
        self.assertRaises(InvalidParameterError,
                self.checker.check_lb_listener_healthy_check_option, option)
        option = '2|5|2|11'
        self.assertRaises(InvalidParameterError,
                self.checker.check_lb_listener_healthy_check_option, option)

    def test_check_lb_backend_port(self):
        valid_ports = range(1, 65535)
        for port in valid_ports:
            self.checker.check_lb_backend_port(port)

        self.assertRaises(InvalidParameterError,
                self.checker.check_lb_backend_port, 0)
        self.assertRaises(InvalidParameterError,
                self.checker.check_lb_backend_port, 65536)

    def test_check_lb_backend_weight(self):
        valid_weights = range(1, 100)
        for weight in valid_weights:
            self.checker.check_lb_backend_weight(weight)

        self.assertRaises(InvalidParameterError,
                self.checker.check_lb_backend_weight, 0)
        self.assertRaises(InvalidParameterError,
                self.checker.check_lb_backend_weight, 101)

    def test_check_lb_listeners(self):
        listeners = [{
            'listener_protocol': 'tcp',
            'listener_port': '80',
            'backend_protocol': 'tcp',
            'balance_mode': 'roundrobin',
            'healthy_check_method': 'tcp',
            'healthy_check_option': '10|5|5|5',
            }]
        self.checker.check_lb_listeners(listeners)

    def test_check_lb_listeners_when_missing_param(self):
        listeners = [{
            'listener_port': '80',
            'backend_protocol': 'tcp',
            'balance_mode': 'roundrobin',
            'healthy_check_method': 'tcp',
            'healthy_check_option': '10|5|5|5',
            }]
        self.assertRaises(InvalidParameterError,
                self.checker.check_lb_listeners, listeners)

    def test_check_lb_listeners_with_invalid_port(self):
        listeners = [{
            'listener_protocol': 'tcp',
            'listener_port': '808',
            'backend_protocol': 'tcp',
            'balance_mode': 'roundrobin',
            'healthy_check_method': 'tcp',
            'healthy_check_option': '10|5|5|5',
            }]
        self.assertRaises(InvalidParameterError,
                self.checker.check_lb_listeners, listeners)

    def test_check_lb_listeners_with_invalid_method(self):
        listeners = [{
            'listener_protocol': 'tcp',
            'listener_port': '80',
            'backend_protocol': 'tcp',
            'balance_mode': 'roundrobin',
            'healthy_check_method': 'http',
            'healthy_check_option': '10|5|5|5',
            }]
        self.assertRaises(InvalidParameterError,
                self.checker.check_lb_listeners, listeners)

    def test_check_lb_listeners_with_invalid_option(self):
        listeners = [{
            'listener_protocol': 'tcp',
            'listener_port': '80',
            'backend_protocol': 'tcp',
            'balance_mode': 'roundrobin',
            'healthy_check_method': 'tcp',
            'healthy_check_option': '100|5|5|5', # invalid interval
            }]
        self.assertRaises(InvalidParameterError,
                self.checker.check_lb_listeners, listeners)

    def test_check_lb_backends(self):
        backends = [{
            'resource_id': 'i-1234abcd',
            'port': '80',
            }]
        self.checker.check_lb_backends(backends)

    def test_check_lb_backends_when_missing_param(self):
        backends = [{
            'resource_id': 'i-1234abcd',
            }]
        self.assertRaises(InvalidParameterError,
                self.checker.check_lb_backends, backends)

    def test_check_lb_backends_with_invalid_port(self):
        backends = [{
            'resource_id': 'i-1234abcd',
            'port': '65536',
            }]
        self.assertRaises(InvalidParameterError,
                self.checker.check_lb_backends, backends)
