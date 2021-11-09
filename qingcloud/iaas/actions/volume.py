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


class VolumeAction(object):

    def __init__(self, conn):
        self.conn = conn

    def describe_volumes(self, volumes=None,
                         volume_type=None,
                         instance_id=None,
                         status=None,
                         owner=None,
                         search_word=None,
                         verbose=0,
                         offset=None,
                         limit=None,
                         tags=None,
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
        @param tags : the array of IDs of tags.
        """
        valid_keys = ['volumes', 'instance_id', 'status', 'search_word',
                      'volume_type', 'verbose', 'offset', 'limit', 'tags', 'owner']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=[],
                                                  integer_params=[
                                                      'offset', 'limit', 'verbose'],
                                                  list_params=[
                                                      'volumes', 'status', 'tags']
                                                  ):
            return None
        return self.conn.send_request(const.ACTION_DESCRIBE_VOLUMES, body)

    def create_volumes(self, size,
                       volume_name="",
                       volume_type=0,
                       count=1,
                       target_user=None,
                       round_up=0,
                       **ignore):
        """ Create one or more volumes.
        @param size : the size of each volume. Unit is GB.
        @param volume_name : the short name of volume
        @param volume_type : the type of volume, 0 is high performance, 1 is high capacity
        @param count : the number of volumes to create.
        @param target_user: ID of user who will own this resource, should be one of your sub-accounts
        @param round_up: The volume size will round up to the minimum size if it's samller than the minimum size
        """
        action = const.ACTION_CREATE_VOLUMES
        valid_keys = ['size', 'volume_name', 'volume_type', 'count', 'target_user', 'round_up']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=['size'],
                                                  integer_params=['size', 'count'],
                                                  list_params=[]
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def delete_volumes(self, volumes,
                       **ignore):
        """ Delete one or more volumes.
        @param volumes : An array including IDs of the volumes you want to delete.
        """
        action = const.ACTION_DELETE_VOLUMES
        body = {'volumes': volumes}
        if not self.conn.req_checker.check_params(body,
                                                  required_params=['volumes'],
                                                  integer_params=[],
                                                  list_params=['volumes']
                                                  ):
            return None

        return self.conn.send_request(action, body)

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
        if not self.conn.req_checker.check_params(body,
                                                  required_params=[
                                                      'volumes', 'instance'],
                                                  integer_params=[],
                                                  list_params=['volumes']
                                                  ):
            return None

        return self.conn.send_request(action, body)

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
        if not self.conn.req_checker.check_params(body,
                                                  required_params=[
                                                      'volumes', 'instance'],
                                                  integer_params=[],
                                                  list_params=['volumes']
                                                  ):
            return None

        return self.conn.send_request(action, body)

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
        if not self.conn.req_checker.check_params(body,
                                                  required_params=[
                                                      'volumes', 'size'],
                                                  integer_params=['size'],
                                                  list_params=['volumes']
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def modify_volume_attributes(self, volume,
                                 volume_name=None,
                                 description=None,
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
        if not self.conn.req_checker.check_params(body,
                                                  required_params=['volume'],
                                                  integer_params=[],
                                                  list_params=[]
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def clone_volumes(self,
                      zone,
                      volume,
                      volume_name="",
                      volume_type=None,
                      count=1,
                      **ignore):
        """ Clone an existed volume to one or more new volumes.
        @param zone: the ID of zone for new volume.
        @param volume: the ID of volume you want to clone.
        @param volume_name: name of the volume. It's a short name for
        the volume that more meaningful than volume id.
        @param volume_type: type of the volume.
        @param count: how many volumes will be created.
        """
        action = const.ACTION_CLONE_VOLUMES
        valid_keys = ['zone', 'volume', 'volume_name', 'volume_type', 'count']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=['zone', 'volume'],
                                                  integer_params=['count'],
                                                  list_params=[]
                                                  ):
            return None

        return self.conn.send_request(action, body)
