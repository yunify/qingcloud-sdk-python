from qingcloud.iaas.connection import APIConnection
from qingcloud.conn import auth
from . import constants as const
from __builtin__ import str


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

    def send_request(self, action, body, url='/app/', verb='GET'):
        """ Send request
        """
        return super(AppConnection, self).send_request(action, body, url, verb)

    def describe_users(self, **ignore):
        """ get current app user info
        """
        action = const.ACTION_DESCRIBE_USERS
        body = {}

        return self.send_request(action, body)

    def lease_app(self, service, resource=None):
        """ start lease app
        @param service: service to lease
        @param resource: related qingcloud resource
        """
        action = const.ACTION_LEASE_APP
        body = {"service": service}
        if resource:
            body["resource"] = resource

        return self.send_request(action, body)

    def unlease_app(self, resources):
        """ start lease app
        @param resources: list of resource ids to unlease.
                          It can be id of user, app, service or appr.
                          For user id, unlease all app services for this user
                          For app id, unlease all services for this app
                          For service id, unlease all services
                          user id and other id can be conbined to unlease service for specified user
        """
        action = const.ACTION_UNLEASE_APP

        if isinstance(resources, str):
            resources = [resources]

        if not isinstance(resources, list):
            return None

        body = {"resources": resources}

        return self.send_request(action, body)
