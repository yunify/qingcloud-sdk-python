import json
import unittest

from tests import MockTestCase
from qingcloud.qingstor.connection import QSConnection
from qingcloud.qingstor.multipart import MultiPartUpload, Part

class TestQingStorBucket(MockTestCase):

    connection_class = QSConnection

    def setUp(self):
        super(TestQingStorBucket, self).setUp()
        self.mock_http_response(status_code=201)
        self.bucket = self.connection.create_bucket(bucket="mybucket", zone="pek3")
        self.assertEqual(self.bucket.name, "mybucket")

    def test_bucket_delete(self):
        self.mock_http_response(status_code=204)
        self.bucket.delete()

    def test_bucket_new_key(self):
        key = self.bucket.new_key("myobject")
        self.assertEqual(key.name, "myobject")

    def test_bucket_get_key(self):
        self.mock_http_response(status_code=200)
        key = self.bucket.get_key("myobject")
        self.assertEqual(key.name, "myobject")

    def test_bucket_delete_key(self):
        self.mock_http_response(status_code=204)
        self.bucket.delete_key("myobject")

    def test_bucket_list(self):

        keys = [{
            "modified": 1445508821,
            "created": "2015-10-22T10:13:41.000Z",
            "mime_type": "application/x-www-form-urlencoded",
            "key": "bbcfvevjkcoorkvo",
            "size": 409600
        },{
            "modified": 1445508789,
            "created": "2015-10-22T10:13:09.000Z",
            "mime_type": "application/x-www-form-urlencoded",
            "key": "bbcnjwqyqpodqmqf",
            "size": 409600
        },{
            "modified": 1445508833,
            "created": "2015-10-22T10:13:53.000Z",
            "mime_type": "application/x-www-form-urlencoded",
            "key": "bbdwopvqfbpjqwjo",
            "size": 409600
        }]

        body = {
            "keys": keys,
            "prefix": "",
            "limit": 200,
            "name": "tsung-get-1445508780",
            "owner": "f9c74ff873c311e5948c5254862d85f1",
            "delimiter": "",
            "marker": "bnlepimlrwmlosvq",
            "common_prefixes": []
        }
        self.mock_http_response(status_code=200, body=json.dumps(body))
        resp = self.bucket.list()
        for index, key in enumerate(resp):
            self.assertEqual(key.name, keys[index]["key"])
            self.assertEqual(key.content_type, keys[index]["mime_type"])
            self.assertEqual(key.bucket.name, "mybucket")

    def test_bucket_stats(self):
        body = {
            "count": 10000,
            "status": "active",
            "name": "tsung-get-1445508780",
            "created": "2015-10-22T10:12:59.000Z",
            "url": "http://tsung-get-1445508780.pek3.qingstor.com",
            "location": "pek3",
            "status_time": "2015-10-22T10:12:59.000Z",
            "size": 4096000000
        }
        self.mock_http_response(status_code=200, body=json.dumps(body))
        stats = self.bucket.stats()
        self.assertDictEqual(stats, body)

    def test_bucket_get_acl(self):
        body = {
            "owner": {"id": "usr-1mvNCzZu", "name": ""},
            "acl":
            [{
                "grantee": {"id": "usr-B5WmNqAI", "name": "william"},
                "permission": "FULL_CONTROL"
            }]
        }
        self.mock_http_response(status_code=200, body=json.dumps(body))
        acls = self.bucket.get_acl()
        self.assertDictEqual(acls, body)

    def test_bucket_set_acl(self):
        self.mock_http_response(status_code=200)
        ret = self.bucket.set_acl({
            "*": "READ",
            "usr-B5WmNqAI": "FULL_CONTROL",
        })
        self.assertTrue(ret)

    def test_bucket_initiate_multipart_upload(self):
        body = {
            "bucket": "mybucket",
            "key": "myobject",
            "upload_id": "95e28428651f33ea8162b3209bf3b867"
        }
        self.mock_http_response(status_code=200, body=json.dumps(body))
        handler = self.bucket.initiate_multipart_upload(key_name="myobject")
        self.assertIsInstance(handler, MultiPartUpload)

    def test_bucket_cancel_multipart_upload(self):
        self.mock_http_response(status_code=204)
        ret = self.bucket.cancel_multipart_upload(key_name="myobject",
            upload_id="95e28428651f33ea8162b3209bf3b867")
        self.assertTrue(ret)

    def test_bucket_complete_multipart_upload(self):
        parts = []
        for part_number in range(0, 3):
            part = Part(bucket="mybucket", key_name="myobject", part_number=part_number)
            parts.append(part)
        self.mock_http_response(status_code=201)
        ret = self.bucket.complete_multipart_upload(key_name="myobject",
            upload_id="95e28428651f33ea8162b3209bf3b867", parts=parts)
        self.assertTrue(ret)


if __name__ == "__main__":
    unittest.main()
