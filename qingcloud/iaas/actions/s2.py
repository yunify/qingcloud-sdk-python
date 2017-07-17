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
