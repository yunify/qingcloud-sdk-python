import unittest
import json

from qingcloud.qingstor.connection import QSConnection
from qingcloud.qingstor.file import InputFile, OutputFile
from tests import MockTestCase
from functools import partial


class TestQingStoreFile(MockTestCase):

    connection_class = QSConnection

    def make_input(self):
        input = InputFile(
            zone="pek3", access_key_id='abc', access_key='abc')
        input.conn = self.connection
        return input

    def make_output(self):
        output = OutputFile(
            zone="pek3", access_key_id='abc', access_key='abc')
        output.conn = self.connection
        return output

    def test_read(self):
        input = self.make_input()
        # read before open
        self.assertRaises(ValueError, input.read)
        body = "abcdefghij"
        self.mock_http_response(
            status_code=200, header={'content-length': len(body)}, body=body)
        input.open(bucket='abc', key='abc')
        # read all data
        data = input.read()
        self.assertEqual(body, data, "read invalid data")
        # read over eof
        data = input.read()
        self.assertEqual('', data, "read invalid data")
        input.close()
        # read after close
        self.assertRaises(ValueError, input.read)
        # read after reopen
        self.mock_http_response(
            status_code=200, header={'content-length': len(body)}, body=body)
        input.open(bucket='abc', key='abc')
        # read some data
        data = input.read(size=1)
        self.assertEqual('a', data, "read invalid data")
        data = input.read(size=1)
        self.assertEqual('b', data, "read invalid data")
        data = input.read(size=10)
        self.assertEqual('cdefghij', data, "read invalid data")
        input.close()
        input.close()

    def test_read_with_retry(self):
        body = "abcdefghij"
        self.mock_http_response(
            status_code=200, header={'content-length': len(body)}, body=body)
        input = self.make_input()
        input.open(bucket="mybucket", key="mykey")
        data = input.read(size=1)
        self.assertEqual('a', data, "read invalid data")
        # call _reset() as if an exception is caught and retry
        input._reset()
        input.conn = self.connection
        input.bucket.connection = self.connection
        self.mock_http_response(
            status_code=200, header={'content-length': len(body) - 1}, body=body[1:])
        data = input.read(size=1)
        self.assertEqual('b', data, "read invalid data")
        data = input.read(size=10)
        self.assertEqual('cdefghij', data, "read invalid data")

    def test_write(self):
        output = self.make_output()
        # write before open
        self.assertRaises(ValueError, partial(output.write, ""))
        body = {
            "bucket": "abc",
            "key": "abc",
            "upload_id": "95e28428651f33ea8162b3209bf3b867"
        }
        self.push_mock_http_response(status_code=200, body=json.dumps(body))
        output.open(bucket='abc', key='abc')
        self.check_pending_http_request()
        # test write data
        self.push_mock_http_response(status_code=201)
        buffer = ['a'] * (4 * 1024 * 1024 - 1)
        output.write(''.join(buffer))
        output.write("a")
        self.check_pending_http_request()
        self.push_mock_http_response(status_code=201)
        output.write(''.join(buffer))
        output.write("a")
        self.check_pending_http_request()
        # test close
        self.push_mock_http_response(status_code=201)
        output.close()
        output.close()
        # write after close
        self.assertRaises(ValueError, partial(output.write, 'a'))
        # test reopen
        self.push_mock_http_response(status_code=200, body=json.dumps(body))
        output.open(bucket='abc', key='def')
        # write data
        self.push_mock_http_response(status_code=201)
        output.write(''.join(buffer))
        output.write("a")
        self.check_pending_http_request()
        # test abort
        self.push_mock_http_response(status_code=204)
        output.abort()
        self.check_pending_http_request()
        output.close()
        output.close()


if __name__ == "__main__":
    unittest.main()
