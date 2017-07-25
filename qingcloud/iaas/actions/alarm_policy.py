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


class AlarmPolicy(object):

    def __init__(self, conn):
        self.conn = conn

    def describe_alarm_policies(self,
                                alarm_policies=None,
                                tags=None,
                                alarm_policy_name=None,
                                alarm_policy_type=None,
                                search_word=None,
                                resource=None,
                                status=None,
                                verbose=None,
                                offset=None,
                                limit=None,
                                **ignore):
        """ Describe alarm policies

        :param alarm_policies: id IDs of alarm policies you want to describe.
        :param tags: the array of IDs of tags.
        :param alarm_policy_name: the name of alarm policy.
        :param alarm_policy_type: valid values includes instance, eip, router, loadbalancer_listener_http, loadbalancer_listener_tcp, loadbalancer_backend_http, loadbalancer_backend_tcp.
        :param search_word: you can use this field to search from id or name.
        :param resource: the ID of resource associated to this policy.
        :param status: valid values includes active, suspended.
        :param verbose: the number to specify the verbose level,
                        larger the number, the more detailed information will be returned.
        :param offset: the starting offset of the returning results.
        :param limit: specify the number of the returning results.
        """
        action = const.ACTION_DESCRIBE_ALARM_POLICIES
        valid_keys = [
            'alarm_policies', 'alarm_policy_name',
            'alarm_policy_type', 'search_word', 'resource',
            'status', 'verbose', 'offset', 'limit', 'tags',
        ]
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(
            body,
            integer_params=['offset', 'limit', 'verbose'],
            list_params=['alarm_policies', 'status', 'tags'],
        ):
            return None

        return self.conn.send_request(action, body)
