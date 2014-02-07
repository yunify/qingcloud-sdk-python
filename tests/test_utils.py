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

import time
import unittest
from qingcloud.misc.utils import get_utf8_value, filter_out_none, get_ts, parse_ts

class UtilsTestCase(unittest.TestCase):

    def test_get_utf8_value(self):
        self.assertEqual(get_utf8_value('utf-8'), 'utf-8')
        self.assertEqual(get_utf8_value(u'unicode'), 'unicode')
        self.assertEqual(get_utf8_value([1, 2]), '[1, 2]')

    def test_filter_out_none(self):
        data = {'a': 1, 'b': 2, 'c': None}
        self.assertEqual(filter_out_none(data), {'a': 1, 'b': 2})

        data = {'a': 1, 'b': 2, 'c': None}
        self.assertEqual(filter_out_none(data, keys=['a', 'c']), {'a': 1})

    def test_get_ts(self):
        ts = 1391832000
        ts = time.localtime(ts)
        expected = '2014-02-08T12:00:00Z'
        self.assertEqual(get_ts(ts), expected)
        self.assertTrue(isinstance(get_ts(), str))

    def test_parse_ts(self):
        ts = '2014-02-08T12:00:00Z'
        expected = 1391832000.0
        self.assertEqual(parse_ts(ts), expected)

        ts = '2014-02-08T12:00:00.000Z'
        expected = 1391832000.0
        self.assertEqual(parse_ts(ts), expected)
