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

from qingcloud.iaas.lb_backend import LoadBalancerBackend

class LoadBalancerBackendTestCase(unittest.TestCase):

    def test_init_backend(self):
        port = 443
        weight = 12
        backend = LoadBalancerBackend('i-test1234', port, weight)
        self.assertEqual(backend.to_json()['port'], port)
        self.assertEqual(backend.to_json()['weight'], weight)

    def test_create_multiple_backends_from_string(self):
        string = '''
        [{"status":"down","loadbalancer_backend_id":"lbb-rruzir3s","weight":1,
        "resource_id":"i-1234abcd","loadbalancer_backend_name":"",
        "port":23,"controller":"self", "create_time":"2014-02-03T17:12:03Z",
        "owner":"usr-1234abcd", "loadbalancer_listener_id":"lbl-1234abcd",
        "loadbalancer_id":"lb-1234abcd"},
        {"status":"down","loadbalancer_backend_id":"lbb-vz51avzj","weight":1,
        "resource_id":"i-1234abcd","loadbalancer_backend_name":"",
        "port":3,"controller":"self","create_time":"2014-02-03T17:12:07Z",
        "owner":"usr-1234abcd","loadbalancer_listener_id":"lbl-1234abcd",
        "loadbalancer_id":"lb-1234abcd"}]
        '''
        backends = LoadBalancerBackend.create_from_string(string)
        self.assertEqual(len(backends), 2)

    def test_create_single_backend_from_string(self):
        string = '''
        {"status":"down","loadbalancer_backend_id":"lbb-rruzir3s","weight":1,
        "resource_id":"i-1234abcd","loadbalancer_backend_name":"",
        "port":23,"controller":"self", "create_time":"2014-02-03T17:12:03Z",
        "owner":"usr-1234abcd", "loadbalancer_listener_id":"lbl-1234abcd",
        "loadbalancer_id":"lb-1234abcd"}
        '''
        backend = LoadBalancerBackend.create_from_string(string)
        self.assertTrue(isinstance(backend, LoadBalancerBackend))
