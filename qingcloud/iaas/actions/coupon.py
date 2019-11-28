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


class CouponAction(object):

    def __init__(self, conn):
        self.conn = conn

    def issue_coupons(self,
                      to_user_id,
                      value,
                      category,
                      sub_category=None,
                      remarks=None,
                      **ignore):
        """ Issue coupons to user.
        """
        action = const.ACTION_ISSUE_COUPONS
        valid_keys = ["to_user_id", "category", "sub_category",
                      "remarks", "value"]
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=["to_user_id", "value"],
                                                  integer_params=["value"],
                                                  list_params=[]):
            return None

        return self.conn.send_request(action, body)
