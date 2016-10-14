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

from .util import load_data


class QSResponseError(Exception):

    def __init__(self, status, body=None, request_id=None,
                 code=None, message=None, url=None):
        self.status = status
        self.body = body or ''
        self.request_id = request_id
        self.code = code
        self.message = message
        self.url = url

    def __repr__(self):
        return "%s: %s %s\n%s" % (self.__class__.__name__,
                                  self.status, self.code, self.body)

    def __str__(self):
        return "%s: %s %s\n%s" % (self.__class__.__name__,
                                  self.status, self.code, self.body)


def get_response_error(response, body=None):
    if not body:
        body = response.read()
    args = {
        "status": response.status,
        "body": body,
        "request_id": response.getheader("request_id")
    }
    if body:
        try:
            resp = load_data(body)
            args["code"] = resp["code"]
            args["message"] = resp["message"]
            args["url"] = resp["url"]
        except ValueError:
            pass
    return QSResponseError(**args)
