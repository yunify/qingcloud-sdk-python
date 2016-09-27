import mock
import unittest
try:
    import httplib
except:
    import http.client as httplib


class MockTestCase(unittest.TestCase):
    """Base class for mocking http connection."""
    connection_class = None

    def setUp(self):

        self.https_connection = mock.Mock(
            spec=httplib.HTTPSConnection("host", "port"))

        if self.connection_class is None:
            raise ValueError(
                "The connection_class attribute must be set firstly")

        self.connection = self.connection_class(qy_access_key_id="access_key_id",
                                                qy_secret_access_key="secret_access_key")

        self.connection._new_conn = mock.Mock(
            return_value=self.https_connection)

    def create_http_response(self, status_code, header=None, body=None):

        if header is None:
            header = {}
        if body is None:
            body = ""

        response = mock.Mock(spec=httplib.HTTPResponse)
        response.status = status_code
        response.read.return_value = body
        response.length = len(body)
        response.getheaders.return_value = header

        def overwrite_header(arg, default=None):
            header_dict = dict(header)
            if arg in header_dict:
                return header_dict[arg]
            else:
                return default
        response.getheader.side_effect = overwrite_header

        return response

    def assert_request_parameters(self, params, ignore_params_values=None):
        """Verify the actual parameters sent to the service API."""
        request_params = self.actual_request.params.copy()
        if ignore_params_values is not None:
            for param in ignore_params_values:
                try:
                    del request_params[param]
                except KeyError:
                    pass
        self.assertDictEqual(request_params, params)

    def mock_http_response(self, status_code, header=None, body=None):
        http_response = self.create_http_response(status_code, header, body)
        self.https_connection.getresponse.return_value = http_response
