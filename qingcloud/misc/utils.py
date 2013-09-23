# coding: utf-8

import time
import os
import stat

def save_private_key(file_name, private_key):
    """ save ssh private key """
    if not save_file(file_name, private_key):
        return False
    os.chmod(file_name, stat.S_IREAD + stat.S_IWRITE)
    return True

def save_file(file_name, content):
    with open("%s" % file_name, "w") as f:
        f.write("%s" % content)

def get_utf8_value(value):
    if not isinstance(value, str) and not isinstance(value, unicode):
        value = str(value)
    if isinstance(value, unicode):
        return value.encode('utf-8')
    else:
        return value

def filter_out_none(dictionary, keys=None):
    """
    Filter out items whose value is None.
    If `keys` specified, only return non-None and key matched items.
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
    """
    Get formatted time
    """
    if not ts:
        ts = time.gmtime()
    return time.strftime(ISO8601, ts)

def parse_ts(ts):
    """
    Return as timestamp
    """
    ts = ts.strip()
    try:
        ts_s = time.strptime(ts, ISO8601)
        return time.mktime(ts_s)
    except ValueError:
        ts_s = time.strptime(ts, ISO8601_MS)
        return time.mktime(ts_s)

def get_expired_ts(ts, time_out):
    ts_expired_s = parse_ts(ts) + time_out
    ts_expired = time.localtime(ts_expired_s)
    return get_ts(ts_expired)
