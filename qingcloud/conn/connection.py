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
import threading
try:
    import httplib
except:
    import http.client as httplib


class ConnectionQueue(object):
    """ Http connection queue
    """

    def __init__(self, timeout=60):
        self.queue = []
        self.timeout = timeout

    def size(self):
        return len(self.queue)

    def get_conn(self):
        # get a valid connection or `None`
        for _ in range(len(self.queue)):
            (conn, _) = self.queue.pop(0)
            if self._is_conn_ready(conn):
                return conn
            else:
                self.put_conn(conn)

    def put_conn(self, conn):
        self.queue.append((conn, time.time()))

    def clear(self):
        # clear expired connections
        while self.queue and self._is_conn_expired(self.queue[0]):
            self.queue.pop(0)

    def _is_conn_expired(self, conn_info):
        (_, time_stamp) = conn_info
        return (time.time() - time_stamp) > self.timeout

    def _is_conn_ready(self, conn):
        # sometimes the response may not be remove
        # after read at lasttime's connection
        response = getattr(conn, '_HTTPConnection__response', None)
        return (response is None) or response.isclosed()


class ConnectionPool(object):
    """ Http connection pool for multiple hosts.
        It's thread-safe
    """

    CLEAR_INTERVAL = 5.0

    def __init__(self, timeout=60):
        self.timeout = timeout
        self.last_clear_time = time.time()
        self.lock = threading.Lock()
        self.pool = {}

    def size(self):
        with self.lock:
            return sum([conn.size() for conn in self.pool.values()])

    def put_conn(self, host, port, conn):
        # put connection into host's connection pool
        with self.lock:
            key = (host, port)
            queue = self.pool.setdefault(key, ConnectionQueue(self.timeout))
            queue.put_conn(conn)

    def get_conn(self, host, port):
        # get connection from host's connection pool
        # return a valid connection or `None`
        self._clear()
        with self.lock:
            key = (host, port)
            if key in self.pool:
                return self.pool[key].get_conn()

    def _clear(self):
        # clear expired connections of all hosts
        with self.lock:
            curr_time = time.time()
            if self.last_clear_time + self.CLEAR_INTERVAL > curr_time:
                return
            key_to_delete = []
            for key in self.pool:
                self.pool[key].clear()
                if self.pool[key].size() == 0:
                    key_to_delete.append(key)
            for key in key_to_delete:
                del self.pool[key]
            self.last_clear_time = curr_time


class HTTPRequest(object):

    def __init__(self, method, protocol, header, host, port, path,
                 params, auth_path=None, body=""):
        """
        Represents an HTTP request.

        @param method - The HTTP method name, 'GET', 'POST', 'PUT' etc.
        @param protocol - 'http' or 'https'
        @param header - http request header
        @param host - the host to make the connection to
        @param port - the port to use when connect to host
        @param path - URL path that is being accessed.
        @param auth_path - The part of the URL path used when creating the
                         authentication string.
        @param params - HTTP url query parameters, {'name':'value'}.
        @param body - Body of the HTTP request. If not present, will be None or
                     empty string ('').
        """
        self.method = method
        self.protocol = protocol
        self.header = header
        self.host = host
        self.port = port
        self.path = path
        self.auth_path = auth_path or path
        self.params = params
        self.body = body

    def __str__(self):
        return (('method:(%s) protocol:(%s) header(%s) host(%s) port(%s) path(%s) '
                 'params(%s) body(%s)') % (self.method, self.protocol, self.header,
                                           self.host, str(self.port),
                                           self.path, self.params,
                                           self.body))

    def authorize(self, connection, **kwargs):
        # add authorize information to request
        if connection._auth_handler:
            connection._auth_handler.add_auth(self, **kwargs)


