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

APP_ID = "app-zjd5o6ae"
APP_KEY = "CXikZWDoRkttCO8Y7XXhRTtMxiUFSr7ZePO1tGQP"
PAYLOAD = 'eyJhY2Nlc3NfdG9rZW4iOiIxMjM0NTY3IiwiYWN0aW9uIjoid\
mlld19hcHAiLCJleHBpcmVzIjoiMjAxNC0wMi0wOFQxMjowMDowMC4wMDBaIi\
wibGFuZyI6InpoX0NOIiwidXNlcl9pZCI6InVzZXItaWQxIiwiem9uZSI6ImJldGEifQ'
SIGNATURE = 'bwt9NTDknRpa3vu-gh_2u2qpKnlMBkrar8TeJwp6KG0'

ACCESS_INFO = {"user_id": "user-id1",
               "access_token": "1234567",
               "action": "view_app",
               "zone": "beta",
               "expires": "2014-02-08T12:00:00.000Z",
               "lang": "zh_CN"}


class AppAuthTestCase(unittest.TestCase):

    def setUp(self):
        super(AppAuthTestCase, self).setUp()
        self.app = AppSignatureAuthHandler(APP_ID, APP_KEY)

    def test_sign_string(self):
        self.assertEqual("-xmepZZrlRW9dOgO3KA9MY8rgOjLvfSedNEPXsxrpcQ",
                         self.app.sign_string("some string to sign"))

    def test_extract_payload(self):
        extracted_payload = self.app.extract_payload(
            PAYLOAD,
            SIGNATURE)
        self.assertEqual(ACCESS_INFO, extracted_payload)

        self.assertIsNone(self.app.extract_payload(
                          PAYLOAD,
                          "-xmepZZrlRW9dOgO3KA9MY8rgOjLvfSedNEPXsxrpcx"))

    def test_create_auth(self):

        auth_info = self.app.create_auth(ACCESS_INFO)
        self.assertEqual(PAYLOAD, auth_info['payload'])

        self.assertEqual(SIGNATURE,
                         auth_info['signature'])

    def test_payload(self):
        app = AppSignatureAuthHandler(
            "app-b9p6qxqj", "jimLjavU3uQAGxrv6FkeJKd58ieRiuWeVtilFl7V")
        extracted_payload = app.extract_payload("eyJsYW5nIjoiemgtY24iLCJ1c2VyX2lkIjoidXNyLWluZWE5dzdaIiwiem9uZSI6ImFsbGlub25lIiwiYWNjZXNzX3Rva2VuIjoiYWhacEhCOFZ2aUJ1bXB0YTBHeTZGMUFDUFNtbkZNeGsiLCJleHBpcmVzIjoiMjAxNS0wMS0yOFQwOTozNTozNFoiLCJhY3Rpb24iOiJ2aWV3X2FwcCJ9",
                                                "3k-0pqvAjf5BvFtssV3_2t_KBkesEpYEmesv3O5sJeI")

        self.assertIsNotNone(extracted_payload)
