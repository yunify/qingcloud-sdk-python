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


class Key(object):

    DefaultContentType = "application/oct-stream"

    def __init__(self, bucket=None, name=None):

        self.bucket = bucket
        self.name = name
        self.resp = None
        self.content_type = self.DefaultContentType

    def __repr__(self):
        return '<Key: %s, %s>' % (self.name, self.bucket.name)

    def close(self):
        if self.resp:
            self.resp.read()
        self.resp = None

    def open_read(self, headers=None):
        """ Open this key for reading.
        """
        if self.resp is None:
            self.resp = self.bucket.connection.make_request(
                "GET", self.bucket.name, self.name, headers=headers)
            if self.resp.status != 200 and self.resp.status != 206:
                err = get_response_error(self.resp)
                raise err

    def open(self, mode="r", headers=None):
        if mode == "r":
            self.open_read(headers)
        else:
            raise Exception("Not implement mode %s yet" % mode)

    def read(self, size=0):
        if size == 0:
            self.open_read()
        else:
            headers = {"Range": "bytes=0-%d" % size}
            self.open_read(headers)
        data = self.resp.read()
        if not data:
            self.resp.close()
        return data

    def send_file(self, fp, content_type=None):
        """ Upload a file to a key into the bucket.

        Keyword arguments:
        content_type - The content type of the object
        """
        headers = {
            "Content-Type": content_type or self.content_type
        }
        response = self.bucket.connection.make_request(
            "PUT", self.bucket.name, self.name, data=fp, headers=headers)
        if response.status == 201:
            self.close()
            return True
        else:
            err = get_response_error(response)
            raise err

    def exists(self):
        """ Check whether the object exists or not.
        """
        response = self.bucket.connection.make_request("HEAD", self.bucket.name,
                                                       self.name)
        if response.status == 200:
            return True
        elif response.status == 404:
            return False
        else:
            err = get_response_error(response)
            raise err
