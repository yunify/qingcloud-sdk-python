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

from qingcloud.conn.connection import HttpConnection
from qingcloud.misc.json_tool import json_load
from qingcloud.misc.utils import filter_out_none

import constants as const
from .consolidator import RequestChecker
from .monitor import MonitorProcessor


class APIConnection(HttpConnection):
    """
    Public connection to qingcloud service
    """
    req_checker = RequestChecker()

    def send_request(self, action, body, url = '/iaas/', verb = 'GET'):
        """ send request """
        request = body
        request['action'] = action
        request.setdefault('zone', self.zone)
        if self.expires:
            request['expires'] = self.expires
        resp = self.send(url, request, verb)
        if resp:
            return json_load(resp)

    def describe_images(self, images = None,
                              os_family = None,
                              processor_type = None,
                              status = None,
                              visibility = None,
                              provider = None,
                              verbose = 0,
                              search_word = None,
                              offset = None,
                              limit = None,
                              **ignore):
        """ Describe images filtered by condition.
        @param images: an array including IDs of the images you want to list.
                       No ID specified means list all.
        @param os_family: os family, windows/debian/centos/ubuntu.
        @param processor_type: supported processor types are `64bit` and `32bit`.
        @param status: valid values include pending, available, deleted, ceased.
        @param visibility: who can see and use this image. Valid values include public, private.
        @param provider: who provide this image, self, system.
        @param verbose: the number to specify the verbose level,
                        larger the number, the more detailed information will be returned.
        @param search_word: the search word.
        @param offset: the starting offset of the returning results.
        @param limit: specify the number of the returning results.
        """

        action = const.ACTION_DESCRIBE_IMAGES
        valid_keys = ['images', 'os_family', 'processor_type', 'status', 'visibility',
                'provider', 'verbose', 'search_word', 'offset', 'limit']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                required_params=[],
                integer_params=["offset", "limit", "verbose"],
                list_params=["images"]
                ):
            return None

        return self.send_request(action, body)

    def capture_instance(self, instance,
                               image_name = "",
                               **ignore):
        """ Capture an instance and make it available as an image for reuse.
        @param instance: ID of the instance you want to capture.
        @param image_name: short name of the image.
        """
        action = const.ACTION_CAPTURE_INSTANCE
        valid_keys = ['instance', 'image_name']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                required_params=['instance'],
                integer_params=[],
                list_params=[]
                ):
            return None

        return self.send_request(action, body)

    def delete_images(self, images,
                            **ignore):
        """ Delete one or more images whose provider is `self`.
        @param images: ID of the images you want to delete.
        """
        action = const.ACTION_DELETE_IMAGES
        body = {'images': images}
        if not self.req_checker.check_params(body,
                required_params=['images'],
                integer_params=[],
                list_params=[]
                ):
            return None

        return self.send_request(action, body)

    def modify_image_attributes(self, image,
                                      image_name = None,
                                      description = None,
                                      **ignore):
        """ Modify image attributes.
        @param image: the ID of image whose attributes you want to modify.
        @param image_name: Name of the image. It's a short name for the image
                           that more meaningful than image id.
        @param description: The detailed description of the image.
        """
        action = const.ACTION_MODIFY_IMAGE_ATTRIBUTES
        valid_keys = ['image', 'image_name', 'description']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                required_params=['image'],
                integer_params=[],
                list_params=[]
                ):
            return None

        return self.send_request(action, body)

    def describe_instances(self, instances = None,
                                 image_id = None,
                                 instance_type = None,
                                 status = None,
                                 search_word = None,
                                 verbose = 0,
                                 offset = None,
                                 limit = None,
                                 **ignore):
        """ Describe instances filtered by conditions
        @param instances : the array of IDs of instances
        @param image_id : ID of the image which is used to launch this instance.
        @param instance_type: The instance type.
        @param status : Status of the instance, including pending, running, stopped, terminated.
        @param verbose: the number to specify the verbose level, larger the number, the more detailed information will be returned.
        @param search_word: the combined search column.
        @param offset: the starting offset of the returning results.
        @param limit: specify the number of the returning results.
        """
        action = const.ACTION_DESCRIBE_INSTANCES
        valid_keys = ['instances', 'image_id', 'instance_type', 'status',
                'search_word', 'verbose', 'offset', 'limit']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                required_params=[],
                integer_params=['offset', 'limit', 'verbose'],
                list_params=['instances', 'status']
                ):
            return None

        return self.send_request(action, body)

    def run_instances(self, image_id,
                            instance_type = None,
                            cpu = None,
                            memory = None,
                            count = 1,
                            instance_name = "",
                            vxnets = None,
                            security_group = None,
                            login_mode = None,
                            login_keypair = None,
                            login_passwd = None,
                            need_newsid = False,
                            volumes = None,
                            need_userdata = 0,
                            userdata_type = None,
                            userdata_value = None,
                            userdata_path = None,
                            **ignore):
        """ Create one or more instances.
        @param image_id : ID of the image you want to use, "img-12345"
        @param instance_type: What kind of instance you want to launch. "micro", "small", "medium", "large".
        @param cpu: cpu core number.
        @param memory: memory size in MB.
        @param instance_name: a meaningful short name of instance.
        @param count : The number of instances to launch, default 1.
        @param instance_type : e.g., "micro", "small", "medium", "large".
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
        @param need_userdata: Whether to enable userdata feature. 1 for enable, 0 for disable.
        @param userdata_type: valid type is either 'plain' or 'tar'
        @param userdata_value: base64 encoded string for type 'plain'; attachment id for type 'tar'
        @param userdata_path: path of metadata and userdata.string file to be stored
        """
        action = const.ACTION_RUN_INSTANCES
        valid_keys = ['image_id', 'instance_type', 'cpu', 'memory', 'count',
                'instance_name', 'vxnets', 'security_group', 'login_mode',
                'login_keypair', 'login_passwd', 'need_newsid',
                'volumes', 'need_userdata', 'userdata_type', 'userdata_value', 'userdata_path']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                required_params=['image_id'],
                integer_params=['count', 'cpu', 'memory', 'need_newsid', 'need_userdata'],
                list_params=['volumes']
                ):
            return None

        return self.send_request(action, body)

    def terminate_instances(self, instances,
                                  **ignore):
        """ Terminate one or more instances.
        @param instances : An array including IDs of the instances you want to terminate.
        """
        action = const.ACTION_TERMINATE_INSTANCES
        body = {'instances': instances}
        if not self.req_checker.check_params(body,
                required_params=['instances'],
                integer_params=[],
                list_params=['instances']
                ):
            return None

        return self.send_request(action, body)

    def stop_instances(self, instances,
                             force=False,
                             **ignore):
        """ Stop one or more instances.
        @param instances : An array including IDs of the instances you want to stop.
        @param force: False for gracefully shutdown and True for forcibly shutdown.
        """
        action = const.ACTION_STOP_INSTANCES
        body = {'instances': instances, 'force': int(force)}
        if not self.req_checker.check_params(body,
                required_params=['instances'],
                integer_params=['force'],
                list_params=['instances']
                ):
            return None

        return self.send_request(action, body)

    def restart_instances(self, instances,
                                **ignore):
        """ Restart one or more instances.
        @param instances : An array including IDs of the instances you want to restart.
        """

        action = const.ACTION_RESTART_INSTANCES
        body = {'instances': instances}
        if not self.req_checker.check_params(body,
                required_params=['instances'],
                integer_params=[],
                list_params=['instances']
                ):
            return None

        return self.send_request(action, body)

    def start_instances(self, instances,
                              **ignore):
        """ Start one or more instances.
            @param instances : An array including IDs of the instances you want to start.
        """
        action = const.ACTION_START_INSTANCES
        body = {'instances': instances}
        if not self.req_checker.check_params(body,
                required_params=['instances'],
                integer_params=[],
                list_params=['instances']
                ):
            return None

        return self.send_request(action, body)

    def reset_instances(self, instances,
                              login_mode=None,
                              login_passwd=None,
                              login_keypair=None,
                              need_newsid=False,
                              **ignore):
        """ Reset one or monre instances to its initial state.
            @param login_mode: login mode, only supported for linux instance, valid values are "keypair", "passwd".
            @param login_passwd: if login_mode is "passwd", should be specified.
            @param login_keypair: if login_mode is "keypair", should be specified.
            @param instances : an array of instance ids you want to reset.
            @param need_newsid: Whether to generate new SID for the instance (True) or not
                                (False). Only valid for Windows instance; Silently ignored
                                for Linux instance.
        """
        action = const.ACTION_RESET_INSTANCES
        valid_keys = ['instances', 'login_mode', 'login_passwd', 'login_keypair', 'need_newsid']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                required_params=['instances'],
                integer_params=['need_newsid'],
                list_params=['instances']
                ):
            return None

        return self.send_request(action, body)

    def resize_instances(self, instances,
                               instance_type=None,
                               cpu=None,
                               memory=None,
                               **ignore):
        """ Resize one or more instances
        @param instances: the IDs of the instances you want to resize.
        @param instance_type: defined by qingcloud.
        @param cpu: cpu core number.
        @param memory: memory size in MB.
        """
        action = const.ACTION_RESIZE_INSTANCES
        valid_keys = ['instances', 'instance_type', 'cpu', 'memory']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                required_params=['instances'],
                integer_params=['cpu', 'memory'],
                list_params=['instances']
                ):
            return None

        return self.send_request(action, body)

    def modify_instance_attributes(self, instance,
                                         instance_name = None,
                                         description = None,
                                         **ignore):
        """ Modify instance attributes.
            @param instance:  the ID of instance whose attributes you want to modify.
            @param instance_name: Name of the instance. It's a short name for the instance
                                  that more meaningful than instance id.
            @param description: The detailed description of the resource.
        """
        action = const.ACTION_MODIFY_INSTANCE_ATTRIBUTES
        valid_keys = ['instance', 'instance_name', 'description']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                required_params=['instance'],
                integer_params=[],
                list_params=[]
                ):
            return None

        return self.send_request(action, body)

    def upload_userdata(self, attachment_content,
                             attachment_name = None,
                             **ignore):
        ''' Action:UploadUserDataAttachment
            @param attachment_content: base64 encoded string
            @param attachment_name: file name
        '''
        action = const.ACTION_UPLOAD_USERDATA_ATTACHMENT
        valid_keys = ['attachment_content', 'attachment_name']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                required_params=['attachment_content'],
                integer_params=[],
                list_params=[]
                ):
            return None

        return self.send_request(action, body, verb='POST')

    def describe_volumes(self, volumes = None,
                               volume_type = None,
                               instance_id = None,
                               status = None,
                               search_word = None,
                               verbose = 0,
                               offset = None,
                               limit = None,
                               **ignore):
        """ Describe volumes filtered by conditions
            @param volumes : the array of IDs of volumes.
            @param volume_type : the type of volume, 0 is high performance, 1 is high capacity
            @param instance_id: ID of the instance that volume is currently attached to, if has.
            @param status: pending, available, in-use, deleted.
            @param search_word: the combined search column.
            @param verbose: the number to specify the verbose level, larger the number, the more detailed information will be returned.
            @param offset: the starting offset of the returning results.
            @param limit: specify the number of the returning results.
        """
        valid_keys = ['volumes', 'instance_id', 'status', 'search_word',
                'volume_type', 'verbose', 'offset', 'limit']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                required_params=[],
                integer_params=['offset', 'limit', 'verbose'],
                list_params=['volumes', 'status']
                ):
            return None
        return self.send_request(const.ACTION_DESCRIBE_VOLUMES, body)

    def create_volumes(self, size,
                             volume_name = "",
                             volume_type = 0,
                             count = 1,
                             **ignore):
        """ Create one or more volumes.
            @param size : the size of each volume. Unit is GB.
            @param volume_name : the short name of volume
            @param volume_type : the type of volume, 0 is high performance, 1 is high capacity
            @param count : the number of volumes to create.
        """
        action = const.ACTION_CREATE_VOLUMES
        valid_keys = ['size', 'volume_name', 'volume_type', 'count']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                required_params=['size'],
                integer_params=['size', 'count'],
                list_params=[]
                ):
            return None

        return self.send_request(action, body)

    def delete_volumes(self, volumes,
                             **ignore):
        """ Delete one or more volumes.
            @param volumes : An array including IDs of the volumes you want to delete.
        """
        action = const.ACTION_DELETE_VOLUMES
        body = {'volumes': volumes}
        if not self.req_checker.check_params(body,
                required_params=['volumes'],
                integer_params=[],
                list_params=['volumes']
                ):
            return None

        return self.send_request(action, body)

    def attach_volumes(self, volumes,
                             instance,
                             **ignore):
        """ Attach one or more volumes to same instance
            @param volumes : an array including IDs of the volumes you want to attach.
            @param instance : the ID of instance the volumes will be attached to.
        """
        action = const.ACTION_ATTACH_VOLUMES
        valid_keys = ['volumes', 'instance']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                required_params=['volumes', 'instance'],
                integer_params=[],
                list_params=['volumes']
                ):
            return None

        return self.send_request(action, body)

    def detach_volumes(self, volumes,
                             instance,
                             **ignore):
        """ Detach one or more volumes from same instance.
            @param volumes : An array including IDs of the volumes you want to attach.
            @param instance : the ID of instance the volumes will be detached from.
        """

        action = const.ACTION_DETACH_VOLUMES
        valid_keys = ['volumes', 'instance']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                required_params=['volumes', 'instance'],
                integer_params=[],
                list_params=['volumes']
                ):
            return None

        return self.send_request(action, body)

    def resize_volumes(self, volumes,
                             size,
                             **ignore):
        """ Extend one or more volumes' size.
            @param volumes: The IDs of the volumes you want to resize.
            @param size : The new larger size of the volumes, unit is GB
        """
        action = const.ACTION_RESIZE_VOLUMES
        valid_keys = ['volumes', 'size']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                required_params=['volumes', 'size'],
                integer_params=['size'],
                list_params=['volumes']
                ):
            return None

        return self.send_request(action, body)

    def modify_volume_attributes(self, volume,
                                       volume_name = None,
                                       description = None,
                                       **ignore):
        """ Modify volume attributes.
            @param volume:  the ID of volume whose attributes you want to modify.
            @param volume_name: Name of the volume. It's a short name for
                                the volume that more meaningful than volume id.
            @param description: The detailed description of the resource.
        """
        action = const.ACTION_MODIFY_VOLUME_ATTRIBUTES
        valid_keys = ['volume', 'volume_name', 'description']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                required_params=['volume'],
                integer_params=[],
                list_params=[]
                ):
            return None

        return self.send_request(action, body)

    def describe_key_pairs(self, keypairs = None,
                                 encrypt_method = None,
                                 search_word = None,
                                 verbose = 0,
                                 offset = None,
                                 limit = None,
                                 **ignore):
        """ Describe key-pairs filtered by condition
            @param keypairs: IDs of the keypairs you want to describe.
            @param encrypt_method: encrypt method.
            @param verbose: the number to specify the verbose level, larger the number, the more detailed information will be returned.
            @param offset: the starting offset of the returning results.
            @param limit: specify the number of the returning results.
        """
        action = const.ACTION_DESCRIBE_KEY_PAIRS
        valid_keys = ['keypairs', 'encrypt_method', 'search_word', 'verbose',
                'offset', 'limit']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                required_params=[],
                integer_params=['offset', 'limit', 'verbose'],
                list_params=['keypairs']
                ):
            return None

        return self.send_request(action, body)

    def attach_keypairs(self, keypairs,
                              instances,
                              **ignore):
        """ Attach one or more keypairs to instances.
            @param keypairs: IDs of the keypairs you want to attach to instance .
            @param instances: IDs of the instances the keypairs will be attached to.
        """
        action = const.ACTION_ATTACH_KEY_PAIRS
        valid_keys = ['keypairs', 'instances']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                required_params=['keypairs', 'instances'],
                integer_params=[],
                list_params=['keypairs', 'instances']
                ):
            return None

        return self.send_request(action, body)

    def detach_keypairs(self, keypairs,
                              instances,
                              **ignore):
        """ Detach one or more keypairs from instances.
            @param keypairs: IDs of the keypairs you want to detach from instance .
            @param instances: IDs of the instances the keypairs will be detached from.
        """
        action = const.ACTION_DETACH_KEY_PAIRS
        valid_keys = ['keypairs', 'instances']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                required_params=["keypairs", "instances"],
                integer_params=[],
                list_params=["keypairs", "instances"]
                ):
            return None

        return self.send_request(action, body)

    def create_keypair(self, keypair_name,
                             mode = 'system',
                             encrypt_method = "ssh-rsa",
                             public_key = None,
                             **ignore):
        """ Create a keypair.
            @param keypair_name: the name of the keypair you want to create.
            @param mode: the keypair creation mode, "system" or "user".
            @param encrypt_method: the encrypt method, supported methods "ssh-rsa", "ssh-dss".
            @param public_key: provide your public key. (need "user" mode)
        """
        action = const.ACTION_CREATE_KEY_PAIR
        valid_keys = ['keypair_name', 'mode', 'encrypt_method', 'public_key']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                required_params=['keypair_name'],
                integer_params=[],
                list_params=[]
                ):
            return None

        return self.send_request(action, body)

    def delete_keypairs(self, keypairs,
                              **ignore):
        """ Delete one or more keypairs.
            @param keypairs: IDs of the keypairs you want to delete.
        """
        action = const.ACTION_DELETE_KEY_PAIRS
        body = {'keypairs': keypairs}
        if not self.req_checker.check_params(body,
                required_params=['keypairs'],
                integer_params=[],
                list_params=['keypairs']
                ):
            return None

        return self.send_request(action, body)

    def modify_keypair_attributes(self, keypair,
                                        keypair_name = None,
                                        description = None,
                                        **ignore):
        """ Modify keypair attributes.
            @param keypair: the ID of keypair you want to modify its attributes.
            @param keypair_name: the new name of keypair.
            @param description: The detailed description of the resource.
        """
        action = const.ACTION_MODIFY_KEYPAIR_ATTRIBUTES
        valid_keys = ['keypair', 'keypair_name', 'description']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                required_params=['keypair'],
                integer_params=[],
                list_params=[]
                ):
            return None

        return self.send_request(action, body)

    def describe_security_groups(self, security_groups = None,
                                       security_group_name = None,
                                       search_word = None,
                                       verbose = 0,
                                       offset = None,
                                       limit = None,
                                       **ignore):
        """ Describe security groups filtered by condition
            @param security_groups: IDs of the security groups you want to describe.
            @param security_group_name: the name of the security group.
            @param verbose: the number to specify the verbose level, larger the number, the more detailed information will be returned.
            @param offset: the starting offset of the returning results.
            @param limit: specify the number of the returning results.
        """
        action = const.ACTION_DESCRIBE_SECURITY_GROUPS
        valid_keys = ['security_groups', 'security_group_name', 'search_word',
                'verbose', 'offset', 'limit']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                required_params=[],
                integer_params=['offset', 'limit', 'verbose'],
                list_params=['security_groups']
                ):
            return None

        return self.send_request(action, body)

    def create_security_group(self, security_group_name,
                                    **ignore):
        """ Create a new security group without any rule.
            @param security_group_name: the name of the security group you want to create.
        """
        action = const.ACTION_CREATE_SECURITY_GROUP
        body = {'security_group_name': security_group_name}
        if not self.req_checker.check_params(body,
                required_params=['security_group_name'],
                integer_params=[],
                list_params=[]
                ):
            return None

        return self.send_request(action, body)

    def modify_security_group_attributes(self, security_group,
                                               security_group_name = None,
                                               description = None,
                                               **ignore):
        """ Modify security group attributes.
            @param security_group: the ID of the security group whose content you
                                      want to update.
            @param security_group_name: the new group name you want to update.
            @param description: The detailed description of the resource.
        """
        action = const.ACTION_MODIFY_SECURITY_GROUP_ATTRIBUTES
        valid_keys = ['security_group', 'security_group_name', 'description']
        body = filter_out_none(locals(), valid_keys)
        body['security_group'] = security_group
        if not self.req_checker.check_params(body,
                required_params=['security_group'],
                integer_params=[],
                list_params=[]
                ):
            return None

        if not self.req_checker.check_sg_rules(body.get('rules', [])):
            return None

        return self.send_request(action, body)

    def apply_security_group(self, security_group,
                                   instances = None,
                                   **ignore):
        """ Apply a security group with current rules.
            If `instances` specified, apply the security group to them,
            or will affect all instances that has applied this security group.
            @param security_group: the ID of the security group that you
                                   want to apply to instances.
            @param instances: the IDs of the instances you want to apply the security group.
        """
        action = const.ACTION_APPLY_SECURITY_GROUP
        valid_keys = ['security_group', 'instances']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                required_params=['security_group'],
                integer_params=[],
                list_params=['instances']
                ):
            return None
        return self.send_request(action, body)

    def delete_security_groups(self, security_groups,
                                     **ignore):
        """ Delete one or more security groups.
            @param security_groups: the IDs of the security groups you want to delete.
        """
        action = const.ACTION_DELETE_SECURITY_GROUPS
        body = {'security_groups': security_groups}
        if not self.req_checker.check_params(body,
                required_params=['security_groups'],
                integer_params=[],
                list_params=['security_groups']
                ):
            return None

        return self.send_request(action, body)

    def describe_security_group_rules(self, security_group = None,
                                            security_group_rules = None,
                                            direction = None,
                                            offset = None,
                                            limit = None,
                                            **ignore):
        """ Describe security group rules filtered by condition.
            @param security_group: the ID of the security group whose rules you want to describe.
            @param security_group_rules: the IDs of the security group rules you want to describe.
            @param direction: 0 for inbound; 1 for outbound
            @param offset: the starting offset of the returning results.
            @param limit: specify the number of the returning results.
        """
        action = const.ACTION_DESCRIBE_SECURITY_GROUP_RULES
        valid_keys = ['security_group', 'security_group_rules', 'direction',
                'offset', 'limit']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                required_params=[],
                integer_params=['direction', 'offset', 'limit'],
                list_params=['security_group_rules']
                ):
            return None

        return self.send_request(action, body)

    def add_security_group_rules(self, security_group,
                                       rules,
                                       **ignore):
        """ Add rules to security group.
            @param security_group: the ID of the security group whose rules you
                                      want to add.
            @param rules: a list of rules you want to add,
                          can be created by SecurityGroupRuleFactory.
        """
        action = const.ACTION_ADD_SECURITY_GROUP_RULES
        valid_keys = ['security_group', 'rules']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                required_params=['security_group', 'rules'],
                integer_params=[],
                list_params=['rules']
                ):
            return None

        if not self.req_checker.check_sg_rules(body.get('rules', [])):
            return None

        return self.send_request(action, body)

    def delete_security_group_rules(self, security_group_rules,
                                          **ignore):
        """ Delete one or more security group rules.
            @param security_group_rules: the IDs of rules you want to delete.
        """
        action = const.ACTION_DELETE_SECURITY_GROUP_RULES
        body = {'security_group_rules': security_group_rules}
        if not self.req_checker.check_params(body,
                required_params=['security_group_rules'],
                integer_params=[],
                list_params=['security_group_rules']
                ):
            return None

        return self.send_request(action, body)

    def modify_security_group_rule_attributes(self, security_group_rule,
                                                    priority=None,
                                                    security_group_rule_name=None,
                                                    rule_action=None,
                                                    direction=None,
                                                    protocol=None,
                                                    val1=None,
                                                    val2=None,
                                                    val3=None,
                                                    **ignore):
        """ Modify security group rule attributes.
            @param security_group_rule: the ID of the security group rule whose attributes you
                                      want to update.
            @param priority: priority [0 - 100].
            @param security_group_rule_name: name of the rule.

            @param rule_action: "accept" or "drop".
            @param direction: 0 for inbound; 1 for outbound.
            @param protocol: supported protocols are "icmp", "tcp", "udp", "gre".
            @param val1: for "icmp" protocol, this field is "icmp type";
                         for "tcp/udp", it's "start port", empty means all.
            @param val2: for "icmp" protocol, this field is "icmp code";
                         for "tcp/udp", it's "end port", empty means all.
            @param val3: ip network, e.g "1.2.3.0/24"
        """
        action = const.ACTION_MODIFY_SECURITY_GROUP_RULE_ATTRIBUTES
        valid_keys = ['security_group_rule', 'priority', 'security_group_rule_name',
                'rule_action', 'direction', 'protocol', 'val1', 'val2', 'val3']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                required_params=['security_group_rule'],
                integer_params=['priority'],
                list_params=[]
                ):
            return None

        return self.send_request(action, body)

    def describe_vxnets(self, vxnets = None,
                              search_word = None,
                              verbose = 0,
                              limit = None,
                              offset = None,
                              **ignore):
        """ Describe vxnets filtered by condition.
            @param vxnets: the IDs of vxnets you want to describe.
            @param verbose: the number to specify the verbose level, larger the number, the more detailed information will be returned.
            @param offset: the starting offset of the returning results.
            @param limit: specify the number of the returning results.
        """
        action = const.ACTION_DESCRIBE_VXNETS
        valid_keys = ['vxnets', 'search_word', 'verbose', 'limit', 'offset']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                required_params=[],
                integer_params=['limit', 'offset', 'verbose'],
                list_params=['vxnets']
                ):
            return None

        return self.send_request(action, body)

    def create_vxnets(self, vxnet_name,
                            vxnet_type=const.VXNET_TYPE_MANAGED,
                            count=1,
                            **ignore):
        """ Create one or more vxnets.
            @param vxnet_name: the name of vxnet you want to create.
            @param vxnet_type: vxnet type: unmanaged or managed.
            @param offset: the starting offset of the returning results.
            @param limit: specify the number of the returning results.
        """
        action = const.ACTION_CREATE_VXNETS
        valid_keys = ['vxnet_name', 'vxnet_type', 'count']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                required_params=['vxnet_name'],
                integer_params=['vxnet_type', 'count'],
                list_params=[]
                ):
            return None

        return self.send_request(action, body)

    def join_vxnet(self, vxnet,
                         instances,
                         **ignore):
        """ One or more instances join the vxnet.
            @param vxnet : the id of vxnet you want the instances to join.
            @param instances : the IDs of instances that will join vxnet.
        """

        action = const.ACTION_JOIN_VXNET
        valid_keys = ['vxnet', 'instances']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                required_params=['vxnet', 'instances'],
                integer_params=[],
                list_params=['instances']
                ):
            return None

        return self.send_request(action, body)

    def leave_vxnet(self, vxnet,
                          instances,
                          **ignore):
        """ One or more instances leave the vxnet.
            @param vxnet : The id of vxnet that the instances will leave.
            @param instances : the IDs of instances that will leave vxnet.
        """
        action = const.ACTION_LEAVE_VXNET
        valid_keys = ['vxnet', 'instances']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                required_params=['vxnet', 'instances'],
                integer_params=[],
                list_params=['instances']
                ):
            return None

        return self.send_request(action, body)

    def delete_vxnets(self, vxnets,
                            **ignore):
        """ Delete one or more vxnets.
            @param vxnets: the IDs of vxnets you want to delete.
        """
        action = const.ACTION_DELETE_VXNETS
        body = {'vxnets': vxnets}
        if not self.req_checker.check_params(body,
                required_params=['vxnets'],
                integer_params=[],
                list_params=['vxnets']
                ):
            return None

        return self.send_request(action, body)

    def modify_vxnet_attributes(self, vxnet,
                                      vxnet_name = None,
                                      description = None,
                                      **ignore):
        """ Modify vxnet attributes
            @param vxnet: the ID of vxnet you want to modify its attributes.
            @param vxnet_name: the new name of vxnet.
            @param description: The detailed description of the resource.
        """
        action = const.ACTION_MODIFY_VXNET_ATTRIBUTES
        valid_keys = ['vxnet', 'vxnet_name', 'description']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                required_params=['vxnet'],
                integer_params=[],
                list_params=[]
                ):
            return None

        return self.send_request(action, body)

    def describe_vxnet_instances(self, vxnet,
                                       instances = None,
                                       image = None,
                                       instance_type = None,
                                       status = None,
                                       limit = None,
                                       offset = None,
                                       **ignore):
        """ Describe instances in vxnet.
            @param vxnet: the ID of vxnet whose instances you want to describe.
            @param image: filter by image ID.
            @param instances: filter by instance ID.
            @param instance_type: filter by instance type
            @param status: filter by status
            @param offset: the starting offset of the returning results.
            @param limit: specify the number of the returning results.
        """
        action = const.ACTION_DESCRIBE_VXNET_INSTANCES
        valid_keys = ['vxnet', 'instances', 'image', 'instance_type', 'status',
                'limit', 'offset']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                required_params=['vxnet'],
                integer_params=['limit', 'offset'],
                list_params=['instances']
                ):
            return None

        return self.send_request(action, body)

    def describe_routers(self, routers = None,
                               vxnet = None,
                               status = None,
                               verbose = 0,
                               search_word = None,
                               limit = None,
                               offset = None,
                               **ignore):
        """ Describe routers filtered by condition.
            @param routers: the IDs of the routers you want to describe.
            @param vxnet: the ID of vxnet you want to describe.
            @param verbose: the number to specify the verbose level, larger the number, the more detailed information will be returned.
            @param offset: the starting offset of the returning results.
            @param limit: specify the number of the returning results.
        """
        action = const.ACTION_DESCRIBE_ROUTERS
        valid_keys = ['routers', 'vxnet', 'status', 'verbose', 'search_word',
                'limit', 'offset']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                required_params=[],
                integer_params=['limit', 'offset', 'verbose'],
                list_params=['routers']
                ):
            return None

        return self.send_request(action, body)

    def create_routers(self, count=1,
                             router_name=None,
                             security_group=None,
                             **ignore):
        """ Create one or more routers.
            @param router_name: the name of the router.
            @param security_group: the ID of the security_group you want to apply to router.
            @param count: the count of router you want to create.
        """
        action = const.ACTION_CREATE_ROUTERS
        valid_keys = ['count', 'router_name', 'security_group']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                required_params=[],
                integer_params=['count'],
                list_params=[]
                ):
            return None

        return self.send_request(action, body)

    def delete_routers(self, routers,
                             **ignore):
        """ Delete one or more routers.
            @param routers: the IDs of routers you want to delete.
        """
        action = const.ACTION_DELETE_ROUTERS
        body = {'routers': routers}
        if not self.req_checker.check_params(body,
                required_params=['routers'],
                integer_params=[],
                list_params=['routers']
                ):
            return None

        return self.send_request(action, body)

    def update_routers(self, routers,
                             **ignore):
        """ Update one or more routers.
            @param routers: the IDs of routers you want to update.
        """
        action = const.ACTION_UPDATE_ROUTERS
        body = {'routers': routers}
        if not self.req_checker.check_params(body,
                required_params=['routers'],
                integer_params=[],
                list_params=['routers']
                ):
            return None

        return self.send_request(action, body)

    def poweroff_routers(self, routers,
                               **ignore):
        """ Poweroff one or more routers.
            @param routers: the IDs of routers you want to poweroff.
        """
        action = const.ACTION_POWEROFF_ROUTERS
        body = {'routers': routers}
        if not self.req_checker.check_params(body,
                required_params=['routers'],
                integer_params=[],
                list_params=['routers']
                ):
            return None

        return self.send_request(action, body)

    def poweron_routers(self, routers,
                              **ignore):
        """ Poweron one or more routers.
            @param routers: the IDs of routers you want to poweron.
        """
        action = const.ACTION_POWERON_ROUTERS
        body = {'routers': routers}
        if not self.req_checker.check_params(body,
                required_params=['routers'],
                integer_params=[],
                list_params=['routers']
                ):
            return None

        return self.send_request(action, body)

    def join_router(self, vxnet,
                          router,
                          ip_network,
                          manager_ip=None,
                          dyn_ip_start=None,
                          dyn_ip_end=None,
                          features=1,
                          **ignore):
        """ Connect vxnet to router.
            @param vxnet: the ID of vxnet that will join the router.
            @param router: the ID of the router the vxnet will join.
            @param ip_network: the ip network in CSI format.
            @param manager_ip: can be provided if DHCP feature is enabled.
            @param dyn_ip_start: starting IP that allocated from DHCP server.
            @param dyn_ip_end: ending IP that allocated from DHCP server.
            @param features: the feature the vxnet will enable in the router.
                             1 - dhcp server.
        """
        action = const.ACTION_JOIN_ROUTER
        valid_keys = ['vxnet', 'router', 'ip_network', 'manager_ip',
                'dyn_ip_start', 'dyn_ip_end', 'features']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                required_params=['vxnet', 'router', 'ip_network'],
                integer_params=['features'],
                list_params=[]
                ):
            return None

        return self.send_request(action, body)

    def leave_router(self, router,
                           vxnets,
                           **ignore):
        """ Disconnect vxnets from router.
            @param vxnets: the IDs of vxnets that will leave the router.
            @param router: the ID of the router the vxnet will leave.
        """
        action = const.ACTION_LEAVE_ROUTER
        valid_keys = ['router', 'vxnets']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                required_params=['vxnets', 'router'],
                integer_params=[],
                list_params=['vxnets']
                ):
            return None

        return self.send_request(action, body)

    def modify_router_attributes(self, router,
                                       vxnet=None,
                                       eip=None,
                                       security_group=None,
                                       router_name=None,
                                       description=None,
                                       features=None,
                                       dyn_ip_start=None,
                                       dyn_ip_end=None,
                                       **ignore):
        """ Modify router attributes.
            @param router: the ID of router you want to modify its attributes.
            @param vxnet: the ID of vxnet whose feature you want to modify.
            @param eip: the eip.
            @param security_group: the ID of the security_group you want to apply to router.
            @param router_name: the name of the router.
            @param description: the description of the router.
            @param features: the features of vxnet you want to re-define. 1: enable DHCP; 0: disable DHCP
            @param dyn_ip_start: starting IP that allocated from DHCP server
            @param dyn_ip_end: ending IP that allocated from DHCP server
        """
        action = const.ACTION_MODIFY_ROUTER_ATTRIBUTES
        valid_keys = ['router', 'vxnet', 'eip', 'security_group', 'features',
                'router_name', 'description', 'dyn_ip_start', 'dyn_ip_end']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                required_params=['router'],
                integer_params=[],
                list_params=[]
                ):
            return None

        return self.send_request(action, body)

    def describe_router_vxnets(self, router=None,
                                     vxnet=None,
                                     limit=None,
                                     offset=None,
                                     **ignore):
        """ Describe vxnets in router.
            @param router: filter by router ID.
            @param vxnet: filter by vxnet ID.
            @param offset: the starting offset of the returning results.
            @param limit: specify the number of the returning results.
        """
        action = const.ACTION_DESCRIBE_ROUTER_VXNETS
        valid_keys = ['router', 'vxnet', 'limit', 'offset']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                required_params=[],
                integer_params=['limit', 'offset'],
                list_params=[]
                ):
            return None

        return self.send_request(action, body)

    def describe_router_statics(self, router_statics = None,
                                      router = None,
                                      vxnet = None,
                                      static_type = None,
                                      limit = None,
                                      offset = None,
                                      **ignore):
        """ Describe router statics filtered by condition.
            @param router_statics: the IDs of the router statics you want to describe.
            @param router: filter by router ID.
            @param vxnet: filter by vxnet ID.
            @param static_type: defined in `RouterStaticFactory`.
            @param offset: the starting offset of the returning results.
            @param limit: specify the number of the returning results.
        """
        action = const.ACTION_DESCRIBE_ROUTER_STATICS
        valid_keys = ['router_statics', 'router', 'vxnet', 'static_type',
                'limit', 'offset']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                required_params=[],
                integer_params=['limit', 'offset', 'static_type'],
                list_params=[]
                ):
            return None

        return self.send_request(action, body)

    def add_router_statics(self, router,
                                 statics,
                                 **ignore):
        """ Add statics to router.
            @param router: the ID of the router whose statics you want to add.
            @param statics: a list of statics you want to add,
                            can be created by RouterStaticFactory.
        """
        action = const.ACTION_ADD_ROUTER_STATICS
        valid_keys = ['router', 'statics']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                required_params=['router', 'statics'],
                integer_params=[],
                list_params=['statics']
                ):
            return None

        if not self.req_checker.check_router_statics(body.get('statics', [])):
            return None

        return self.send_request(action, body)

    def delete_router_statics(self, router_statics,
                                    **ignore):
        """ Delete one or more router statics.
            @param router_statics: the IDs of router statics you want to delete.
        """
        action = const.ACTION_DELETE_ROUTER_STATICS
        body = {'router_statics': router_statics}
        if not self.req_checker.check_params(body,
                required_params=['router_statics'],
                integer_params=[],
                list_params=['router_statics']
                ):
            return None

        return self.send_request(action, body)

    def describe_eips(self, eips = None,
                            status = None,
                            instance_id = None,
                            search_word = None,
                            offset = None,
                            limit = None,
                            **ignore):
        """ Describe eips filtered by condition.
            @param eips: IDs of the eip you want describe.
            @param status: filter eips by status
            @param instance_id: filter eips by instance.
            @param search_word: search word column.
            @param offset: the starting offset of the returning results.
            @param limit: specify the number of the returning results.
        """
        action = const.ACTION_DESCRIBE_EIPS
        valid_keys = ['eips', 'status', 'instance_id', 'search_word',
                'offset', 'limit']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                required_params=[],
                integer_params=['offset', 'limit'],
                list_params=['status', 'eips']
                ):
            return None

        return self.send_request(action, body)

    def associate_eip(self, eip,
                            instance,
                            **ignore):
        """ Associate an eip on an instance.
            @param eip: The id of eip you want to associate with instance.
            @param instance: the id of instance you want to associate eip.
        """
        action = const.ACTION_ASSOCIATE_EIP
        body = {'eip': eip, 'instance': instance}
        if not self.req_checker.check_params(body,
                required_params=['eip', 'instance'],
                integer_params=[],
                list_params=[]
                ):
            return None

        return self.send_request(action, body)

    def dissociate_eips(self, eips,
                              **ignore):
        """ Dissociate one or more eips.
            @param eips: The ids of eips you want to dissociate with instance.
        """
        action = const.ACTION_DISSOCIATE_EIPS
        body = {'eips': eips}
        if not self.req_checker.check_params(body,
                required_params=['eips'],
                integer_params=[],
                list_params=['eips']
                ):
            return None

        return self.send_request(action, body)

    def allocate_eips(self, bandwidth,
                            count=1,
                            need_icp=0,
                            eip_name='',
                            **ignore):
        """ Allocate one or more eips.
            @param count: the number of eips you want to allocate.
            @param bandwidth: the bandwidth of the eip in Mbps.
            @param need_icp:
            @param eip_name : the short name of eip
        """
        action = const.ACTION_ALLOCATE_EIPS
        valid_keys = ['bandwidth', 'count', 'need_icp', 'eip_name']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                required_params=['bandwidth'],
                integer_params=['bandwidth', 'count', 'need_icp'],
                list_params=[]
                ):
            return None

        return self.send_request(action, body)

    def release_eips(self, eips,
                           force=0,
                           **ignore):
        """ Release one or more eips.
            @param eips : The ids of eips that you want to release
            @param force : Whether to force release the eip that needs icp codes.
        """
        action = const.ACTION_RELEASE_EIPS
        body = {'eips': eips, 'force': int(force != 0)}
        if not self.req_checker.check_params(body,
                required_params=['eips'],
                integer_params=['force'],
                list_params=['eips']
                ):
            return None

        return self.send_request(action, body)

    def change_eips_bandwidth(self, eips,
                                    bandwidth,
                                    **ignore):
        """ Change one or more eips bandwidth.
            @param eips: The IDs of the eips whose bandwidth you want to change.
            @param bandwidth: the new bandwidth of the eip in MB.
        """
        action = const.ACTION_CHANGE_EIPS_BANDWIDTH
        body = {'eips': eips, 'bandwidth': bandwidth}
        if not self.req_checker.check_params(body,
                required_params=['eips', 'bandwidth'],
                integer_params=['bandwidth'],
                list_params=['eips']
                ):
            return None

        return self.send_request(action, body)

    def modify_eip_attributes(self, eip,
                                    eip_name=None,
                                    description=None,
                                    **ignore):
        """ Modify eip attributes.
            If you want to modify eip's bandwidth, use `change_eips_bandwidth`.

            @param eip : the ID of eip that you want to modify
            @param eip_name : the name of eip
            @param description : the eip description
        """
        action = const.ACTION_MODIFY_EIP_ATTRIBUTES
        valid_keys = ['eip', 'eip_name', 'description']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                required_params=['eip'],
                integer_params=[],
                list_params=[]
                ):
            return None

        return self.send_request(action, body)

    def describe_loadbalancers(self, loadbalancers=None,
                                      status=None,
                                      verbose=0,
                                      search_word=None,
                                      offset=None,
                                      limit=None,
                                      **ignore):
        """ Describe loadbalancers filtered by condition.

            @param loadbalancers : the array of load balancer IDs.
            @param status: pending, active, stopped, deleted, suspended, ceased
            @param verbose: the number to specify the verbose level, larger the number, the more detailed information will be returned.
            @param search_word: search word column.
            @param offset: the starting offset of the returning results.
            @param limit: specify the number of the returning results.
        """
        action = const.ACTION_DESCRIBE_LOADBALANCERS
        valid_keys = ['loadbalancers', 'status', 'verbose', 'search_word',
                'offset', 'limit']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                required_params=[],
                integer_params=['offset', 'limit'],
                list_params=['loadbalancers', 'status']
                ):
            return None

        return self.send_request(action, body)

    def create_loadbalancer(self, eips,
                                  loadbalancer_name=None,
                                  security_group=None,
                                  **ignore):
        """ Create new load balancer.

            @param eips: the IDs of the eips that will be associated to load balancer.
            @param loadbalancer_name: the name of the loadbalancer.
            @param security_group: the id of the security_group you want to apply to loadbalancer,
                                   use `default security` group as default.
        """
        action = const.ACTION_CREATE_LOADBALANCER
        valid_keys = ['eips', 'loadbalancer_name', 'security_group']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                required_params=['eips'],
                integer_params=[],
                list_params=['loadbalancers']
                ):
            return None

        return self.send_request(action, body)

    def delete_loadbalancers(self, loadbalancers,
                                   **ignore):
        """ Delete one or more load balancers.
            @param loadbalancers: the IDs of load balancers you want to delete.
        """
        action = const.ACTION_DELETE_LOADBALANCERS
        body = {'loadbalancers': loadbalancers}
        if not self.req_checker.check_params(body,
                required_params=['loadbalancers'],
                integer_params=[],
                list_params=[]
                ):
            return None

        return self.send_request(action, body)

    def stop_loadbalancers(self, loadbalancers,
                                 **ignore):
        """ Stop one or more load balancers.

            @param loadbalancers: the array of load balancer IDs.
        """
        action = const.ACTION_STOP_LOADBALANCERS
        body = {'loadbalancers': loadbalancers}
        if not self.req_checker.check_params(body,
                required_params=['loadbalancers'],
                integer_params=[],
                list_params=['loadbalancers']
                ):
            return None

        return self.send_request(action, body)

    def start_loadbalancers(self, loadbalancers,
                                  **ignore):
        """ Start one or more load balancers.

            @param loadbalancers: the array of load balancer IDs.
        """
        action = const.ACTION_START_LOADBALANCERS
        body = {'loadbalancers': loadbalancers}
        if not self.req_checker.check_params(body,
                required_params=['loadbalancers'],
                integer_params=[],
                list_params=['loadbalancers']
                ):
            return None

        return self.send_request(action, body)

    def update_loadbalancers(self, loadbalancers,
                                   **ignore):
        """ Update one or more load balancers.

            @param loadbalancers: the array of load balancer IDs.
        """
        action = const.ACTION_UPDATE_LOADBALANCERS
        body = {'loadbalancers': loadbalancers}
        if not self.req_checker.check_params(body,
                required_params=['loadbalancers'],
                integer_params=[],
                list_params=['loadbalancers']
                ):
            return None

        return self.send_request(action, body)

    def associate_eips_to_loadbalancer(self, loadbalancer,
                                              eips,
                                              **ignore):
        """ Associate one or more eips to load balancer.

            @param loadbalancer: the ID of load balancer.
            @param eips: the array of eip IDs.
        """
        action = const.ACTION_ASSOCIATE_EIPS_TO_LOADBALANCER
        body = {'loadbalancer': loadbalancer, 'eips': eips}
        if not self.req_checker.check_params(body,
                required_params=['loadbalancer', 'eips'],
                integer_params=[],
                list_params=['eips']
                ):
            return None

        return self.send_request(action, body)

    def dissociate_eips_from_loadbalancer(self, loadbalancer,
                                                eips,
                                                **ignore):
        """ Dissociate one or more eips from load balancer.

            @param loadbalancer: the ID of load balancer.
            @param eips: the array of eip IDs.
        """
        action = const.ACTION_DISSOCIATE_EIPS_FROM_LOADBALANCER
        body = {'loadbalancer': loadbalancer, 'eips': eips}
        if not self.req_checker.check_params(body,
                required_params=['loadbalancer', 'eips'],
                integer_params=[],
                list_params=['eips']
                ):
            return None

        return self.send_request(action, body)

    def modify_loadbalancer_attributes(self, loadbalancer,
                                             security_group=None,
                                             loadbalancer_name=None,
                                             description=None,
                                             **ignore):
        """ Modify load balancer attributes.

            @param loadbalancer: the ID of loadbalancer you want to modify.
            @param security_group: the ID of the security_group.
            @param loadbalancer_name: the name of the loadbalancer.
            @param description: the description of the loadbalancer.
        """
        action = const.ACTION_MODIFY_LOADBALANCER_ATTRIBUTES
        valid_keys = ['loadbalancer', 'security_group', 'loadbalancer_name',
                'description']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                required_params=['loadbalancer'],
                integer_params=[],
                list_params=[]
                ):
            return None

        return self.send_request(action, body)

    def describe_loadbalancer_listeners(self, loadbalancer_listeners=None,
                                              loadbalancer=None,
                                              verbose=0,
                                              limit=None,
                                              offset=None,
                                              **ignore):
        """ Describe load balancer listeners by filter condition.

            @param loadbalancer_listeners: filter by load balancer listener IDs.
            @param loadbalancer: filter by loadbalancer ID.
            @param verbose: the number to specify the verbose level, larger the number, the more detailed information will be returned.
            @param offset: the starting offset of the returning results.
            @param limit: specify the number of the returning results.
        """
        action = const.ACTION_DESCRIBE_LOADBALANCER_LISTENERS
        valid_keys = ['loadbalancer_listeners', 'loadbalancer', 'verbose',
                'limit', 'offset']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                required_params=[],
                integer_params=['verbose', 'limit', 'offset'],
                list_params=['loadbalancer_listeners']
                ):
            return None

        return self.send_request(action, body)

    def add_listeners_to_loadbalancer(self, loadbalancer,
                                            listeners,
                                            **ignore):

        """ Add listeners to load balancer.

            @param loadbalancer: The ID of loadbalancer.
            @param listeners: the listeners to add.
        """
        action = const.ACTION_ADD_LOADBALANCER_LISTENERS
        valid_keys = ['listeners', 'loadbalancer']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                required_params=['loadbalancer', 'listeners'],
                integer_params=[],
                list_params=['listeners']
                ):
            return None

        self.req_checker.check_lb_listeners(listeners)

        return self.send_request(action, body)

    def delete_loadbalancer_listeners(self, loadbalancer_listeners,
                                            **ignore):

        """ Delete load balancer listeners.

            @param loadbalancer_listeners: the array of listener IDs.
        """
        action = const.ACTION_DELETE_LOADBALANCER_LISTENERS
        body = {'loadbalancer_listeners': loadbalancer_listeners}
        if not self.req_checker.check_params(body,
                required_params=[],
                integer_params=[],
                list_params=['loadbalancer_listeners']
                ):
            return None

        return self.send_request(action, body)

    def modify_loadbalancer_listener_attributes(self, loadbalancer_listener,
                                                      loadbalancer_listener_name=None,
                                                      balance_mode=None,
                                                      forwardfor=None,
                                                      healthy_check_method=None,
                                                      healthy_check_option=None,
                                                      session_sticky=None,
                                                      **ignore):
        """ Modify load balancer listener attributes

            @param loadbalancer_listener: the ID of listener.
            @param loadbalancer_listener_name: the name of the listener.
            @param balance_mode: defined in constants.py,
                        BALANCE_ROUNDROBIN, BALANCE_LEASTCONN
            @param forwardfor: extra http headers, represented as bitwise flag defined in constants.py,
                        HEADER_QC_LB_IP, HEADER_QC_LB_ID and HEADER_X_FORWARD_FOR.
                        Example: if you need X-Forwarded-For and QC-LB-IP in http header,
                        then forwardfor should be HEADER_X_FORWARD_FOR | HEADER_QC_LB_IP.
            @param description: the description of the listener.
        """
        action = const.ACTION_MODIFY_LOADBALANCER_LISTENER_ATTRIBUTES
        valid_keys = ['loadbalancer_listener', 'loadbalancer_listener_name',
                'balance_mode', 'forwardfor', 'healthy_check_method',
                'healthy_check_option', 'session_sticky']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                required_params=['loadbalancer_listener'],
                integer_params=['forwardfor'],
                list_params=[]
                ):
            return None

        if body.has_key('healthy_check_method'):
            self.req_checker.check_lb_listener_healthy_check_method(
                    body['healthy_check_method'])
        if body.has_key('healthy_check_option'):
            self.req_checker.check_lb_listener_healthy_check_option(
                    body['healthy_check_option'])

        return self.send_request(action, body)

    def describe_loadbalancer_backends(self, loadbalancer_backends=None,
                                             loadbalancer_listener=None,
                                             loadbalancer=None,
                                             verbose=0,
                                             limit=None,
                                             offset=None,
                                             **ignore):
        """ Describe load balancer backends.

            @param loadbalancer_backends: filter by load balancer backends ID.
            @param loadbalancer_listener: filter by load balancer listener ID.
            @param loadbalancer: filter by load balancer ID.
            @param verbose: the number to specify the verbose level, larger the number, the more detailed information will be returned.
            @param offset: the starting offset of the returning results.
            @param limit: specify the number of the returning results.
        """
        action = const.ACTION_DESCRIBE_LOADBALANCER_BACKENDS
        valid_keys = ['loadbalancer_backends', 'loadbalancer_listener',
                'loadbalancer', 'verbose', 'limit', 'offset']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                required_params=[],
                integer_params=['verbose', 'limit', 'offset'],
                list_params=['loadbalancer_backends']
                ):
            return None

        return self.send_request(action, body)

    def add_backends_to_listener(self, loadbalancer_listener,
                                       backends,
                                       **ignore):
        """ Add one or more backends to load balancer listener.

            @param loadbalancer_listener: the ID of load balancer listener
            @param backends: the load balancer backends to add
        """
        action = const.ACTION_ADD_LOADBALANCER_BACKENDS
        body = {'loadbalancer_listener': loadbalancer_listener, 'backends': backends}
        if not self.req_checker.check_params(body,
                required_params=['loadbalancer_listener', 'backends'],
                integer_params=[],
                list_params=['backends']
                ):
            return None

        self.req_checker.check_lb_backends(backends)

        return self.send_request(action, body)

    def delete_loadbalancer_backends(self, loadbalancer_backends,
                                           **ignore):
        """ Delete load balancer backends.

            @param loadbalancer_backends: the array of backends IDs.
        """
        action = const.ACTION_DELETE_LOADBALANCER_BACKENDS
        body = {'loadbalancer_backends': loadbalancer_backends}
        if not self.req_checker.check_params(body,
                required_params=['loadbalancer_backends'],
                integer_params=[],
                list_params=['loadbalancer_backends']
                ):
            return None

        return self.send_request(action, body)

    def modify_loadbalancer_backend_attributes(self, loadbalancer_backend,
                                                     loadbalancer_backend_name=None,
                                                     port=None,
                                                     weight=None,
                                                     **ignore):
        """ Modify load balancer backend attributes.

            @param loadbalancer_backend: the ID of backend.
            @param loadbalancer_backend_name: the name of the backend.
            @param port: backend server listen port.
            @param weight: backend server weight, valid range is from 1 to 100.
        """
        action = const.ACTION_MODIFY_LOADBALANCER_BACKEND_ATTRIBUTES
        valid_keys = ['loadbalancer_backend', 'loadbalancer_backend_name',
                'port', 'weight']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                required_params=['loadbalancer_backend'],
                integer_params=['port', 'weight'],
                list_params=[]
                ):
            return None

        if body.has_key('port'):
            self.req_checker.check_lb_backend_port(body['port'])
        if body.has_key('weight'):
            self.req_checker.check_lb_backend_weight(body['weight'])

        return self.send_request(action, body)

    def get_monitoring_data(self, resource,
                                  meters,
                                  step,
                                  start_time,
                                  end_time,
                                  decompress=False,
                                  **ignore):
        """ Get resource monitoring data.

            @param resource: the ID of resource, can be instance_id, volume_id, eip_id or router_id.
            @param meters: list of metering types you want to get.
                           If resource is instance, meter can be "cpu", "disk-os", "memory",
                           "disk-%s" % attached_volume_id, "if-%s" % vxnet_mac_address.
                           If resource is volume, meter should be "disk-%s" % volume_id.
                           If resource is eip, meter should be "traffic".
                           If resource is router, meter can be "vxnet-0" and joint vxnet ID.
            @param step: The metering time step, valid steps: "5m", "15m", "30m", "1h", "2h", "1d".
            @param start_time: the starting UTC time, in the format YYYY-MM-DDThh:mm:ssZ.
            @param end_time: the ending UTC time, in the format YYYY-MM-DDThh:mm:ssZ.
        """
        action = const.ACTION_GET_MONITOR
        valid_keys = ['resource', 'meters', 'step', 'start_time', 'end_time']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                required_params=['resource', 'meters', 'step', 'start_time', 'end_time'],
                integer_params=[],
                datetime_params=['start_time', 'end_time'],
                list_params=['meters']
                ):
            return None

        resp = self.send_request(action, body)
        if resp and resp.get('meter_set') and decompress:
            p = MonitorProcessor(resp['meter_set'], start_time, end_time, step)
            resp['meter_set'] = p.decompress_monitoring_data()
        return resp

    def get_loadbalancer_monitoring_data(self, resource,
                                               meters,
                                               step,
                                               start_time,
                                               end_time,
                                               decompress=False,
                                               **ignore):
        """ Get load balancer monitoring data.

            @param resource: the ID of resource, can be loadbalancer_id, listener_id or backend_id.
            @param meters: list of metering types you want to get, valid values: request, traffic.
            @param step: The metering time step, valid steps: "5m", "15m", "30m", "1h", "2h", "1d".
            @param start_time: the starting UTC time, in the format YYYY-MM-DDThh:mm:ssZ.
            @param end_time: the ending UTC time, in the format YYYY-MM-DDThh:mm:ssZ.
        """
        action = const.ACTION_GET_LOADBALANCER_MONITOR
        valid_keys = ['resource', 'meters', 'step', 'start_time', 'end_time']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                required_params=['resource', 'meters', 'step', 'start_time', 'end_time'],
                integer_params=[],
                datetime_params=['start_time', 'end_time'],
                list_params=['meters']
                ):
            return None

        resp = self.send_request(action, body)
        if resp and resp.get('meter_set') and decompress:
            p = MonitorProcessor(resp['meter_set'], start_time, end_time, step)
            resp['meter_set'] = p.decompress_lb_monitoring_data()
        return resp

    def describe_snapshots(self, snapshots = None,
                                 resource_id = None,
                                 snapshot_type = None,
                                 root_id = None,
                                 status = None,
                                 verbose = 0,
                                 search_word = None,
                                 offset = None,
                                 limit = None,
                                 **ignore):
        """ Describe snapshots filtered by condition.

        @param snapshots: an array including IDs of the snapshots you want to list.
                           No ID specified means list all.
        @param resource_id: filter by resource ID.
        @param snapshot_type: filter by snapshot type. 0: incremantal snapshot, 1: full snapshot.
        @param root_id: filter by snapshot root ID.
        @param status: valid values include pending, available, suspended, deleted, ceased.
        @param verbose: the number to specify the verbose level,
                        larger the number, the more detailed information will be returned.
        @param search_word: the search word.
        @param offset: the starting offset of the returning results.
        @param limit: specify the number of the returning results.
        """
        action = const.ACTION_DESCRIBE_SNAPSHOTS
        valid_keys = ['snapshots', 'resource_id', 'snapshot_type', 'root_id', 'status',
                      'verbose', 'search_word', 'offset', 'limit']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                required_params=[],
                integer_params=["offset", "limit", "verbose", "snapshot_type"],
                list_params=["snapshots"]
                ):
            return None

        return self.send_request(action, body)

    def create_snapshots(self, resources,
                               snapshot_name=None,
                               is_full=0,
                               **ignore):
        """ Create snapshots.

        @param resources: the IDs of resources you want to create snapshot for, the supported resource types are instance/volume.
        @param snapshot_name: the name of the snapshot.
        @param is_full: whether to create a full snapshot. 0: determined by the system. 1: should create full snapshot.
        """
        action = const.ACTION_CREATE_SNAPSHOTS
        valid_keys = ['resources', 'snapshot_name', 'is_full']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                required_params=["resources"],
                integer_params=["is_full"],
                list_params=["resources"]
                ):
            return None

        return self.send_request(action, body)

    def delete_snapshots(self, snapshots,
                               **ignore):
        """ Delete snapshots.

        @param snapshots: the IDs of snapshots you want to delete.
        """
        action = const.ACTION_DELETE_SNAPSHOTS
        valid_keys = ['snapshots']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                required_params=["snapshots"],
                integer_params=[],
                list_params=["snapshots"]
                ):
            return None

        return self.send_request(action, body)

    def apply_snapshots(self, snapshots,
                               **ignore):
        """ Apply snapshots.

        @param snapshots: the IDs of snapshots you want to apply.
        """
        action = const.ACTION_APPLY_SNAPSHOTS
        valid_keys = ['snapshots']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                required_params=["snapshots"],
                integer_params=[],
                list_params=["snapshots"]
                ):
            return None

        return self.send_request(action, body)

    def modify_snapshot_attributes(self, snapshot,
                                         snapshot_name=None,
                                         description=None,
                                         **ignore):
        """ Modify snapshot attributes.

        @param snapshot: the ID of snapshot whose attributes you want to modify.
        @param snapshot_name: the new snapshot name.
        @param description: the new snapshot description.
        """
        action = const.ACTION_MODIFY_SNAPSHOT_ATTRIBUTES
        valid_keys = ['snapshot', 'snapshot_name', 'description']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                required_params=["snapshot"],
                integer_params=[],
                list_params=[]
                ):
            return None

        return self.send_request(action, body)

    def capture_instance_from_snapshot(self, snapshot,
                                             image_name=None,
                                             **ignore):
        """ Capture instance from snapshot.

        @param snapshot: the ID of snapshot you want to export as an image, this snapshot should be created from an instance.
        @param image_name: the image name.
        """
        action = const.ACTION_CAPTURE_INSTANCE_FROM_SNAPSHOT
        valid_keys = ['snapshot', 'image_name']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                required_params=["snapshot"],
                integer_params=[],
                list_params=[]
                ):
            return None

        return self.send_request(action, body)

    def create_volume_from_snapshot(self, snapshot,
                                          volume_name=None,
                                          **ignore):
        """ Create volume from snapshot.

        @param snapshot: the ID of snapshot you want to export as an volume, this snapshot should be created from a volume.
        @param volume_name: the volume name.
        """
        action = const.ACTION_CREATE_VOLUME_FROM_SNAPSHOT
        valid_keys = ['snapshot', 'volume_name']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                required_params=["snapshot"],
                integer_params=[],
                list_params=[]
                ):
            return None

        return self.send_request(action, body)
