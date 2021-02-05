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
import time
import random
import unittest
from qingcloud.iaas.connection import APIConnection


class TestInstanceGroupsAction(unittest.TestCase):

    max_retry_times = 2

    @classmethod
    def setUpClass(cls):
        """ Initialization of test. """

        cls.access_key_id = os.getenv('QY_ACCESS_KEY_ID')
        cls.secret_access_key = os.getenv('QY_SECRET_ACCESS_KEY')
        cls.zone = 'pek3'

        cls.conn = APIConnection(
            qy_access_key_id=cls.access_key_id,
            qy_secret_access_key=cls.secret_access_key,
            zone=cls.zone,
        )

        # Describe image
        resp = cls.conn.describe_images(limit=1, status=['available'], provider='selected')
        import pprint
        pprint.pprint(resp)
        image_id_list = resp.get('image_set', [])
        if image_id_list:
            image_id = image_id_list[0].get('image_id')
        else:
            raise Exception('No available images')

        # Create two test instance.
        resp = cls.conn.run_instances(
            image_id=image_id,
            cpu=1,
            memory=1024,
            instance_name='Test_add_InstanceGroupsAction',
            count=2,
            login_mode="passwd",
            login_passwd='Test_add_InstanceGroupsAction99'
        )
        pprint.pprint(resp)
        cls.existed_instances = resp['instances']
        cls.group_dict = {'repel_group': None, 'attract_group': None}

        if resp.get('ret_code') == 0:
            # Ensure that instances is available for test.
            while True:
                status_resp = cls.conn.describe_instances(
                    instances=cls.existed_instances
                )
                if status_resp['instance_set'][0].get('status') == 'running' and \
                   status_resp['instance_set'][1].get('status') == 'running':
                    break
        else:
            raise Exception

    def test01_create_instance_groups(self):

        # Create a repel-group.
        resp_repel_group = self.conn.create_instance_groups(relation='repel')
        self.group_dict.update(repel_group=resp_repel_group['instance_groups'].pop())
        self.assertEqual(resp_repel_group['ret_code'], 0)

        # Create a attract-group.
        resp_attract_group = self.conn.create_instance_groups(relation='attract')
        self.group_dict.update(attract_group=resp_attract_group['instance_groups'].pop())
        self.assertEqual(resp_attract_group['ret_code'], 0)

    def test02_join_instance_group(self):

        existed_instances = [
            self.existed_instances[0],
            self.existed_instances[1]
        ]
        tmp = {'instances': [random.choice(existed_instances)],
               'group_id': self.group_dict.get('repel_group')}
        existed_instances.remove(tmp['instances'][0])

        # Add an instance into repel-group.
        resp_repel = self.conn.join_instance_group(
            instances=tmp['instances'],
            instance_group=tmp['group_id']
        )
        self.group_dict.update(repel_group=tmp)
        self.assertEqual(resp_repel['ret_code'], 0)

        tmp = {'instances': [random.choice(existed_instances)],
               'group_id': self.group_dict.get('attract_group')}

        # Add an instance into attract-group.
        resp_attract = self.conn.join_instance_group(
            instances=tmp['instances'],
            instance_group=tmp['group_id']
        )
        self.group_dict.update(attract_group=tmp)
        self.assertEqual(resp_attract['ret_code'], 0)

    def test03_describe_instance_groups(self):

        repel_id = self.group_dict['repel_group'].get('group_id')
        resp_repel = self.conn.describe_instance_groups(
            instance_groups=[repel_id]
        )
        self.assertEqual(resp_repel['instance_group_set'][0]['instance_group_id'], repel_id)

        attract_id = self.group_dict['attract_group'].get('group_id')
        resp_attract = self.conn.describe_instance_groups(
            instance_groups=[attract_id]
        )
        self.assertEqual(resp_attract['instance_group_set'][0]['instance_group_id'], attract_id)

    def test04_leave_instance_group(self):

        try_count = 0
        while try_count < self.max_retry_times:
            try:
                resp_repel = self.conn.leave_instance_group(
                    instances=self.group_dict['repel_group'].get('instances'),
                    instance_group=self.group_dict['repel_group'].get('group_id')
                )
                self.assertEqual(resp_repel['ret_code'], 0)
            except Exception:
                try_count += 1
                time.sleep(2**try_count)
                pass

        try_count = 0
        while try_count < self.max_retry_times:
            try:
                resp_attract = self.conn.leave_instance_group(
                    instances=self.group_dict['attract_group'].get('instances'),
                    instance_group=self.group_dict['attract_group'].get('group_id')
                )
                self.assertEqual(resp_attract['ret_code'], 0)
            except Exception:
                try_count += 1
                time.sleep(2**try_count)
                pass

    def test05_delete_instance_groups(self):

        try_count = 0
        while try_count < self.max_retry_times:
            check_empty = self.conn.describe_instance_groups(
                instance_groups=[
                    self.group_dict['repel_group'].get('group_id'),
                    self.group_dict['attract_group'].get('group_id')
                ]
            )
            if not check_empty['instance_group_set'][0].get('instances') and \
               not check_empty['instance_group_set'][1].get('instances'):
                break

        resp_del_groups = self.conn.delete_instance_groups(
            instance_groups=[
                self.group_dict['repel_group'].get('group_id'),
                self.group_dict['attract_group'].get('group_id')
            ]
        )
        self.assertEqual(resp_del_groups['ret_code'], 0)

    @classmethod
    def tearDownClass(cls):
        """ Terminate the test instances."""

        try_count = 0
        while try_count < cls.max_retry_times+3:

            resp = cls.conn.terminate_instances(
                instances=cls.existed_instances,
                direct_cease=1
            )
            if resp['ret_code'] == 1400:
                try_count += 1
                time.sleep(2**try_count)
                continue
            elif resp['ret_code'] == 0:
                cls.conn._get_conn(cls.conn.host, cls.conn.port).close()
                break


if __name__ == '__main__':

    unittest.main()
