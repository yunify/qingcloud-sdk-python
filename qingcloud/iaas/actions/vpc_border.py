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


class VpcBorder(object):

    def __init__(self, conn):
        self.conn = conn

    def create_vpc_borders(self,
                           routers=None,
                           reset=None,
                           place_group_id=None,
                           border_type=0,
                           border=None,
                           border_name=None,
                           description=None,
                           project_id=None,
                           **params):
        """ Action: CreateVpcBorders
            @param routers: routers you want to create border.
            @param reset: reset vpc border rules.
            @param place_group_id: specify the place group id to hold the vpc border.
                                   default place group id is selected if this option does not present.
            @param border_type: the type of border, 0: vpc border, 1: intranet router.
            @param border: border id, used when reset intranet router.
            @param border_name: the short name of borders.
            @param description: the description of borders.
            @param project_id: the ID of project for vpc borders.
        """

        action = const.ACTION_CREATE_VPC_BORDERS
        valid_keys = ['routers', 'reset', 'place_group_id',
                      'border_type', 'border', 'border_name', 'description',
                      'project_id']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(
                body,
                list_params=["routers"],
                integer_params=['reset', 'border_type'],
        ):
            return None

        return self.conn.send_request(action, body)

    def delete_vpc_borders(self,
                           vpc_borders=None,
                           unlease=1,
                           project_id=None,
                           **params):
        """ Action: DeleteVpcBorders
            @param vpc_borders: IDs of vpc_borders you want to delete border.
            @param unlease: whether to unlease before terminate.
            @param project_id: the project ID of vpc borders.
        """

        action = const.ACTION_DELETE_VPC_BORDERS
        valid_keys = ['vpc_borders', 'unlease', 'project_id']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(
                body,
                required_params=['vpc_borders'],
                integer_params=['unlease'],
        ):
            return None

        return self.conn.send_request(action, body)

    def describe_vpc_borders(self,
                             vpc_borders=None,
                             status=None,
                             router_id=None,
                             l3vni=None,
                             border_type=None,
                             border_name=None,
                             verbose=0,
                             owner=None,
                             offset=None,
                             limit=None,
                             search_word=None,
                             project_id=None,
                             tags=None,
                             **params):
        """ Action: DescribeVpcBorders
            @param vpc_borders: the comma separated IDs of vpc_borders you want to describe border.
            @param status: the status of vpc border. eg: pending, available, ceased, deleted.
            @param router_id: the id of the router whose vpc_border you want to describe.
            @param l3vni: the l3vni of the router whose vpc_border you want to describe.
            @param border_type: the type of border, 0: vpc border, 1: intranet router.
            @param border_name: the short name of borders.
            @param verbose: the number to specify the verbose level, larger the number,
                            the more detailed information will be returned.
            @param owner: the owner id.
            @param offset: the starting offset of the returning results.
            @param limit: specify the number of the returning results.
            @param search_word: the search word.
            @param project_id: the project ID of vpc borders.
            @param tags: the tags of vpc borders.
        """

        action = const.ACTION_DESCRIBE_VPC_BORDERS
        valid_keys = ['vpc_borders', 'status', 'router_id', 'l3vni',
                      'border_type', 'border_name', 'verbose', 'owner',
                      'offset', 'limit', 'search_word', 'project_id', 'tags']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(
                body,
                integer_params=['l3vni', "limit", "offset",
                                "verbose"],
                list_params=["vpc_borders", "tags"],
        ):
            return None

        return self.conn.send_request(action, body)

    def join_border(self,
                    border,
                    vxnets,
                    border_private_ips=None,
                    **params):
        """ Action: JoinBorder
            @param border: the intranet router you want to join.
            @param vxnets: the ids of the vxnets that will join the intranet router.
            @param border_private_ips: specify the border private ip for each vxnet.
        """

        action = const.ACTION_JOIN_BORDER
        valid_keys = ['border', 'vxnets', 'border_private_ips']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(
                body,
                required_params=['border', 'vxnets'],
                list_params=['vxnets'],
        ):
            return None

        return self.conn.send_request(action, body)

    def leave_border(self,
                     border,
                     vxnets,
                     force=0,
                     **params):
        """ Action: LeaveBorder
            @param border: the intranet router you want to leave.
            @param vxnets: the ids of the vxnets that will leave the intranet router.
            @param force: force leave.
        """

        action = const.ACTION_LEAVE_BORDER
        valid_keys = ['border', 'vxnets', 'force']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(
                body,
                required_params=['border', 'vxnets'],
                integer_params=["force"],
                list_params=["vxnets"],
        ):
            return None

        return self.conn.send_request(action, body)

    def config_border(self,
                      border,
                      operation,
                      data=None,
                      **params):
        """ Action: ConfigBorder
            @param border: the ID of border you want to configure.
            @param operation: operation such as
                              CreateSubIf, DeleteSubIf, CheckBorderPrivateIP,
                              RemoveBgpNeighbor, AddBgpNeighbor, ConfigRoute.
            @param data: configuration data.
        """

        action = const.ACTION_CONFIG_BORDER
        valid_keys = ['border', 'operation', 'data']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(
                body,
                required_params=['border', 'operation'],
        ):
            return None

        return self.conn.send_request(action, body)

    def modify_border_attributes(self,
                                 border,
                                 border_name=None,
                                 description=None,
                                 **params):
        """ Action: ModifyBorderAttributes
            @param border: border id.
            @param border_name: the short name of borders.
            @param description: the description of borders.
        """

        action = const.ACTION_MODIFY_BORDER_ATTRIBUTES
        valid_keys = ['border', 'border_name', 'description']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(
                body,
                required_params=['border'],
        ):
            return None

        return self.conn.send_request(action, body)

    def describe_border_vxnets(self,
                               border=None,
                               vxnet=None,
                               include_vpc_vxnet=0,
                               owner=None,
                               console=None,
                               offset=None,
                               limit=None,
                               **params):
        """ Action: DescribeBorderVxnets
            @param border: filter by border.
            @param vxnet: filter by vxnet ID.
            @param include_vpc_vxnet: include vxnets within vpc associates with intranet router.
            @param owner: the id of owner.
            @param console: console.
            @param offset: the starting offset of the returning results.
            @param limit: specify the number of the returning results.
        """

        action = const.ACTION_DESCRIBE_BORDER_VXNETS
        valid_keys = ['border', 'vxnet', 'include_vpc_vxnet',
                      'owner', 'console', 'offset', 'limit']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(
                body,
                integer_params=["limit", "offset",
                                "include_vpc_vxnet"],
        ):
            return None

        return self.conn.send_request(action, body)

    def associate_border(self,
                         border,
                         router,
                         **params):
        """ Action: AssociateBorder
            @param border: the intranet router you want to associate.
            @param router: the id of the vpc router.
        """

        action = const.ACTION_ASSOCIATE_BORDER
        valid_keys = ['border', 'router']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(
                body,
                required_params=['border', 'router'],
        ):
            return None

        return self.conn.send_request(action, body)

    def dissociate_border(self,
                          border,
                          router,
                          **params):
        """ Action: DissociateBorder
            @param border: the intranet router you want to dissociate.
            @param router: the id of the vpc router.
        """

        action = const.ACTION_DISSOCIATE_BORDER
        valid_keys = ['border', 'router']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(
                body,
                required_params=['border', 'router'],
        ):
            return None

        return self.conn.send_request(action, body)

    def add_border_statics(self,
                           border,
                           statics,
                           **params):
        """ Action: AddBorderStatics
            @param border: the ID of intranet router whose statics you want to add.
            @param statics: a json string of rules list.
        """

        action = const.ACTION_ADD_BORDER_STATICS
        valid_keys = ['border', 'statics']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(
                body,
                required_params=['border', 'statics'],
        ):
            return None

        return self.conn.send_request(action, body)

    def delete_border_statics(self,
                              border_statics,
                              **params):
        """ Action: DeleteBorderStatics
            @param border_statics: border statics you want to delete.
        """

        action = const.ACTION_DELETE_BORDER_STATICS
        valid_keys = ['border_statics']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(
                body,
                required_params=['border_statics'],
                list_params=['border_statics'],
        ):
            return None

        return self.conn.send_request(action, body)

    def modify_border_static_attributes(self,
                                        border_static,
                                        border_static_name=None,
                                        val1=None,
                                        val2=None,
                                        val3=None,
                                        disabled=None,
                                        **params):
        """ Action: ModifyBorderStaticAttributes
            @param border_static: the ID of border_static whose attributes you want to update.
            @param border_static_name: the name of border_static.
            @param val1: val1.
            @param val2: val2.
            @param val3: val3.
            @param disabled: disable a border static.
        """

        action = const.ACTION_MODIFY_BORDER_STATIC_ATTRIBUTES
        valid_keys = ['border_static', 'border_static_name', 'val1',
                      'val2', 'val3', 'disabled']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(
                body,
                required_params=['border_static'],
                integer_params=['disabled'],
        ):
            return None

        return self.conn.send_request(action, body)

    def describe_border_statics(self,
                                border_statics=None,
                                border=None,
                                static_type=None,
                                owner=None,
                                offset=None,
                                limit=None,
                                verbose=None,
                                **params):
        """ Action: DescribeBorderStatics
            @param border_statics: border_statics you want to list.
            @param border: filter by owner.
            @param static_type: a list of static type. 0: route.
            @param owner: filter by owner.
            @param offset: the starting offset of the returning results.
            @param limit: specify the number of the returning results.
            @param verbose: the number to specify the verbose level, larger the
                            number, the more detailed information will be returned.
        """

        action = const.ACTION_DESCRIBE_BORDER_STATICS
        valid_keys = ['border_statics', 'border', 'static_type',
                      'owner', 'offset', 'limit', 'verbose']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(
                body,
                integer_params=['offset', 'limit', 'verbose'],
        ):
            return None

        return self.conn.send_request(action, body)

    def cancel_border_static_changes(self,
                                     border_statics=None,
                                     border=None,
                                     **params):
        """ Action: CancelBorderStaticChanges
            @param border_statics: the border statics.
            @param border: he ID of intranet router whose static changes.
        """

        action = const.ACTION_CANCEL_BORDER_STATIC_CHANGES
        valid_keys = ['border_statics', 'border']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(
                body,
        ):
            return None

        return self.conn.send_request(action, body)
