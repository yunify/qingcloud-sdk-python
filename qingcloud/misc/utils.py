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
import base64

def get_utf8_value(value):
    if not isinstance(value, (str, unicode)):
        value = str(value)
    if isinstance(value, unicode):
        return value.encode('utf-8')
    else:
        return value

def filter_out_none(dictionary, keys=None):
    """ Filter out items whose value is None.
        If `keys` specified, only return non-None items with matched key.
    """
    ret = {}
    if keys is None:
        keys = []
    for key, value in dictionary.items():
        if value is None or (keys and key not in keys):
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
    ''' read file content '''
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
