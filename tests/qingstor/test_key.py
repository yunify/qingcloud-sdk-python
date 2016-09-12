import os
import unittest

from tests import MockTestCase
from qingcloud.qingstor.connection import QSConnection


class TestQingStorKey(MockTestCase):

    connection_class = QSConnection

    def setUp(self):
        super(TestQingStorKey, self).setUp()
        self.mock_http_response(status_code=201)
        conn = self.connection
        bucket = conn.create_bucket(bucket="mybucket", zone="pek3")
        self.mock_http_response(status_code=200)
        self.key = bucket.get_key("myobject")
        self.assertEqual(self.key.name, "myobject")

    def test_key_open(self):
        self.mock_http_response(status_code=200)
        self.key.open(mode="r")

    def test_key_read(self):
        self.mock_http_response(status_code=200, body="hello world")
        data = self.key.read()
        self.assertEqual(data, "hello world")

    def test_key_send_file(self):
        with open(".test_key_send_file", "w+") as f:
            f.write("hello world")
        self.mock_http_response(status_code=201)
        with open(".test_key_send_file", "r") as f:
            ret = self.key.send_file(f, content_type="text/plain")
            self.assertTrue(ret)
        os.remove(".test_key_send_file")

    def test_key_exists(self):
        self.mock_http_response(status_code=200)
        ret = self.key.exists()
        self.assertTrue(ret)
        self.mock_http_response(status_code=404)
        ret = self.key.exists()
        self.assertFalse(ret)


if __name__ == "__main__":
    unittest.main()
