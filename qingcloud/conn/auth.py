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

import base64
import hmac
import urllib
from hashlib import sha1, sha256

from qingcloud.misc.utils import get_utf8_value, get_ts
from qingcloud.misc.json_tool import json_dump


class HmacKeys(object):
    """
    Key based Auth handler helper.
    """
    host = None
    qy_access_key_id = None
    qy_secret_access_key = None
    _hmac = None
    _hmac_256 = None

    def __init__(self, host, qy_access_key_id, qy_secret_access_key):
        self.host = host
        self.update_provider(qy_access_key_id, qy_secret_access_key)

    def update_provider(self, qy_access_key_id, qy_secret_access_key):
        self.qy_access_key_id = qy_access_key_id
        self.qy_secret_access_key = qy_secret_access_key
        self._hmac = hmac.new(self.qy_secret_access_key, digestmod=sha1)
        if sha256:
            self._hmac_256 = hmac.new(self.qy_secret_access_key,
                                      digestmod=sha256)
        else:
            self._hmac_256 = None

    def algorithm(self):
        if self._hmac_256:
            return 'HmacSHA256'
        else:
            return 'HmacSHA1'

    def sign_string(self, string_to_sign):
        if self._hmac_256:
            _hmac = self._hmac_256.copy()
        else:
            _hmac = self._hmac.copy()
        _hmac.update(string_to_sign)
        return base64.b64encode(_hmac.digest()).strip()

class QuerySignatureAuthHandler(HmacKeys):
    """
    Provides Query Signature Authentication.
    """

    SignatureVersion = 1
    APIVersion = 1

    def _calc_signature(self, params, verb, path):
        '''
        calc signature for request
        '''
        string_to_sign = '%s\n%s\n' % (verb, path)
        params['signature_method'] = self.algorithm()
        keys = sorted(params.keys())
        pairs = []
        for key in keys:
            val = get_utf8_value(params[key])
            pairs.append(urllib.quote(key, safe='') + '=' +
                         urllib.quote(val, safe='-_~'))
        qs = '&'.join(pairs)
        string_to_sign += qs
        #print "string to sign:[%s]" % string_to_sign
        b64 = self.sign_string(string_to_sign)
        return (qs, b64)

    def add_auth(self, req, **kwargs):
        '''
        add authorize information for request
        '''
        req.params['access_key_id'] = self.qy_access_key_id
        req.params['signature_version'] = self.SignatureVersion
        req.params['version'] = self.APIVersion
        time_stamp = get_ts()
        req.params['time_stamp'] = time_stamp
        #print json_dump(req.params, indent=2)
        qs, signature = self._calc_signature(req.params, req.method,
                                             req.auth_path)
        #print 'query_string: %s Signature: %s' % (qs, signature)
        if req.method == 'POST':
            # req and retried req should not have signature
            params = req.params.copy()
            params["signature"] = signature
            req.body = urllib.urlencode(params)
            req.header = {
                'Content-Length' : str(len(req.body)),
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'text/plain',
                'Connection': 'Keep-Alive'
            }
        else:
            req.body = ''
            # if this is a retried req, the qs from the previous try will
            # already be there, we need to get rid of that and rebuild it
            req.path = req.path.split('?')[0]
            req.path = (req.path + '?' + qs +
                                 '&signature=' + urllib.quote_plus(signature))
