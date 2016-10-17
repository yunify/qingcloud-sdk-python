# =========================================================================
# Copyright 2015 Yunify, Inc.
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

from .exception import get_response_error
from .util import load_data


class Part(object):

    def __init__(self, bucket, key_name, part_number, size=None, created=None):
        """
        @param bucket - The name of the bucket
        @param key_name - The name of the object
        @param part_number - The number of the multipart
        @param size - The size of the multipart
        @param created - The creation time of the multipart
        """
        self.bucket = bucket
        self.key_name = key_name
        self.part_number = part_number
        self.size = size
        self.created = created

    def __repr__(self):
        return "<Part: %d, Key: %s>" % (
            self.part_number, self.key_name
        )


class MultiPartUpload(object):

    def __init__(self, bucket, key_name, upload_id):
        """
        @param bucket - The name of the bucket
        @param key_name - The name of the object
        @param upload_id - ID for the initiated multipart upload
        """
        self.bucket = bucket
        self.key_name = key_name
        self.upload_id = upload_id

    def upload_part_from_file(self, fp, part_number):
        """ Upload multipart from a file

        Keyword arguments:
        fp - a file-like object
        part_number - The number of the multipart
        """
        params = {
            "upload_id": self.upload_id,
            "part_number": str(part_number),
        }
        response = self.bucket.connection.make_request(
            "PUT", self.bucket.name, self.key_name, data=fp, params=params)
        if response.status == 201:
            part = Part(self.bucket.name, self.key_name, part_number)
            return part
        else:
            err = get_response_error(response)
            raise err

    def get_all_parts(self):
        """ Retrieve all multiparts of an object that uploaded.
        """
        params = {
            "upload_id": self.upload_id,
        }
        response = self.bucket.connection.make_request(
            "GET", self.bucket.name, self.key_name, params=params)
        if response.status == 200:
            parts = []
            resp = load_data(response.read())
            for item in resp["object_parts"]:
                part = Part(self.bucket.name, self.key_name,
                            item["part_number"])
                part.size = item["size"]
                part.created = item["created"]
                parts.append(part)
            return parts
        else:
            err = get_response_error(response)
            raise err

    def cancel_upload(self):
        """Abort the multipart upload.
        """
        return self.bucket.cancel_multipart_upload(
            self.key_name, self.upload_id
        )

    def complete_upload(self, parts):
        """Complete the multipart upload.
        """
        return self.bucket.complete_multipart_upload(
            self.key_name, self.upload_id, parts
        )
