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

import json

from .key import Key
from .acl import ACL
from .multipart import MultiPartUpload
from .exception import get_response_error
from .util import load_data

class Bucket(object):
    DefaultContentType = "application/oct-stream"

    def __init__(self, connection=None, name=None):
        self.connection = connection
        self.name = name

    def __repr__(self):
        return '<Bucket: %s>' % self.name

    def __contains__(self, key_name):
        return not (self.get_key(key_name) is None)

    def __getitem__(self, key_name):
        key = self.get_key(key_name)
        if key:
            return key
        else:
            raise KeyError

    def __len__(self):
        pass

    def get_key(self, key_name, validate=True):
        """ Retrieves an object by name.
        Returns: An instance of a Key object or None

        Keyword arguments:
        key_name - The name of the bucket
        validate - If True, the function will try to verify the object exists
            on the service-side (Default: True)
        """

        if not validate:
            return Key(self, key_name)

        response = self.connection.make_request("HEAD", self.name, key_name)

        if response.status == 200:
            return Key(self, key_name)
        elif response.status == 401:
            err = get_response_error(response)
            err.code = "invalid_access_key_id"
            err.message = "Request not authenticated, Access Key ID is either " \
                "missing or invalid."
            raise err
        elif response.status == 403:
            err = get_response_error(response)
            err.code = "permission_denied"
            err.message = "You don't have enough permission to accomplish " \
                "this request."
            raise err
        elif response.status == 404:
            err = get_response_error(response)
            err.code = "object_not_exists"
            err.message = "The object you are accessing doesn't exist."
            raise err
        else:
            err = get_response_error(response)
            raise err

    def new_key(self, key_name):
        """ Create a new object within the bucket.
        The function will not PUT an object to service-side, utils function
        send_file of the return instance is called.
        Returns: An instance of a Key object

        Keyword arguments:
        key_name - The name of the object
        """
        return Key(self, key_name)

    def copy_key(self, key_name, source_bucket_name, source_key_name, headers=None):
        """ Create a new object within the bucket by copying from existing object.

        Keyword arguments:
            key_name - The name of the object
            source_bucket_name - The bucket of object to be copied from
            source_key_name - The key of object to be copied from
            headers - Extra request headers to send
        """
        copy_source = "/%s/%s" % (source_bucket_name, source_key_name)
        headers = headers or {}
        headers["X-QS-Copy-Source"] = copy_source

        resp = self.connection.make_request("PUT",
                                            self.name,
                                            key_name,
                                            headers=headers)
        if resp.status == 201:
            key = Key(self, key_name)
            key.content_type = resp.getheader("Content-Type")
            return key
        else:
            raise get_response_error(resp)

    def move_key(self, key_name, source_bucket_name, source_key_name, headers=None):
        """ Move an existing object to a new name within the bucket.

        Keyword arguments:
            key_name - The name of the object
            source_bucket_name - The bucket of object to be moved
            source_key_name - The key of object to be moved
            headers - Extra request headers to send
        """
        move_source = "/%s/%s" % (source_bucket_name, source_key_name)
        headers = headers or {}
        headers["X-QS-Move-Source"] = move_source

        resp = self.connection.make_request("PUT",
                                            self.name,
                                            key_name,
                                            headers=headers)
        if resp.status == 201:
            key = Key(self, key_name)
            key.content_type = resp.getheader("Content-Type")
            return key
        else:
            raise get_response_error(resp)

    def delete_key(self, key_name):
        """ Deleted the particular object by object name.

        Keyword arguments:
        key_name - The name of the object
        """
        response = self.connection.make_request("DELETE", self.name, key_name)
        if response.status == 204:
            return True
        else:
            err = get_response_error(response)
            raise err

    def list(self, prefix=None, delimiter=None, marker=None, limit=None):
        """ List objects of the bucket.

        Keyword arguments:
        prefix - Limits the response to keys that begin with the specified prefix
        delimiter - A character you use to group keys
        marker - Specifies the key to start with when listing objects
        limit - The count of objects that the request returns
        """
        params = {}
        if prefix:
            params["prefix"] = prefix
        if delimiter:
            params["delimiter"] = delimiter
        if marker:
            params["marker"] = marker
        if limit:
            params["limit"] = str(limit)
        response = self.connection.make_request(
            "GET", self.name, params=params)
        if response.status == 200:
            resp = load_data(response.read())
            result_set = []
            for k in resp["keys"]:
                key = Key(self, k["key"])
                key.content_type = k["mime_type"]
                result_set.append(key)
            return result_set
        else:
            err = get_response_error(response)
            raise err

    def delete(self):
        """ Delete the bucket
        """
        response = self.connection.make_request(
            "DELETE", self.name, num_retries=6)
        if response.status == 204:
            return True
        else:
            raise get_response_error(response)

    def stats(self):
        """ Retrieve the bucket meta information.
        """
        params = {"stats": None}
        response = self.connection.make_request(
            "GET", self.name, params=params)
        if response.status == 200:
            resp = load_data(response.read())
            return resp
        else:
            err = get_response_error(response)
            raise err

    def get_acl(self):
        """ Retrieve the bucket access control list.
        """
        params = {"acl": None}
        response = self.connection.make_request(
            "GET", self.name, params=params)
        if response.status == 200:
            resp = load_data(response.read())
            return ACL(self, resp["acl"])
        else:
            err = get_response_error(response)
            raise err

    def set_acl(self, acl):
        """ Set the bucket access control list.

        Keyword arguments:
        acl - The access control list
        """
        if isinstance(acl, ACL):
            grants = [grant.to_dict() for grant in acl.grants]
            data = json.dumps({"acl": grants})
        else:
            data = json.dumps({"acl": acl})

        params = {"acl": None}

        response = self.connection.make_request("PUT", self.name,
                                                params=params, data=data)
        if response.status == 200:
            return True
        else:
            err = get_response_error(response)
            raise err

    def initiate_multipart_upload(self, key_name, content_type=None):
        """Initiate a multipart upload.
        Returns: An instance of MultiPartUpload

        Keyword arguments:
        key_name - The object name
        content_type - The content type of the object
        """
        params = {"uploads": None}
        headers = {
            "Content-Type": content_type or self.DefaultContentType
        }
        response = self.connection.make_request(
            "POST", self.name, key_name, headers=headers, params=params)
        if response.status == 200:
            resp = load_data(response.read())
            handler = MultiPartUpload(self, key_name, resp["upload_id"])
            return handler
        else:
            err = get_response_error(response)
            raise err

    def cancel_multipart_upload(self, key_name, upload_id):
        """Abort the multipart upload.

        Keyword arguments:
        key_name - The object name
        upload_id - ID for the initiated multipart upload
        """
        params = {
            "upload_id": upload_id,
        }
        response = self.connection.make_request(
            "DELETE", self.name, key_name, params=params)
        if response.status == 204:
            return True
        else:
            err = get_response_error(response)
            raise err

    def complete_multipart_upload(self, key_name, upload_id, parts):
        """Complete the multipart upload.

        Keyword arguments:
        key_name - The object name
        upload_id - ID for the initiated multipart upload
        parts - The list of the multiparts which need to be combined
        """
        params = {
            "upload_id": upload_id,
        }
        object_parts = []
        # for part in sorted(parts, key=lambda x: x.part_number):
        for part in parts:
            object_parts.append({"part_number": part.part_number})

        if not object_parts:
            return False

        body = {"object_parts": object_parts}
        response = self.connection.make_request(
            "POST", self.name, key_name, data=json.dumps(body), params=params)
        if response.status == 201:
            return True
        else:
            err = get_response_error(response)
            raise err
