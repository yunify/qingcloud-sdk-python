import mock
import unittest
from StringIO import StringIO
from functools import partial

try:
    import httplib
except:
    import http.client as httplib

class MockTestCase(unittest.TestCase):
    """Base class for mocking http connection."""
    connection_class = None

    def setUp(self):
        self.responses_queue = []

        self.https_connection = mock.Mock(spec=httplib.HTTPSConnection("host", "port"))

        if self.connection_class is None:
            raise ValueError("The connection_class attribute must be set firstly")

        self.connection = self.connection_class(qy_access_key_id="access_key_id",
            qy_secret_access_key="secret_access_key")

        self.connection._new_conn = mock.Mock(return_value=self.https_connection)

    def create_http_response(self, status_code, header=None, body=None):

        if header is None:
            header = {}
        if body is None:
            body = ""

        response = mock.Mock(spec=httplib.HTTPResponse)
        response.status = status_code

        def body_reader(amt=None, body_stream=None):
            return body_stream.read(n=amt)

        response.read.side_effect = partial(
            body_reader, body_stream=StringIO(body))

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

    def get_response_from_queue(self):
        if not self.responses_queue:
            self.fail("Unexpected http request")
        retval = self.responses_queue[0]

        self.responses_queue = self.responses_queue[1:]

        return retval

    def check_pending_http_request(self):
        if self.responses_queue:
            self.fail("more http requests are expected")

    def push_mock_http_response(self, status_code, header=None, body=None):
        http_response = self.create_http_response(status_code, header, body)
        self.responses_queue.append(http_response)
        self.https_connection.getresponse.side_effect = self.get_response_from_queue