class HTTPResponse(httplib.HTTPResponse):

    def __init__(self, *args, **kwargs):
        httplib.HTTPResponse.__init__(self, *args, **kwargs)
        self._cached_response = ""

    def read(self, amt=None):
        """Read the response.

        If this method is called without amt argument, the response body
        will be cached. Subsequent calls without arguments will return
        the cached response.
        """
        if amt is None:
            if not self._cached_response:
                self._cached_response = httplib.HTTPResponse.read(self)
            return self._cached_response
        else:
            return httplib.HTTPResponse.read(self, amt)


class HttpConnection(object):
    """
    Connection control to restful service
    """

    def __init__(self, qy_access_key_id, qy_secret_access_key, host=None,
                 port=443, protocol="https", pool=None, expires=None,
                 http_socket_timeout=10, debug=False):
        """
        @param qy_access_key_id - the access key id
        @param qy_secret_access_key - the secret access key
        @param host - the host to make the connection to
        @param port - the port to use when connect to host
        @param protocol - the protocol to access to web server, "http" or "https"
        @param pool - the connection pool
        """
        self.host = host
        self.port = port
        self.qy_access_key_id = qy_access_key_id
        self.qy_secret_access_key = qy_secret_access_key
        self.http_socket_timeout = http_socket_timeout
        self._conn = pool if pool else ConnectionPool()
        self.expires = expires
        self.protocol = protocol
        self.secure = protocol.lower() == "https"
        self.debug = debug
        self._auth_handler = None
        self._proxy_host = None
        self._proxy_port = None
        self._proxy_headers = None
        self._proxy_protocol = None

    def set_proxy(self, host, port=None, headers=None, protocol="http"):
        """ set http (https) proxy
        @param host - the host to make the connection to proxy host
        @param port - the port to use when connect to proxy host
        @param header - using by https proxy. The headers argument should be a mapping
                            of extra HTTP headers to send with the CONNECT request.
        @param protocol - 'http' or 'https'
                        if protocol is https, set the host and the port for HTTP Connect Tunnelling.
                        if protocol is http, Request-Uri is only absoluteURI.
        """
        if protocol not in ["http", "https"]:
            raise Exception("%s is not supported" % protocol)
        self._proxy_host = host
        self._proxy_port = port
        self._proxy_headers = headers
        self._proxy_protocol = protocol

    def _get_conn(self, host, port):
        """ Get connection from pool
        """
        conn = self._conn.get_conn(host, port)
        return conn or self._new_conn(host, port)

    def _set_conn(self, conn):
        """ Set valid connection into pool
        """
        self._conn.put_conn(conn.host, conn.port, conn)

    def _new_conn(self, host, port):
        """ Create new connection
        """
        if self.secure:
            conn = httplib.HTTPSConnection(
                host, port, timeout=self.http_socket_timeout)
        else:
            conn = httplib.HTTPConnection(
                host, port, timeout=self.http_socket_timeout)
        # Use self-defined Response class
        conn.response_class = HTTPResponse
        return conn

    def build_http_request(self, method, path, params, auth_path, headers,
                           host, data):
        raise NotImplementedError(
            "The build_http_request method must be implemented")

    def send(self, method, path, params=None, headers=None, host=None,
             auth_path=None, data=""):

        if not params:
            params = {}

        if not headers:
            headers = {}

        if not host:
            host = self.host

        # Build the http request
        request = self.build_http_request(method, path, params, auth_path,
                                          headers, host, data)
        request.authorize(self)

        conn_host = host
        conn_port = self.port
        request_path = request.path

        #: proxy
        if self._proxy_protocol:
            conn_host = self._proxy_host
            conn_port = self._proxy_port

        #: proxy - http
        if self._proxy_protocol == "http":
            request_path = "%s://%s%s" % (self.protocol, host, request_path)

        #: get connection
        conn = self._get_conn(conn_host, conn_port)

        #: proxy - https
        if self._proxy_protocol == "https":
            conn.set_tunnel(host, self.port, self._proxy_headers)

        # Send the request
        conn.request(method, request_path, request.body, request.header)

        # Receive the response
        response = conn.getresponse()

        # Reuse the connection
        if response.status < 500:
            self._set_conn(conn)

        return response
