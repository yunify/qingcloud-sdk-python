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

import time
import random
import unittest
from qingcloud.iaas.connection import APIConnection


class TestInstanceGroupsAction(unittest.TestCase):

    access_key_id = input('Please input your Access-Key-ID: ')
    secret_access_key = input('Please input your Secret-Access-Key: ')
    zone = input('Please input your zone ID: ')
    group_dict = {'repel_group': '', 'attract_group': ''}
    # at least 2 existed instances of yours were required here.
    existed_instances = ['i-t1n999yi', 'i-agd5mfok']

    def setUp(self):
        """ Initialization of connection """
        # Every action needs the Connection Object for sending request.
        self.conn = APIConnection(
            qy_access_key_id=self.access_key_id,
            qy_secret_access_key=self.secret_access_key,
            zone=self.zone
        )

    def test01_create_instance_groups(self):

        resp_repel_group = self.conn.create_instance_groups(relation='repel')
        self.group_dict.update(repel_group=resp_repel_group['instance_groups'].pop())
        time.sleep(2)
        self.assertEqual(resp_repel_group['ret_code'], 0)

        resp_attract_group = self.conn.create_instance_groups(relation='attract')
        self.group_dict.update(attract_group=resp_attract_group['instance_groups'].pop())
        time.sleep(2)
        self.assertEqual(resp_attract_group['ret_code'], 0)

    def test02_join_instance_group(self):

        tmp = {'instances': [random.choice(self.existed_instances)],
               'group_id': self.group_dict.get('repel_group')}
        resp_repel = self.conn.join_instance_group(
            instances=tmp['instances'],
            instance_group=tmp['group_id']
        )
        self.group_dict.update(repel_group=tmp)
        time.sleep(2)
        self.assertEqual(resp_repel['ret_code'], 0)

        tmp = {'instances': [random.choice(self.existed_instances)],
               'group_id': self.group_dict.get('attract_group')}
        resp_attract = self.conn.join_instance_group(
            instances=tmp['instances'],
            instance_group=tmp['group_id']
        )
        self.group_dict.update(attract_group=tmp)
        time.sleep(2)
        self.assertEqual(resp_attract['ret_code'], 0)

    def test03_describe_instance_groups(self):

        repel_id = self.group_dict['repel_group'].get('group_id')
        resp_repel = self.conn.describe_instance_groups(
            instance_groups=[repel_id]
        )
        time.sleep(2)
        self.assertEqual(resp_repel['instance_group_set'][0]['instance_group_id'], repel_id)

        attract_id = self.group_dict['attract_group'].get('group_id')
        resp_attract = self.conn.describe_instance_groups(
            instance_groups=[attract_id]
        )
        time.sleep(2)
        self.assertEqual(resp_attract['instance_group_set'][0]['instance_group_id'], attract_id)

    def test04_leave_instance_group(self):

        resp_repel = self.conn.leave_instance_group(
            instances=self.group_dict['repel_group'].get('instances'),
            instance_group=self.group_dict['repel_group'].get('group_id')
        )
        time.sleep(2)
        self.assertEqual(resp_repel['ret_code'], 0)

        resp_attract = self.conn.leave_instance_group(
            instances=self.group_dict['attract_group'].get('instances'),
            instance_group=self.group_dict['attract_group'].get('group_id')
        )
        time.sleep(2)
        self.assertEqual(resp_attract['ret_code'], 0)

    def test05_delete_instance_groups(self):

        resp_del = self.conn.delete_instance_groups(
            instance_groups=[
                self.group_dict['repel_group'].get('group_id'),
                self.group_dict['attract_group'].get('group_id')
            ]
        )
        time.sleep(2)
        self.assertEqual(resp_del['ret_code'], 0)


if __name__ == '__main__':

    unittest.main()
