"""
Basic http connection to qingcloud
"""

import time
import socket
import random
import threading
import httplib

import auth

class ConnectionQueue(object):
    """
    Http connection queue
    """

    def __init__(self, timeout = 60):
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
    """
    Http connection pool for multiple hosts.
    It's thread-safe
    """

    CLEAR_INTERVAL = 5.0

    def __init__(self, timeout = 60):
        self.timeout = timeout
        self.last_clear_time = time.time()
        self.lock = threading.Lock()
        self.pool = {}

    def size(self):
        with self.lock:
            return sum([conn.size() for conn in self.pool.values()])

    def put_conn(self, host, is_secure, conn):
        # put connection into host's connection pool
        with self.lock:
            key = (host, is_secure)
            queue = self.pool.setdefault(key, ConnectionQueue(self.timeout))
            queue.put_conn(conn)

    def get_conn(self, host, is_secure):
        # get connection from host's connection pool
        # return a valid connection or `None`
        self._clear()
        with self.lock:
            key = (host, is_secure)
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
                 params, body = ""):
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
        self.auth_path = path
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
        connection._auth_handler.add_auth(self, **kwargs)


class HttpConnection(object):
    """
    Connection control to restful service
    """

    def __init__(self, qy_access_key_id, qy_secret_access_key, zone,
            host='api.qingcloud.com', port=443, protocol='https',
            pool = None,
            retry_time = 3, http_socket_timeout = 10):
        """
        @param qy_access_key_id - the access key id
        @param qy_secret_access_key - the secret access key
        @param zone - the zone id to access
        @param host - the host to make the connection to
        @param port - the port to use when connect to host
        @param protocol - the protocol to access to web server, "http" or "https"
        @param pool - the connection pool
        @param retry_time - the retry_time when message send fail
        """
        self.host = host
        self.port = port
        self.qy_access_key_id = qy_access_key_id
        self.qy_secret_access_key = qy_secret_access_key
        self.zone = zone
        self.retry_time = retry_time
        self.http_socket_timeout = http_socket_timeout
        self._conn = pool if pool else ConnectionPool()
        self.protocol = protocol
        self.secure = protocol.lower() == "https"
        self._auth_handler = auth.QuerySignatureAuthHandler(
                self.host,
                self.qy_access_key_id,
                self.qy_secret_access_key,
                )

    def _get_conn(self):
        # get connection from pool
        conn = self._conn.get_conn(self.host, self.secure)
        return conn or self._new_conn()

    def _set_conn(self, conn):
        # set valid connection into pool
        self._conn.put_conn(self.host, self.secure, conn)

    def _new_conn(self):
        if self.secure:
            return httplib.HTTPSConnection(self.host, self.port,
                    timeout = self.http_socket_timeout)
        else:
            return httplib.HTTPConnection(self.host, self.port,
                    timeout = self.http_socket_timeout)

    def _build_http_request(self, url, base_params, verb):
        params = {}
        for key, values in base_params.items():
            if values is None:
                continue
            if isinstance(values, list):
                for i in range(1, len(values) + 1):
                    if isinstance(values[i - 1], dict):
                        for sk, sv in values[i - 1].items():
                            params['%s.%d.%s' % (key, i, sk)] = sv
                    else:
                        params['%s.%d' % (key, i)] = values[i - 1]
            else:
                params[key] = values

        return HTTPRequest(verb, self.protocol, "", self.host, self.port, url,
                 params)

    def send(self, url, params, verb = 'GET'):
        # send request
        request = self._build_http_request(url, params, verb)
        conn = self._get_conn()
        retry_time = 0
        while retry_time < self.retry_time:
            # Use binary exponential backoff to desynchronize client requests
            next_sleep = random.random() * (2 ** retry_time)
            try:
                if verb == "POST":
                    conn.request(verb, request.path, request.body, request.header)
                else:
                    request.authorize(self)
                    #print "sending request [%s]" % request.path
                    conn.request(verb, request.path, request.body)
                response = conn.getresponse()
                if response.status == 200:
                    self._set_conn(conn)
                    return response.read()
                else:
                    #print "recv abnormal status [%d] for request [%s] " % (response.status, request)
                    _ = response.read()
                    conn = self._get_conn()
            except Exception, e:
                # only retry for timeout error
                if isinstance(e, socket.timeout):
                    #print "send request failed for request [%s], exception: [%s]" % (request, e.__class__.__name__)
                    return None
                conn = self._get_conn()
            time.sleep(next_sleep)
            retry_time += 1
            #print "retry request for [%d] time after sleep for [%.2f] secs" % (retry_time, next_sleep)
