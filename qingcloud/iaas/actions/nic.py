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


class NicAction(object):

    def __init__(self, conn):
        self.conn = conn

    def describe_nics(self,
                      nics=None,
                      nic_name=None,
                      status=None,
                      vxnets=None,
                      vxnet_type=None,
                      offset=None,
                      limit=None,
                      **ignore):
        """ Describe nics

        @param nics: the IDs of nic you want to describe.
        @param nic_name: the name of nic.
        @param status: valid values include available, in-use.
        @param vxnets: the IDs of vxnet.
        @param vxnet_type: vxnet type, 0: unmanaged, 1: managed.
        @param offset: the starting offset of the returning results.
        @param limit: specify the number of the returning results.
        """
        action = const.ACTION_DESCRIBE_NICS
        valid_keys = [
            "nics", "nic_name", "status",
            "vxnets", "vxnet_type", "offset", "limit",
        ]
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(
                body,
                integer_params=["offset", "limit"],
                list_params=["nics", "vxnets"],
        ):
            return None

        return self.conn.send_request(action, body)

    def create_nics(self,
                    vxnet,
                    nic_name=None,
                    count=1,
                    private_ips=None,
                    **ignore):
        """ Create nics

        @param nic_name: the name of nic.
        @param vxnet: the ID of vxnet.
        @param count : the number of nics to create.
        @param private_ips: set nic"s ip, like ["192.168.100.14","192.168.100.17"]
        """
        action = const.ACTION_CREATE_NICS
        valid_keys = [
            "nic_name", "vxnet",
            "count", "private_ips",
        ]
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(
                body,
                required_params=["vxnet"],
                integer_params=["count"],
                list_params=["private_ips"],
        ):
            return None

        return self.conn.send_request(action, body)

    def attach_nics(self,
                    nics,
                    instance,
                    **ignore):
        """ Attach one or more nics to instance.

        @param nics: the IDs of nics.
        @param instance: the ID of instance.
        """
        action = const.ACTION_ATTACH_NICS
        valid_keys = ["nics", "instance"]
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(
                body,
                required_params=["nics", "instance"],
                list_params=["nics"]
        ):
            return None

        return self.conn.send_request(action, body)

    def detach_nics(self,
                    nics,
                    **ignore):
        """ Detach one or more nics from instance.

        @param nics: the IDs of nics you want to detach.
        """
        action = const.ACTION_DETACH_NICS
        valid_keys = ["nics"]
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(
                body,
                required_params=["nics"],
                list_params=["nics"]
        ):
            return None

        return self.conn.send_request(action, body)

    def modify_nic_attributes(self,
                              nic,
                              nic_name=None,
                              private_ip=None,
                              **ignore):
        """ Modify one nic's attributes

        @param nic: the ID of nic you want to modify.
        @param nic_name: the new name of nic.
        @param private_ip: the new ip address for this nic.
        """
        action = const.ACTION_MODIFY_NIC_ATTRIBUTES
        valid_keys = ["nic", "nic_name", "private_ip"]
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(
                body,
                required_params=["nic"],
        ):
            return None

        return self.conn.send_request(action, body)

    def delete_nics(self,
                    nics,
                    **ignore):
        """ Detach one or more nics from instance.

        @param nics: the IDs of nics you want to detach.
        """
        action = const.ACTION_DELETE_NICS
        valid_keys = ["nics"]
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(
                body,
                required_params=["nics"],
                list_params=["nics"]
        ):
            return None

        return self.conn.send_request(action, body)
