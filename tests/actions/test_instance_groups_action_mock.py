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

import mock
import random
import unittest
from iaas.actions.instance_groups import InstanceGroupsAction


class TestInstanceGroupsAction(unittest.TestCase):

    max_retry_times = 2

    @classmethod
    def setUpClass(cls):
        """ Initialization of mock test. """

        cls.ig_action_object = InstanceGroupsAction(mock.Mock())
        cls.group_dict = {}
        cls.existed_instances = ["i-s5sdo5of", "i-a1wy8cvt"]

    def test01_create_instance_groups(self):

        # Create a repel-group.
        # self.conn.create_instance_groups = mock.Mock(return_value={
        self.ig_action_object.conn.send_request = mock.Mock(return_value={
            "action": "CreateInstanceGroupsResponse",
            "instance_groups": ["ig-9edrghud"],
            "ret_code": 0
        })
        resp_repel_group = self.ig_action_object.create_instance_groups(relation='repel')
        self.group_dict.update(repel_group=resp_repel_group['instance_groups'].pop())
        self.assertEqual(resp_repel_group['ret_code'], 0)

        # Create a attract-group.
        self.ig_action_object.conn.send_request = mock.Mock(return_value={
            "action": "CreateInstanceGroupsResponse",
            "instance_groups": ["ig-ejtdp9su"],
            "ret_code": 0
        })
        resp_attract_group = self.ig_action_object.create_instance_groups(relation='attract')
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
        self.ig_action_object.conn.send_request = mock.Mock(return_value={
            "action": "JoinInstanceGroupResponse",
            "job_id": "j-ggxi98503wy",
            "ret_code": 0
        })
        resp_repel = self.ig_action_object.join_instance_group(
            instances=tmp['instances'],
            instance_group=tmp['group_id']
        )
        self.group_dict.update(repel_group=tmp)
        self.assertEqual(resp_repel['ret_code'], 0)

        tmp = {'instances': [random.choice(existed_instances)],
               'group_id': self.group_dict.get('attract_group')}

        # Add an instance into attract-group.
        self.ig_action_object.conn.send_request = mock.Mock(return_value={
            "action": "JoinInstanceGroupResponse",
            "job_id": "j-j7e7lt0nk4c",
            "ret_code": 0
        })
        resp_attract = self.ig_action_object.join_instance_group(
            instances=tmp['instances'],
            instance_group=tmp['group_id']
        )
        self.group_dict.update(attract_group=tmp)
        self.assertEqual(resp_attract['ret_code'], 0)

    def test03_describe_instance_groups(self):

        repel_id = self.group_dict['repel_group'].get('group_id')

        self.ig_action_object.conn.send_request = mock.Mock(return_value={
            "action": "DescribeInstanceGroupsResponse",
            "total_count": 1,
            "instance_group_set":[{
                "instance_group_name": "\u5206\u6563",
                "description": "",
                "tags": [],
                "controller": "self",
                "console_id": "alphacloud",
                "instances": [{
                    "instance_id": "i-s5sdo5of",
                    "instance_name": "test4",
                    "status": "running",
                    "instance_group_id": "ig-9edrghud"
                }],
                "root_user_id": "usr-jGys5Ecd",
                "create_time": "2021-02-08T09:00:38Z",
                "relation": "repel",
                "owner": "usr-jGys5Ecd",
                "resource_project_info": [],
                "instance_group_id": "ig-9edrghud",
                "zone_id": "test"
            }],
            "ret_code": 0
        })

        resp_repel = self.ig_action_object.describe_instance_groups(
            instance_groups=[repel_id]
        )
        self.assertEqual(resp_repel['instance_group_set'][0]['instance_group_id'], repel_id)

        attract_id = self.group_dict['attract_group'].get('group_id')

        self.ig_action_object.conn.send_request = mock.Mock(return_value={
            "action": "DescribeInstanceGroupsResponse",
            "total_count": 1,
            "instance_group_set": [{
                "instance_group_name": "\u96c6\u4e2d",
                "description": "",
                "tags": [],
                "controller": "self",
                "console_id": "alphacloud",
                "instances":[{
                    "instance_id": "i-a1wy8cvt",
                    "instance_name": "test3",
                    "status": "running",
                    "instance_group_id": "ig-ejtdp9su"
                }],
                "root_user_id": "usr-jGys5Ecd",
                "create_time": "2021-02-08T09:07:35Z",
                "relation": "attract",
                "owner": "usr-jGys5Ecd",
                "resource_project_info": [],
                "instance_group_id": "ig-ejtdp9su",
                "zone_id": "test"
            }],
            "ret_code": 0
        })

        resp_attract = self.ig_action_object.describe_instance_groups(
            instance_groups=[attract_id]
        )
        self.assertEqual(resp_attract['instance_group_set'][0]['instance_group_id'], attract_id)

    def test04_leave_instance_group(self):

        self.ig_action_object.conn.send_request = mock.Mock(return_value={
            "action": "LeaveInstanceGroupResponse",
            "job_id": "j-lxuwydwb0mk",
            "ret_code": 0
        })

        resp_repel = self.ig_action_object.leave_instance_group(
            instances=self.group_dict['repel_group'].get('instances'),
            instance_group=self.group_dict['repel_group'].get('group_id')
        )
        self.assertEqual(resp_repel['ret_code'], 0)

        self.ig_action_object.conn.send_request = mock.Mock(return_value={
            "action": "LeaveInstanceGroupResponse",
            "job_id": "j-oobmayrygpy",
            "ret_code": 0
        })

        resp_attract = self.ig_action_object.leave_instance_group(
            instances=self.group_dict['attract_group'].get('instances'),
            instance_group=self.group_dict['attract_group'].get('group_id')
        )
        self.assertEqual(resp_attract['ret_code'], 0)

    def test05_delete_instance_groups(self):

        self.ig_action_object.conn.send_request = mock.Mock(return_value={
            "action": "DeleteInstanceGroupsResponse",
            "instance_groups": ["ig-9edrghud", "ig-ejtdp9su"],
            "ret_code": 0
        })

        resp_del_groups = self.ig_action_object.delete_instance_groups(
            instance_groups=[
                self.group_dict['repel_group'].get('group_id'),
                self.group_dict['attract_group'].get('group_id')
            ]
        )
        self.assertEqual(resp_del_groups['ret_code'], 0)


if __name__ == '__main__':

    unittest.main()
