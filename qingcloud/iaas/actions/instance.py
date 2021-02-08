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

from qingcloud.iaas import constants as const
from qingcloud.misc.utils import filter_out_none


class InstanceAction(object):

    def __init__(self, conn):
        self.conn = conn

    def describe_instances(self, instances=None,
                           image_id=None,
                           instance_type=None,
                           status=None,
                           owner=None,
                           search_word=None,
                           verbose=0,
                           offset=None,
                           limit=None,
                           tags=None,
                           **ignore):
        """ Describe instances filtered by conditions
        @param instances : the array of IDs of instances
        @param image_id : ID of the image which is used to launch this instance.
        @param instance_type: The instance type.
                              See: https://docs.qingcloud.com/api/common/includes/instance_type.html
        @param status : Status of the instance, including pending, running, stopped, terminated.
        @param verbose: the number to specify the verbose level, larger the number, the more detailed information will be returned.
        @param search_word: the combined search column.
        @param offset: the starting offset of the returning results.
        @param limit: specify the number of the returning results.
        @param tags : the array of IDs of tags.
        """
        action = const.ACTION_DESCRIBE_INSTANCES
        valid_keys = ['instances', 'image_id', 'instance_type', 'status',
                      'search_word', 'verbose', 'offset', 'limit', 'tags', 'owner']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=[],
                                                  integer_params=[
                                                      'offset', 'limit', 'verbose'],
                                                  list_params=[
                                                      'instances', 'status', 'tags']
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def run_instances(self, image_id,
                      instance_type=None,
                      cpu=None,
                      memory=None,
                      count=1,
                      instance_name="",
                      vxnets=None,
                      security_group=None,
                      login_mode=None,
                      login_keypair=None,
                      login_passwd=None,
                      need_newsid=False,
                      volumes=None,
                      cpu_model=None,
                      need_userdata=0,
                      userdata_type=None,
                      userdata_value=None,
                      userdata_path=None,
                      instance_class=None,
                      hostname=None,
                      target_user=None,
                      nic_mqueue=0,
                      cpu_max=None,
                      mem_max=None,
                      os_disk_size=None,
                      **ignore):
        """ Create one or more instances.
        @param image_id : ID of the image you want to use, "img-12345"
        @param instance_type: What kind of instance you want to launch.
        See: https://docs.qingcloud.com/api/common/includes/instance_type.html
        @param cpu: cpu core number.
        @param memory: memory size in MB.
        @param instance_name: a meaningful short name of instance.
        @param count : The number of instances to launch, default 1.
        @param vxnets : The IDs of vxnets the instance will join.
        @param security_group: The ID of security group that will apply to instance.
        @param login_mode: ssh login mode, "keypair" or "passwd"
        @param login_keypair: login keypair id
        @param login_passwd: login passwd
        @param need_newsid: Whether to generate new SID for the instance (True) or not
        (False). Only valid for Windows instance; Silently ignored
        for Linux instance.
        @param volumes: the IDs of volumes you want to attach to newly created instance,
        parameter only affected when count = 1.
        @param cpu_model: the type of cpu architecture.
        @param need_userdata: Whether to enable userdata feature. 1 for enable, 0 for disable.
        @param userdata_type: valid type is either 'plain' or 'tar'
        @param userdata_value: base64 encoded string for type 'plain'; attachment id for type 'tar'
        @param userdata_path: path of metadata and userdata.string file to be stored
        @param instance_class: 0 is performance; 1 is high performance
        @param target_user: ID of user who will own this resource, should be one of your sub-accounts
        @param nic_mqueue: enable NIC multi-queue
        @param cpu_max: max cpu core number.
        @param mem_max: max memory size in MB.
        @param os_disk_size: operation system disk size in GB.
        """
        action = const.ACTION_RUN_INSTANCES
        valid_keys = ['image_id', 'instance_type', 'cpu', 'memory', 'count',
                      'instance_name', 'vxnets', 'security_group', 'login_mode',
                      'login_keypair', 'login_passwd', 'need_newsid',
                      'volumes', 'need_userdata', 'userdata_type',
                      'userdata_value', 'userdata_path', 'instance_class',
                      'hostname', 'target_user', 'nic_mqueue', 'cpu_max', 'mem_max',
                      'os_disk_size', 'cpu_model'
                      ]
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=['image_id'],
                                                  integer_params=['count', 'cpu', 'memory', 'need_newsid',
                                                                  'need_userdata', 'instance_class', 'os_disk_size',
                                                                  'nic_mqueue', 'cpu_max', 'mem_max'],
                                                  list_params=['volumes']
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def run_instances_by_configuration(self, launch_configuration,
                                       instance_name='',
                                       count=1,
                                       volumes=None,
                                       **ignore):
        """ Run one or more instances by launch configuration.
        @param launch_configuration: ID of launch configuration you want to use
        @param instance_name: a meaningful short name of instance.
        @param count : The number of instances to launch, default 1.
        @param volumes: the ids of volumes will be attached.
        """
        action = const.ACTION_RUN_INSTANCES_BY_CONFIGURATION
        valid_keys = ['launch_configuration', 'instance_name', 'count', 'volumes']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=[
                                                      'launch_configuration'],
                                                  integer_params=['count'],
                                                  list_params=['volumes']
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def terminate_instances(self, instances,
                            direct_cease=0,
                            **ignore):
        """ Terminate one or more instances.
        @param instances : An array including IDs of the instances you want to terminate.
        @param direct_cease: whether to keep deleted resource in recycle bin (direct_cease=0) or not (direct_cease=1).
        """
        action = const.ACTION_TERMINATE_INSTANCES
        valid_keys = ['instances', 'direct_cease']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=['instances'],
                                                  integer_params=['direct_cease'],
                                                  list_params=['instances']
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def stop_instances(self, instances,
                       force=False,
                       **ignore):
        """ Stop one or more instances.
        @param instances : An array including IDs of the instances you want to stop.
        @param force: False for gracefully shutdown and True for forcibly shutdown.
        """
        action = const.ACTION_STOP_INSTANCES
        body = {'instances': instances, 'force': int(force)}
        if not self.conn.req_checker.check_params(body,
                                                  required_params=['instances'],
                                                  integer_params=['force'],
                                                  list_params=['instances']
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def restart_instances(self, instances,
                          **ignore):
        """ Restart one or more instances.
        @param instances : An array including IDs of the instances you want to restart.
        """

        action = const.ACTION_RESTART_INSTANCES
        body = {'instances': instances}
        if not self.conn.req_checker.check_params(body,
                                                  required_params=['instances'],
                                                  integer_params=[],
                                                  list_params=['instances']
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def start_instances(self, instances,
                        **ignore):
        """ Start one or more instances.
        @param instances : An array including IDs of the instances you want to start.
        """
        action = const.ACTION_START_INSTANCES
        body = {'instances': instances}
        if not self.conn.req_checker.check_params(body,
                                                  required_params=['instances'],
                                                  integer_params=[],
                                                  list_params=['instances']
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def reset_instances(self, instances,
                        login_mode=None,
                        login_passwd=None,
                        login_keypair=None,
                        need_newsid=False,
                        **ignore):
        """ Reset one or monre instances to its initial state.
        @param login_mode: login mode, only supported for linux instance, valid values are "keypair", "passwd".
        param login_passwd: if login_mode is "passwd", should be specified.
        @param login_keypair: if login_mode is "keypair", should be specified.
        @param instances : an array of instance ids you want to reset.
        @param need_newsid: Whether to generate new SID for the instance (True) or not
        (False). Only valid for Windows instance; Silently ignored
        for Linux instance.
        """
        action = const.ACTION_RESET_INSTANCES
        valid_keys = ['instances', 'login_mode',
                      'login_passwd', 'login_keypair', 'need_newsid']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=['instances'],
                                                  integer_params=['need_newsid'],
                                                  list_params=['instances']
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def resize_instances(self, instances,
                         instance_type=None,
                         cpu=None,
                         memory=None,
                         os_disk_size=None,
                         **ignore):
        """ Resize one or more instances
        @param instances: the IDs of the instances you want to resize.
        @param instance_type: defined by qingcloud.
        See: https://docs.qingcloud.com/api/common/includes/instance_type.html
        @param cpu: cpu core number.
        @param memory: memory size in MB.
        @param os_disk_size: operation system disk size in GB.
        """
        action = const.ACTION_RESIZE_INSTANCES
        valid_keys = ['instances', 'instance_type', 'cpu', 'memory', 'os_disk_size']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=['instances'],
                                                  integer_params=['cpu', 'memory', 'os_disk_size'],
                                                  list_params=['instances']
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def modify_instance_attributes(self, instance,
                                   instance_name=None,
                                   description=None,
                                   nic_mqueue=None,
                                   **ignore):
        """ Modify instance attributes.
        @param instance:  the ID of instance whose attributes you want to modify.
        @param instance_name: Name of the instance. It's a short name for the instance
        that more meaningful than instance id.
        @param nic_mqueue: Enable or disable multiqueue.
        @param description: The detailed description of the resource.
        """
        action = const.ACTION_MODIFY_INSTANCE_ATTRIBUTES
        valid_keys = ['instance', 'instance_name', 'description', 'nic_mqueue']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=['instance'],
                                                  integer_params=['nic_mqueue'],
                                                  list_params=[]
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def upload_userdata(self, attachment_content,
                        attachment_name=None,
                        **ignore):
        """ Action:UploadUserDataAttachment
        @param attachment_content: base64 encoded string
        @param attachment_name: file name
        """
        action = const.ACTION_UPLOAD_USERDATA_ATTACHMENT
        valid_keys = ['attachment_content', 'attachment_name']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=[
                                                      'attachment_content'],
                                                  integer_params=[],
                                                  list_params=[]
                                                  ):
            return None

        return self.conn.send_request(action, body, verb='POST')

    def clone_instances(self,
                        instances,
                        vxnets=None,
                        **ignore):
        """ Clone one or more instances
        @param instances: the IDs of the instances you want to clone.
        @param vxnets: which vxnet will the new instance join,
            value formatted as ["i-xxxxxx1|vxnet-xxxxx1","i-xxxxx2|vxnet-xxxx2"]
        """
        action = const.ACTION_CLONE_INSTANCES
        valid_keys = ['instances', 'vxnets']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=['instances'],
                                                  list_params=['instances', 'vxnets']
                                                  ):
            return None

        return self.conn.send_request(action, body)
