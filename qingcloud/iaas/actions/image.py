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


class ImageAction(object):

    def __init__(self, conn):
        self.conn = conn

    def describe_images(self, images=None,
                        tags=None,
                        os_family=None,
                        processor_type=None,
                        status=None,
                        visibility=None,
                        provider=None,
                        verbose=0,
                        search_word=None,
                        owner=None,
                        offset=None,
                        limit=None,
                        **ignore):
        """ Describe images filtered by condition.
        @param images: an array including IDs of the images you want to list.
                       No ID specified means list all.
        @param tags: the array of IDs of tags.
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
                      'provider', 'verbose', 'search_word', 'offset', 'limit', 'owner',
                      'tags']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=[],
                                                  integer_params=[
                                                      "offset", "limit", "verbose"],
                                                  list_params=["images", "tags"]
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def capture_instance(self, instance,
                         image_name="",
                         **ignore):
        """ Capture an instance and make it available as an image for reuse.
        @param instance: ID of the instance you want to capture.
        @param image_name: short name of the image.
        """
        action = const.ACTION_CAPTURE_INSTANCE
        valid_keys = ['instance', 'image_name']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=['instance'],
                                                  integer_params=[],
                                                  list_params=[]
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def delete_images(self, images,
                      **ignore):
        """ Delete one or more images whose provider is `self`.
        @param images: ID of the images you want to delete.
        """
        action = const.ACTION_DELETE_IMAGES
        body = {'images': images}
        if not self.conn.req_checker.check_params(body,
                                                  required_params=['images'],
                                                  integer_params=[],
                                                  list_params=[]
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def modify_image_attributes(self, image,
                                image_name=None,
                                description=None,
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
        if not self.conn.req_checker.check_params(body,
                                                  required_params=['image'],
                                                  integer_params=[],
                                                  list_params=[]
                                                  ):
            return None

        return self.conn.send_request(action, body)
