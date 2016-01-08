import os
import json
import unittest

from tests import MockTestCase
from qingcloud.qingstor.connection import QSConnection

class TestQingStorMultiPart(MockTestCase):

    connection_class = QSConnection

    def setUp(self):
        super(TestQingStorMultiPart, self).setUp()
        self.mock_http_response(status_code=201)
        bucket = self.connection.create_bucket(bucket="mybucket", zone="pek3")
        body = {
            "bucket": "mybucket",
            "key": "myobject",
            "upload_id": "95e28428651f33ea8162b3209bf3b867"
        }
        self.mock_http_response(status_code=200, body=json.dumps(body))
        self.handler = bucket.initiate_multipart_upload(key_name="myobject")

    def test_multipart_upload_part_from_file(self):
        with open(".test_multipart_upload_part_from_file", "w+") as f:
            f.write("hello world")
        self.mock_http_response(status_code=201)
        for part_number in range(0, 3):
            with open(".test_multipart_upload_part_from_file", "r") as f:
                part = self.handler.upload_part_from_file(f, part_number)
                self.assertEqual(part.bucket, "mybucket")
                self.assertEqual(part.key_name, "myobject")
                self.assertEqual(part.part_number, part_number)
        os.remove(".test_multipart_upload_part_from_file")

    def test_get_all_parts(self):
        body = {
            "count": 3,
            "object_parts": [
                {"part_number": 1, "size": 12, "created": "2015-10-26T03:19:32.000Z"},
                {"part_number": 2, "size": 12, "created": "2015-10-26T03:19:32.000Z"},
                {"part_number": 3, "size": 12, "created": "2015-10-26T03:19:32.000Z"}
            ]
        }
        self.mock_http_response(status_code=200, body=json.dumps(body))
        parts = self.handler.get_all_parts()
        for index, part in enumerate(parts):
            self.assertEqual(part.part_number, body["object_parts"][index]["part_number"])
            self.assertEqual(part.size, body["object_parts"][index]["size"])
            self.assertEqual(part.created, body["object_parts"][index]["created"])

    def test_cancel_upload(self):
        self.mock_http_response(status_code=204)
        ret = self.handler.cancel_upload()
        self.assertTrue(ret)

    def test_complete_upload(self):
        body = {
            "count": 3,
            "object_parts": [
                {"part_number": 1, "size": 12, "created": "2015-10-26T03:19:32.000Z"},
                {"part_number": 2, "size": 12, "created": "2015-10-26T03:19:32.000Z"},
                {"part_number": 3, "size": 12, "created": "2015-10-26T03:19:32.000Z"}
            ]
        }
        self.mock_http_response(status_code=200, body=json.dumps(body))
        parts = self.handler.get_all_parts()
        self.mock_http_response(status_code=201)
        ret = self.handler.complete_upload(parts)
        self.assertTrue(ret)

if __name__ == "__main__":
    unittest.main()
