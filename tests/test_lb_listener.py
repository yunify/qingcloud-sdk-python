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

from qingcloud.iaas.lb_listener import LoadBalancerListener


class LoadBalancerListenerTestCase(unittest.TestCase):

    def test_init_instance(self):
        port = 80
        protocol = 'http'
        listener = LoadBalancerListener(port, listener_protocol=protocol,
                                        backend_protocol=protocol)
        json = listener.to_json()
        self.assertEqual(json['listener_port'], port)
        self.assertEqual(json['listener_protocol'], protocol)

    def test_init_forwardfor(self):
        port = 80
        protocol = 'http'
        listener = LoadBalancerListener(port, listener_protocol=protocol,
                                        backend_protocol=protocol, forwardfor=1)
        json = listener.to_json()
        self.assertEqual(json['forwardfor'], 1)

        listener = LoadBalancerListener(port, listener_protocol=protocol,
                                        backend_protocol=protocol, headers=['QC-LBIP'])
        json = listener.to_json()
        self.assertEqual(json['forwardfor'], 4)

        listener = LoadBalancerListener(port, listener_protocol=protocol,
                                        backend_protocol=protocol, forwardfor=1, headers=['QC-LBIP'])
        json = listener.to_json()
        self.assertEqual(json['forwardfor'], 1)

    def test_get_forwardfor(self):
        headers = []
        self.assertEqual(LoadBalancerListener.get_forwardfor(headers), 0)
        headers = ['wrong_header']
        self.assertEqual(LoadBalancerListener.get_forwardfor(headers), 0)
        headers = ['X-FORWARD-FOR']
        self.assertEqual(LoadBalancerListener.get_forwardfor(headers), 1)
        headers = ['QC-LBID']
        self.assertEqual(LoadBalancerListener.get_forwardfor(headers), 2)
        headers = ['QC-LBIP']
        self.assertEqual(LoadBalancerListener.get_forwardfor(headers), 4)
        headers = ['X-FORWARD-FOR', 'QC-LBID']
        self.assertEqual(LoadBalancerListener.get_forwardfor(headers), 3)
        headers = ['X-FORWARD-FOR', 'QC-LBIP', 'QC-LBID']
        self.assertEqual(LoadBalancerListener.get_forwardfor(headers), 7)

    def test_create_multiple_listeners_from_string(self):
        string = '''
        [{"forwardfor":0,"loadbalancer_listener_id":"lbl-1234abcd",
        "balance_mode":"roundrobin","listener_protocol":"tcp",
        "backend_protocol":"tcp","healthy_check_method":"tcp",
        "session_sticky":"","loadbalancer_listener_name":"demo",
        "controller":"self","backends":[],"create_time":"2014-02-02T16:51:25Z",
        "healthy_check_option":"10|5|2|5","owner":"usr-1234abcd",
        "console_id":"qingcloud","loadbalancer_id":"lb-1234abcd",
        "listener_port":443},
        {"forwardfor":0,
        "loadbalancer_listener_id":"lbl-1234abcd","balance_mode":"roundrobin",
        "listener_protocol":"http","backend_protocol":"http",
        "healthy_check_method":"tcp","session_sticky":"",
        "loadbalancer_listener_name":"demo","controller":"self",
        "backends":[],"create_time":"2014-02-02T16:51:19Z",
        "healthy_check_option":"10|5|2|5","owner":"usr-1234abcd",
        "console_id":"qingcloud","loadbalancer_id":"lb-1234abcd",
        "listener_port":80}]
        '''
        listeners = LoadBalancerListener.create_from_string(string)
        self.assertEqual(len(listeners), 2)

    def test_create_single_listener_from_string(self):
        string = '''
        {"forwardfor":0,"loadbalancer_listener_id":"lbl-1234abcd",
        "balance_mode":"roundrobin","listener_protocol":"tcp",
        "backend_protocol":"tcp","healthy_check_method":"tcp",
        "session_sticky":"","loadbalancer_listener_name":"demo",
        "controller":"self","backends":[],"create_time":"2014-02-02T16:51:25Z",
        "healthy_check_option":"10|5|2|5","owner":"usr-1234abcd",
        "console_id":"qingcloud","loadbalancer_id":"lb-1234abcd",
        "listener_port":443}
        '''
        listener = LoadBalancerListener.create_from_string(string)
        self.assertTrue(isinstance(listener, LoadBalancerListener))
