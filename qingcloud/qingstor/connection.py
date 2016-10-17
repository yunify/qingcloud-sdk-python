# =========================================================================
# Copyright 2015 Yunify, Inc.
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

import os
import sys
import time
import random
import urllib
import hashlib
from datetime import datetime

try:
    from urllib.parse import quote, quote_plus, urlparse
except:
    from urllib import quote, quote_plus
    from urlparse import urlparse

from qingcloud.conn.auth import QSSignatureAuthHandler
from qingcloud.conn.connection import HttpConnection, HTTPRequest

from .bucket import Bucket
from .exception import get_response_error
from .util import load_data


class Zone(object):

    DEFAULT = ""
    PEK3A = "pek3a"


class VirtualHostStyleFormat(object):

    def build_host(self, server, bucket=""):
        if bucket:
            return "%s.%s" % (bucket, server)
        else:
            return server

    def build_auth_path(self, bucket="", key=""):
        path = "/"
        if bucket:
            path += bucket
        if key:
            path += "/%s" % key
        return path

    def build_path_base(self, bucket="", key=""):
        path = "/"
        if key:
            path += quote(key)
        return path


class QSConnection(HttpConnection):
    """ Public connection to qingstor
    """

    def __init__(self, qy_access_key_id=None, qy_secret_access_key=None,
                 host="qingstor.com", port=443, protocol="https",
                 style_format_class=VirtualHostStyleFormat,
                 retry_time=3, timeout=900, debug=False):
        """
        @param qy_access_key_id - the access key id
        @param qy_secret_access_key - the secret access key
        @param host - the host to make the connection to
        @param port - the port to use when connect to host
        @param protocol - the protocol to access to server, "http" or "https"
        @param retry_time - the retry_time when message send fail
        @param timeout - blocking operations will timeout after that many seconds
        @param debug - debug mode
        """

        # Set default host
        host = host
        # Set user agent
        self.user_agent = "QingStor SDK Python"
        # Set retry times
        self.retry_time = retry_time

        self.style_format = style_format_class()

        super(QSConnection, self).__init__(
            qy_access_key_id, qy_secret_access_key, host, port, protocol,
            None, None, timeout, debug)

        if qy_access_key_id and qy_secret_access_key:
            self._auth_handler = QSSignatureAuthHandler(host, qy_access_key_id,
                                                        qy_secret_access_key)
        else:
            self._auth_handler = None

    def get_all_buckets(self, zone=""):
        if zone:
            headers = {"Location": zone}
        else:
            headers = {}
        response = self.make_request("GET", headers=headers)
        if response.status == 200:
            return load_data(response.read())
        else:
            err = get_response_error(response)
            raise err

    def create_bucket(self, bucket, zone=Zone.DEFAULT):
        """ Create a new bucket.

        Keyword arguments:
        bucket - The name of the bucket
        zone - The zone at which bucket and its objects will locate.
            (Default: follow the service-side rule)
        """
        headers = {"Location": zone}
        response = self.make_request("PUT", bucket, headers=headers)
        if response.status in [200, 201]:
            return Bucket(self, bucket)
        else:
            raise get_response_error(response)

    def get_bucket(self, bucket, validate=True):
        """ Retrieve a bucket by name.

        Keyword arguments:
        bucket - The name of the bucket
        validate - If ``True``, the function will try to verify the bucket exists
            on the service-side. (Default: ``True``)
        """

        if not validate:
            return Bucket(self, bucket)

        response = self.make_request("HEAD", bucket)
        if response.status == 200:
            return Bucket(self, bucket)
        elif response.status == 401:
            err = get_response_error(response)
            err.code = "invalid_access_key_id"
            err.message = "Request not authenticated, Access Key ID is either " \
                "missing or invalid."
            raise err
        elif response.status == 403:
            err = get_response_error(response)
            err.code = "permission_denied"
            err.message = "You don't have enough permission to accomplish " \
                "this request."
            raise err
        elif response.status == 404:
            err = get_response_error(response)
            err.code = "bucket_not_exists"
            err.message = "The bucket you are accessing doesn't exist."
            raise err
        else:
            err = get_response_error(response)
            raise err

    def _get_content_length(self, body):
        thelen = 0
        try:
            thelen = str(len(body))
        except TypeError:
            # If this is a file-like object, try to fstat its file descriptor
            try:
                thelen = str(os.fstat(body.fileno()).st_size)
            except (AttributeError, OSError):
                # Don't send a length if this failed
                pass
        return thelen

    def _get_body_checksum(self, data):
        if hasattr(data, "read"):
            # Calculate the MD5 by reading the whole file content
            # This is evil, need to refactor later
            md5 = hashlib.md5()
            blocksize = 1024 * 4
            datablock = data.read(blocksize)
            while datablock:
                if sys.version > "3" and isinstance(datablock, str):
                    datablock = datablock.encode()
                md5.update(datablock)
                datablock = data.read(blocksize)
            token = md5.hexdigest()
            data.seek(0)
        else:
            if sys.version > "3" and isinstance(data, str):
                data = data.encode()
            token = hashlib.md5(data).hexdigest()
        return token

    def _build_params(self, params):

        params_str = ""
        params = params or {}
        for key, value in params.items():
            if params_str:
                params_str += "&"
            params_str += "%s" % quote_plus(key)
            if value is not None:
                params_str += "=%s" % quote_plus(value)
        return params_str

    def _urlparse(self, url):
        parts = urlparse(url)
        return parts.hostname, parts.path or "/", parts.query

    def build_http_request(self, method, path, params, auth_path,
                           headers, host, data):

        if isinstance(params, str):
            path = "%s?%s" % (path, params)
        else:
            suffix = self._build_params(params)
            path = "%s?%s" % (path, suffix) if suffix else path

        req = HTTPRequest(method, self.protocol, headers, host, self.port,
                          path, params, auth_path, data)
        return req

    def make_request(self, method, bucket="", key="", headers=None,
                     data="", params=None, num_retries=3):
        """ Make request
        """
        host = self.style_format.build_host(self.host, bucket)
        path = self.style_format.build_path_base(bucket, key)
        auth_path = self.style_format.build_auth_path(bucket, key)

        # Build request headers
        if not headers:
            headers = {}
        if "Host" not in headers:
            headers["Host"] = host
        if "Date" not in headers:
            headers["Date"] = datetime.utcnow().strftime("%a, %d %b %Y %X GMT")
        if "Content-Length" not in headers:
            headers["Content-Length"] = self._get_content_length(data)
        if data and "Content-MD5" not in headers:
            headers["Content-MD5"] = self._get_body_checksum(data)
        if "User-Agent" not in headers:
            headers["User-Agent"] = self.user_agent

        retry_time = 0
        while retry_time < self.retry_time:
            next_sleep = random.random() * (2 ** retry_time)
            try:
                response = self.send(method, path, params, headers, host,
                                     auth_path, data)
                if response.status == 307:
                    location = response.getheader("location")
                    host, path, params = self._urlparse(location)
                    headers["Host"] = host
                    # Seek to the start if this is a file-like object
                    if hasattr(data, "read") and hasattr(data, "seek"):
                        data.seek(0)
                elif response.status in (500, 502, 503):
                    time.sleep(next_sleep)
                else:
                    if response.length == 0:
                        response.close()
                    return response
            except Exception:
                if retry_time >= self.retry_time - 1:
                    raise
            retry_time += 1
