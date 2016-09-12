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
from mock import Mock
from qingcloud.misc.utils import (get_utf8_value, filter_out_none, get_ts,
                                  parse_ts, local_ts, base64_url_encode, base64_url_decode,
                                  wait_job)


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

    def test_local_ts(self):
        ts = '2014-02-08T12:00:00Z'
        expected = 1391860800.0
        self.assertEqual(local_ts(ts), expected)

        ts = '2014-02-08T12:00:00.000Z'
        expected = 1391860800.0
        self.assertEqual(local_ts(ts), expected)

    def test_base64_url_encode(self):
        self.assertEqual("c29tZSBzdHJpbmcgdG8gZW5jb2RlIA",
                         base64_url_encode("some string to encode "))

    def test_base64_url_decode(self):
        self.assertEqual("some string to encode ", base64_url_decode(
            "c29tZSBzdHJpbmcgdG8gZW5jb2RlIA"))

    def test_wait_job(self):
        job_id = 'job-id'
        conn = Mock()
        # timeout
        conn.describe_jobs.return_value = {'job_set': [{'status': 'working'}]}
        self.assertFalse(wait_job(conn, job_id, 4))
        self.assertEqual(conn.describe_jobs.call_count, 2)
        # call api failed
        conn.describe_jobs.return_value = None
        self.assertFalse(wait_job(conn, job_id, 2))
        # job complete
        conn.describe_jobs.return_value = {'job_set': [{'status': 'failed'}]}
        self.assertTrue(wait_job(conn, job_id))
        conn.describe_jobs.return_value = {
            'job_set': [{'status': 'successful'}]}
        self.assertTrue(wait_job(conn, job_id))
        conn.describe_jobs.return_value = {
            'job_set': [{'status': 'done with failure'}]}
        self.assertTrue(wait_job(conn, job_id))
