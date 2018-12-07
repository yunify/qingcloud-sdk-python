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


class TagAction(object):

    def __init__(self, conn):
        self.conn = conn

    def describe_tags(self, tags=None,
                      resources=None,
                      search_word=None,
                      owner=None,
                      verbose=0,
                      offset=None,
                      limit=None,
                      **ignore):
        """ Describe tags filtered by condition
        @param tags: IDs of the tags you want to describe.
        @param resources: IDs of the resources.
        @param verbose: the number to specify the verbose level, larger the number, the more detailed information will be returned.
        @param offset: the starting offset of the returning results.
        @param limit: specify the number of the returning results.
        """
        action = const.ACTION_DESCRIBE_TAGS
        valid_keys = ['tags', 'search_word',
                      'verbose', 'offset', 'limit', 'owner', 'resources']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=[],
                                                  integer_params=[
                                                      'offset', 'limit', 'verbose'],
                                                  list_params=['tags', 'resources']):
            return None

        return self.conn.send_request(action, body)

    def create_tag(self, tag_name, **ignore):
        """ Create a tag.
        @param tag_name: the name of the tag you want to create.
        """
        action = const.ACTION_CREATE_TAG
        valid_keys = ['tag_name']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body, required_params=['tag_name']):
            return None
        return self.conn.send_request(action, body)

    def delete_tags(self, tags, **ignore):
        """ Delete one or more tags.
        @param tags: IDs of the tags you want to delete.
        """
        action = const.ACTION_DELETE_TAGS
        body = {'tags': tags}
        if not self.conn.req_checker.check_params(body,
                                                  required_params=['tags'],
                                                  list_params=['tags']):
            return None
        return self.conn.send_request(action, body)

    def modify_tag_attributes(self, tag, tag_name=None, description=None, **ignore):
        """ Modify tag attributes.
        @param tag: the ID of tag you want to modify its attributes.
        @param tag_name: the new name of tag.
        @param description: The detailed description of the resource.
        """
        action = const.ACTION_MODIFY_TAG_ATTRIBUTES
        valid_keys = ['tag', 'tag_name', 'description']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=['tag']):
            return None
        return self.conn.send_request(action, body)

    def attach_tags(self, resource_tag_pairs, **ignore):
        """ Attach one or more tags to resources.
        @param resource_tag_pairs: the pair of resource and tag.
        it's a list-dict, such as:
        [{
        'tag_id': 'tag-hp55o9i5',
        'resource_type': 'instance',
        'resource_id': 'i-5yn6js06'
        }]
        """
        action = const.ACTION_ATTACH_TAGS
        valid_keys = ['resource_tag_pairs']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=[
                                                      'resource_tag_pairs'],
                                                  list_params=['resource_tag_pairs']):
            return None
        for pair in resource_tag_pairs:
            if not isinstance(pair, dict):
                return None
            for key in ['tag_id', 'resource_id', 'resource_type']:
                if key not in pair:
                    return None

        return self.conn.send_request(action, body)

    def detach_tags(self, resource_tag_pairs, **ignore):
        """ Detach one or more tags to resources.
        @param resource_tag_pairs: the pair of resource and tag.
        it's a list-dict, such as:
        [{
        'tag_id': 'tag-hp55o9i5',
        'resource_type': 'instance',
        'resource_id': 'i-5yn6js06'
        }]
        """
        action = const.ACTION_DETACH_TAGS
        valid_keys = ['resource_tag_pairs']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=[
                                                      'resource_tag_pairs'],
                                                  list_params=['resource_tag_pairs']):
            return None
        for pair in resource_tag_pairs:
            if not isinstance(pair, dict):
                return None
            for key in ['tag_id', 'resource_id', 'resource_type']:
                if key not in pair:
                    return None

        return self.conn.send_request(action, body)
