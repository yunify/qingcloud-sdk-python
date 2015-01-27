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
from qingcloud.conn.auth import AppSignatureAuthHandler
from qingcloud.misc.utils import base64_url_decode
from qingcloud.misc.json_tool import json_load

APP_ID = "app-zjd5o6ae"
APP_KEY = "CXikZWDoRkttCO8Y7XXhRTtMxiUFSr7ZePO1tGQP"
class AppAuthTestCase(unittest.TestCase):

    def setUp(self):
        super(AppAuthTestCase, self).setUp()
        self.app = AppSignatureAuthHandler(APP_ID, APP_KEY)
        
    def test_sign_string(self):
        self.assertEqual("-xmepZZrlRW9dOgO3KA9MY8rgOjLvfSedNEPXsxrpcQ", 
                         self.app.sign_string("some string to sign"))

    def test_check_access(self):
        self.assertTrue(self.app.check_access(
                          "some string to sign", 
                          "-xmepZZrlRW9dOgO3KA9MY8rgOjLvfSedNEPXsxrpcQ"))
        self.assertFalse(self.app.check_access(
                          "some string to sign", 
                          "-xmepZZrlRW9dOgO3KA9MY8rgOjLvfSedNEPXsxrpcx"))

    def test_create_auth(self):
        
        access_info = {"user_id": "user-id1", 
                       "access_token": "1234567",
                       "action": "view_app",
                       "zone": "beta",
                       "expires": '2014-02-08T12:00:00.000Z'}
        auth_info = self.app.create_auth(access_info)
        self.assertTrue('eyJhY2Nlc3NfdG9rZW4iOiIxMjM0NTY3IiwiYWN0aW9uIjoidmll\
d19hcHAiLCJleHBpcmVzIjoiMjAxNC0wMi0wOFQxMjowMDowMC4wMDBaIiwidXNlcl9pZCI6InVzZ\
XItaWQxIiwiem9uZSI6ImJldGEifQ', auth_info['payload'])

        self.assertTrue('FTkIbXebTMpRdHnjL7f1LSunUoXwZKXMCqHjXTh3qP4',
                        auth_info['signature'])

        self.assertTrue(self.app.check_access(auth_info['payload'], 
                                              auth_info['signature']))

        self.assertEqual(access_info, 
                         json_load(base64_url_decode(auth_info['payload'])))