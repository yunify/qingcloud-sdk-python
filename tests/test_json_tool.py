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
from qingcloud.misc.json_tool import json_dump, json_load

class JsonToolTestCase(unittest.TestCase):

    def test_json_dump_dict(self):
        obj = {'1':1, 'str': 'string', 'none': None}
        expected = '{"1":1,"none":null,"str":"string"}'
        self.assertEqual(json_dump(obj), expected)

    def test_json_dump_invalid_obj(self):
        obj = {unittest: 'invalid key'}
        expected = None
        self.assertEqual(json_dump(obj), expected)

    def test_json_dump_list(self):
        obj = [1, 4, '3']
        expected = '[1,4,"3"]'
        self.assertEqual(json_dump(obj), expected)

    def test_json_load_list(self):
        string = '{"int":1,"none":null,"str":"string"}'
        expected = {'int':1, 'str': 'string', 'none': None}
        self.assertEqual(json_load(string), expected)

    def test_json_load_string(self):
        string = '{"int":1,"none":null,"str":"string"}'
        expected = {'int':1, 'str': 'string', 'none': None}
        self.assertEqual(json_load(string), expected)

    def test_json_load_invalid_string(self):
        string = '{"int":1,:null,"str":"string"}'
        expected = None
        self.assertEqual(json_load(string), expected)
