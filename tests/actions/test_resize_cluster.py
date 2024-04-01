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

    conn = None
    zone = None
    secret_access_key = None
    access_key_id = None

    @classmethod
    def test_resize_cluster(self):
        self.access_key_id = "BHSWXNKSRKXUAXYCNXUI"
        self.secret_access_key = "AK0RfVfmpafzkgwMKcTckudgeKH2efYHxn1Nu3qj"
        self.zone = 'qa'

        self.conn = APIConnection(
            qy_access_key_id=self.access_key_id,
            qy_secret_access_key=self.secret_access_key,
            zone=self.zone,
            host="api.qacloud.com",
            port="80",
            protocol="http",

        )
        cluster = "cl-1ah8j7lp"
        # node_role_not_list = {"cpu": 2, "memory": 2048, "volume_size": 120, "storage_size": 120, "node_role": "maininstance"}
        node_role_with_list = [{"cpu":8,"memory":16384,"volume_size":100,"storage_size":100,"node_role":"maininstance"}]
        
        action = ClusterAction(self.conn)
        resp = action.resize_cluster(cluster, node_role=node_role_with_list)
        print(resp)
        # self.assertEqual(resp['ret_code'], 0)

