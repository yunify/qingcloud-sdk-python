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

class ConsolidatorTestCase(unittest.TestCase):

    def test_check_integer(self):
        checker = RequestChecker()
        self.assertTrue(checker.check_integer(1))
        self.assertTrue(checker.check_integer('1'))
        self.assertTrue(checker.check_integer(False))
        self.assertFalse(checker.check_integer('s'))

    def test_check_integer_param(self):
        checker = RequestChecker()
        directive = {'name': 'donkey', 'age': '10'}
        self.assertTrue(checker.check_integer_params(directive, ['age']))
        self.assertRaises(InvalidParameterError,
                checker.check_integer_params, directive, ['name', 'age'])

    def test_check_required_param(self):
        checker = RequestChecker()
        directive = {'name': 'donkey', 'age': '10'}
        self.assertTrue(checker.check_required_params(directive, ['name', 'age']))
        self.assertRaises(InvalidParameterError,
                checker.check_required_params, directive, ['name', 'non-exist'])

    def test_check_list_param(self):
        checker = RequestChecker()
        directive = {'name': 'donkey', 'friends': ['horse', 'ox', 'sheep']}
        self.assertTrue(checker.check_list_params(directive, ['friends']))
        self.assertRaises(InvalidParameterError,
                checker.check_list_params, directive, ['name'])

    def test_check_sg_rules(self):
        checker = RequestChecker()
        rules = [{'protocol': 'tcp', 'priority': 2, 'val1': 22}]
        self.assertTrue(checker.check_sg_rules(rules))

        rules = [{'protocol': 'tcp'}]
        self.assertRaises(InvalidParameterError, checker.check_sg_rules,
                rules)

    def test_check_router_statics(self):
        checker = RequestChecker()
        statics = [{'static_type': 1, 'val1': '10', 'val2': '', 'val3': '20'}]
        self.assertTrue(checker.check_router_statics(statics))
        statics = [{'static_type': 2}]
        self.assertTrue(checker.check_router_statics(statics))
        statics = [{'static_type': 3, 'val1': '', 'val2': ''}]
        self.assertTrue(checker.check_router_statics(statics))

        invalid_statics = [{'static_type': 1}]
        self.assertRaises(InvalidParameterError, checker.check_router_statics,
                invalid_statics)
        invalid_statics = [{'static_type': 3}]
        self.assertRaises(InvalidParameterError, checker.check_router_statics,
                invalid_statics)


if '__main__' == __name__:
    unittest.main()
