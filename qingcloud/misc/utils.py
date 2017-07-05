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

import sys
import time
import base64


def get_utf8_value(value):
    if sys.version < "3":
        if isinstance(value, unicode):
            return value.encode('utf-8')
        if not isinstance(value, str):
            value = str(value)
        return value
    else:
        return str(value)


def filter_out_none(dictionary, keys=None):
    """ Filter out items whose value is None.
        If `keys` specified, only return non-None items with matched key.
    """
    ret = {}
    if keys is None:
        keys = []
    for key, value in dictionary.items():
        if value is None or key not in keys:
            continue
        ret[key] = value
    return ret


ISO8601 = '%Y-%m-%dT%H:%M:%SZ'
ISO8601_MS = '%Y-%m-%dT%H:%M:%S.%fZ'


def get_ts(ts=None):
    """ Get formatted time
    """
    if not ts:
        ts = time.gmtime()
    return time.strftime(ISO8601, ts)


def parse_ts(ts):
    """ Return as timestamp
    """
    ts = ts.strip()
    try:
        ts_s = time.strptime(ts, ISO8601)
        return time.mktime(ts_s)
    except ValueError:
        try:
            ts_s = time.strptime(ts, ISO8601_MS)
            return time.mktime(ts_s)
        except ValueError:
            return 0


def local_ts(utc_ts):
    ts = parse_ts(utc_ts)
    if ts:
        return ts - time.timezone
    else:
        return 0


def read_file(file_name, mode='r'):
    """ read file content
    """
    try:
        with open(file_name, mode) as f:
            content = f.read()
    except Exception:
        return None
    return content


def encode_base64(content):
    try:
        base64str = base64.standard_b64encode(content)
        return base64str
    except Exception:
        return ''


def decode_base64(base64str):
    try:
        decodestr = base64.standard_b64decode(base64str)
        return decodestr
    except Exception:
        return ''


def base64_url_decode(inp):
    if sys.version > "3":
        if isinstance(inp, bytes):
            inp = inp.decode()
        return base64.urlsafe_b64decode(inp + '=' * (4 - len(inp) % 4)).decode()
    else:
        return base64.urlsafe_b64decode(str(inp + '=' * (4 - len(inp) % 4)))


def base64_url_encode(inp):
    if sys.version > "3":
        if isinstance(inp, str):
            inp = inp.encode()
        return bytes.decode(base64.urlsafe_b64encode(inp).rstrip(b'='))
    else:
        return base64.urlsafe_b64encode(str(inp)).rstrip(b'=')


def wait_job(conn, job_id, timeout=60):
    """ waiting for job complete (success or fail) until timeout
    """
    def describe_job(job_id):
        ret = conn.describe_jobs([job_id])
        if not ret or not ret.get('job_set'):
            return None
        return ret['job_set'][0]

    deadline = time.time() + timeout
    while time.time() <= deadline:
        time.sleep(2)
        job = describe_job(job_id)
        if not job:
            continue
        if job['status'] not in ('pending', 'working'):
            if conn.debug:
                print('job is %s: %s' % (job['status'], job_id))
                sys.stdout.flush()
            return True

    if conn.debug:
        print('timeout for job: %s' % job_id)
        sys.stdout.flush()
    return False
