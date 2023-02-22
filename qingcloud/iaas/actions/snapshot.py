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


class SnapshotAction(object):

    def __init__(self, conn):
        self.conn = conn

    def describe_snapshots(self, snapshots=None,
                           resource_id=None,
                           snapshot_type=None,
                           root_id=None,
                           owner=None,
                           status=None,
                           verbose=0,
                           search_word=None,
                           offset=None,
                           limit=None,
                           tags=None,
                           is_manually=None,
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
        @param tags : the array of IDs of tags.
        """
        action = const.ACTION_DESCRIBE_SNAPSHOTS
        valid_keys = ['snapshots', 'resource_id', 'snapshot_type', 'root_id', 'status',
                      'verbose', 'search_word', 'offset', 'limit', 'tags', 'owner', 'is_manually']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=[],
                                                  integer_params=[
                                                      "offset", "limit", "verbose", "snapshot_type"],
                                                  list_params=["snapshots", "tags"]
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def create_snapshots(self, resources,
                         snapshot_name=None,
                         is_full=0,
                         backstore_type=None,
                         scheduler_id="",
                         **ignore):
        """ Create snapshots.
        @param resources: the IDs of resources you want to create snapshot for, the supported resource types are instance/volume.
        @param snapshot_name: the name of the snapshot.
        @param is_full: whether to create a full snapshot. 0: determined by the system. 1: should create full snapshot.
        @param backstore_type: the backstore type used to store the snapshot.
        """
        action = const.ACTION_CREATE_SNAPSHOTS
        valid_keys = ['resources', 'snapshot_name', 'is_full', 'backstore_type', 'scheduler_id']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=["resources"],
                                                  integer_params=["is_full", 'backstore_type'],
                                                  list_params=["resources"]
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def delete_snapshots(self, snapshots, merge_action=None,
                         **ignore):
        """ Delete snapshots.
        @param snapshots: the IDs of snapshots you want to delete.
        @param merge_action: commit, merge the specified increment snapshot to parent snapshot.
        """
        action = const.ACTION_DELETE_SNAPSHOTS
        valid_keys = ['snapshots', 'merge_action']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=["snapshots"],
                                                  integer_params=[],
                                                  list_params=["snapshots"]
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def apply_snapshots(self, snapshots,
                        **ignore):
        """ Apply snapshots.
        @param snapshots: the IDs of snapshots you want to apply.
        """
        action = const.ACTION_APPLY_SNAPSHOTS
        valid_keys = ['snapshots']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=["snapshots"],
                                                  integer_params=[],
                                                  list_params=["snapshots"]
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def modify_snapshot_attributes(self, snapshot,
                                   snapshot_name=None,
                                   description=None,
                                   scheduler_id=None,
                                   **ignore):
        """ Modify snapshot attributes.
        @param snapshot: the ID of snapshot whose attributes you want to modify.
        @param snapshot_name: the new snapshot name.
        @param description: the new snapshot description.
        """
        action = const.ACTION_MODIFY_SNAPSHOT_ATTRIBUTES
        valid_keys = ['snapshot', 'snapshot_name', 'description', 'scheduler_id']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=["snapshot"],
                                                  integer_params=[],
                                                  list_params=[]
                                                  ):
            return None

        return self.conn.send_request(action, body)

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
        if not self.conn.req_checker.check_params(body,
                                                  required_params=["snapshot"],
                                                  integer_params=[],
                                                  list_params=[]
                                                  ):
            return None

        return self.conn.send_request(action, body)

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
        if not self.conn.req_checker.check_params(body,
                                                  required_params=["snapshot"],
                                                  integer_params=[],
                                                  list_params=[]
                                                  ):
            return None

        return self.conn.send_request(action, body)
