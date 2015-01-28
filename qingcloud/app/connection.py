from qingcloud.iaas.connection import APIConnection
from qingcloud.conn import auth
from . import constants as const
from qingcloud.misc.json_tool import json_load

class AppConnection(APIConnection):
    
    def __init__(self, app_id, secret_app_key, zone,
                 host='api.qingcloud.com', port=443, protocol='https',
                 pool=None, expires=None, retry_time=3,
                 http_socket_timeout=10, access_token=None):
        """
        @param app_id
        @param secret_app_key
        @param zone - the zone id to access
        @param host - the host to make the connection to
        @param port - the port to use when connect to host
        @param protocol - the protocol to access to web server, "http" or "https"
        @param pool - the connection pool
        @param retry_time - the retry_time when message send fail
        """
        APIConnection.__init__(self, app_id, secret_app_key, zone, host, port,
                               protocol, pool, expires, retry_time,
                               http_socket_timeout)
        self._auth_handler = auth.AppSignatureAuthHandler(app_id,
                                                          secret_app_key,
                                                          access_token)

    def send_request(self, action, body, url = '/app/', verb = 'GET'):
        """ send request """
        request = body
        request['action'] = action
        request.setdefault('zone', self.zone)
        if self.expires:
            request['expires'] = self.expires
        resp = self.send(url, request, verb)
        if resp:
            return json_load(resp)

    def describe_users(self, **ignore):
        """ get current app user info
        """
        action = const.ACTION_DESCRIBE_USERS
        body = {}

        return self.send_request(action, body)