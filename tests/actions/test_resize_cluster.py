# =========================================================================
# Copyright 2012-present Yunify, Inc.
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
import os
import unittest

from qingcloud.iaas import APIConnection
from qingcloud.iaas.errors import InvalidRouterStatic
from qingcloud.iaas.actions.cluster import ClusterAction


class ClusterFactoryTestCase(unittest.TestCase):

    protocol = None
    port = None
    host = None
    conn = None
    zone = None
    secret_access_key = None
    access_key_id = None

    @classmethod
    def test_resize_cluster(self):
        self.access_key_id = os.getenv("QY_ACCESS_KEY_ID")
        self.secret_access_key = os.getenv("QY_SECRET_ACCESS_KEY")
        self.host = os.getenv("QY_HOST")
        self.port = os.getenv("QY_PORT")
        self.zone = os.getenv("QY_ZONE")
        self.protocol = os.getenv("QY_PROTOCOL")

        self.conn = APIConnection(
            qy_access_key_id=self.access_key_id,
            qy_secret_access_key=self.secret_access_key,
            zone=self.zone,
            host=self.host,
            port=self.port,
            protocol=self.protocol,

        )
        cluster = ""
        # node_role_not_list = {"cpu": 2, "memory": 2048, "volume_size": 120, "storage_size": 120, "node_role": "maininstance"}
        node_role_with_list = [{"cpu":4,"memory":8192,"volume_size":100,"storage_size":100,"node_role":"maininstance"}]
        
        action = ClusterAction(self.conn)
        resp = action.resize_cluster(cluster, node_role=node_role_with_list)
        print(resp)
        assert resp.get('ret_code') == 0

