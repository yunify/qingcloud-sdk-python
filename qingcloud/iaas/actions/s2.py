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


class S2Action(object):
    def __init__(self, conn):
        self.conn = conn

    def create_s2_server(self,
                         vxnet,
                         service_type,
                         s2_server_name=None,
                         s2_server_type=None,
                         private_ip=None,
                         description=None,
                         s2_class=None,
                         **ignore):
        """ Create S2 server

        :param vxnet: the ID of vxnet.
        :param service_type: valid values is vsan or vnas.
        :param s2_server_name: the name of s2 server.
        :param s2_server_type: valid values includes 0, 1, 2, 3.
        :param private_ip: you may specify the ip address of this server.
        :param description: the detailed description of the resource.
        :param s2_class: valid values includes 0, 1.
        """
        action = const.ACTION_CREATE_S2_SERVER
        valid_keys = [
            'vxnet', 'service_type', 's2_server_name', 's2_server_type',
            'private_ip', 'description', 's2_class',
        ]
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(
                body,
                integer_params=["s2_server_type", "s2_class"],
        ):
            return None

        return self.conn.send_request(action, body)

    def describe_s2_servers(self,
                            s2_servers=None,
                            service_types=None,
                            status=None,
                            search_word=None,
                            tags=None,
                            verbose=None,
                            offset=None,
                            limit=None,
                            **ignore):
        """ Describe S2 servers

        :param s2_servers: the IDs of s2 server you want to describe.
        :param service_types: the type of service, valid value is 'vsan' or 'vnas'.
        :param status: valid values include pending, active, poweroffed, suspended, deleted, ceased.
        :param search_word: you may use this field to search from id, name and description.
        :param tags: the array of IDs of tags.
        :param verbose: the number to specify the verbose level, larger the number, the more detailed information will be returned.
        :param offset: the starting offset of the returning results.
        :param limit: specify the number of the returning results.
        """
        action = const.ACTION_DESCRIBE_S2_SERVERS
        valid_keys = [
            's2_servers', 'service_types', 'status', 'search_word',
            'tags', 'verbose', 'offset', 'limit',
        ]
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(
                body,
                integer_params=["offset", "limit", "verbose"],
                list_params=["s2_servers", "service_types", "tags", "status"],
        ):
            return None

        return self.conn.send_request(action, body)

    def modify_s2_server(self,
                         s2_server,
                         s2_server_name=None,
                         description=None,
                         **ignore):
        """ Modify S2 server

        :param s2_server: the ID of s2 server.
        :param s2_server_name: the new name you want to use.
        :param description: the new value of description.
        """
        action = const.ACTION_MODIFY_S2_SERVER
        valid_keys = [
            's2_server', 's2_server_name', 'description',
        ]
        body = filter_out_none(locals(), valid_keys)

        return self.conn.send_request(action, body)

    def resize_s2_servers(self,
                          s2_servers,
                          s2_server_type,
                          **ignore):
        """ Resize S2 servers

        :param s2_servers: the IDs of s2 servers you want to resize.
        :param s2_server_type: valid values includes 0, 1, 2, 3.
        """
        action = const.ACTION_RESIZE_S2_SERVERS
        valid_keys = [
            's2_servers', 's2_server_type'
        ]
        body = filter_out_none(locals(), valid_keys)

        if not self.conn.req_checker.check_params(
                body,
                integer_params=['s2_server_type'],
                list_params=['s2_servers'],
        ):
            return None

        return self.conn.send_request(action, body)
