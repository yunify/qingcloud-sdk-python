# =========================================================================
# Copyright 2016 Yunify, Inc.
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

class ACL(object):

    def __init__(self, bucket=None, acl=None):
        """
        @param bucket - The bucket
        @param acl - The access control list of the bucket
        """
        self.bucket = bucket
        self.acl = acl or []
        self.grants = []
        for item in self.acl:
            grantee = item["grantee"]
            if grantee["type"] == "user":
                grant = Grant(
                    permission=item["permission"],
                    type=grantee["type"],
                    id=grantee["id"],
                    name=grantee["name"]
                )
            else:
                grant = Grant(
                    permission=item["permission"],
                    type=grantee["type"],
                    name=grantee["name"]
                )
            self.add_grant(grant)

    def add_grant(self, grant):
        self.grants.append(grant)

    def __repr__(self):
        return str(self.grants)


class Grant(object):

    def __init__(self, permission, type, id=None, name=None):
        """
        @param permission - The grant permission
        @param type - The grantee type
        @param id - The grantee user id
        @param name - The grantee name
        """
        self.permission = permission
        self.type = type
        self.id = id
        self.name = name

    def __repr__(self):
        if self.type== "user":
            args = (self.id, self.permission)
        else:
            args = (self.name, self.permission)
        return "<Grantee: %s, Permission: %s>" % args

    def to_dict(self):

        if self.type == "user":
            grantee = {
                "type": self.type,
                "id": self.id,
                "name": self.name or ""
            }
        else:
            grantee = {
                "type": self.type,
                "name": self.name
            }

        return {
            "grantee": grantee,
            "permission": self.permission
        }
