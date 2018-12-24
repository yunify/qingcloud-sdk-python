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


class RouterAction(object):

    def __init__(self, conn):
        self.conn = conn

    def describe_routers(self, routers=None,
                         vxnet=None,
                         status=None,
                         verbose=0,
                         owner=None,
                         search_word=None,
                         limit=None,
                         offset=None,
                         tags=None,
                         **ignore):
        """ Describe routers filtered by condition.
        @param routers: the IDs of the routers you want to describe.
        @param vxnet: the ID of vxnet you want to describe.
        @param verbose: the number to specify the verbose level, larger the number, the more detailed information will be returned.
        @param offset: the starting offset of the returning results.
        @param limit: specify the number of the returning results.
        @param tags : the array of IDs of tags.
        """
        action = const.ACTION_DESCRIBE_ROUTERS
        valid_keys = ['routers', 'vxnet', 'status', 'verbose', 'search_word',
                      'limit', 'offset', 'tags', 'owner']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=[],
                                                  integer_params=[
                                                      'limit', 'offset', 'verbose'],
                                                  list_params=['routers', 'tags']
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def create_routers(self, count=1,
                       router_name=None,
                       security_group=None,
                       vpc_network=None,
                       router_type=None,
                       **ignore):
        """ Create one or more routers.
        @param router_name: the name of the router.
        @param security_group: the ID of the security_group you want to apply to router.
        @param count: the count of router you want to create.
        @param vpc_network: VPC IP addresses range, currently support "192.168.0.0/16" or "172.16.0.0/16", required in zone pek3a.
        @param router_type: 0 - Medium, 1 - Small, 2 - large, 3 - extra-large (default is 1).
        """
        action = const.ACTION_CREATE_ROUTERS
        valid_keys = ['count', 'router_name', 'security_group', 'vpc_network', 'router_type']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=[],
                                                  integer_params=['count'],
                                                  list_params=[]
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def delete_routers(self, routers,
                       **ignore):
        """ Delete one or more routers.
        @param routers: the IDs of routers you want to delete.
        """
        action = const.ACTION_DELETE_ROUTERS
        body = {'routers': routers}
        if not self.conn.req_checker.check_params(body,
                                                  required_params=['routers'],
                                                  integer_params=[],
                                                  list_params=['routers']
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def update_routers(self, routers,
                       **ignore):
        """ Update one or more routers.
        @param routers: the IDs of routers you want to update.
        """
        action = const.ACTION_UPDATE_ROUTERS
        body = {'routers': routers}
        if not self.conn.req_checker.check_params(body,
                                                  required_params=['routers'],
                                                  integer_params=[],
                                                  list_params=['routers']
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def poweroff_routers(self, routers,
                         **ignore):
        """ Poweroff one or more routers.
        @param routers: the IDs of routers you want to poweroff.
        """
        action = const.ACTION_POWEROFF_ROUTERS
        body = {'routers': routers}
        if not self.conn.req_checker.check_params(body,
                                                  required_params=['routers'],
                                                  integer_params=[],
                                                  list_params=['routers']
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def poweron_routers(self, routers,
                        **ignore):
        """ Poweron one or more routers.
        @param routers: the IDs of routers you want to poweron.
        """
        action = const.ACTION_POWERON_ROUTERS
        body = {'routers': routers}
        if not self.conn.req_checker.check_params(body,
                                                  required_params=['routers'],
                                                  integer_params=[],
                                                  list_params=['routers']
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def join_router(self, vxnet,
                    router,
                    ip_network,
                    manager_ip=None,
                    dyn_ip_start=None,
                    dyn_ip_end=None,
                    features=1,
                    **ignore):
        """ Connect vxnet to router.
        @param vxnet: the ID of vxnet that will join the router.
        @param router: the ID of the router the vxnet will join.
        @param ip_network: the ip network in CSI format.
        @param manager_ip: can be provided if DHCP feature is enabled.
        @param dyn_ip_start: starting IP that allocated from DHCP server.
        @param dyn_ip_end: ending IP that allocated from DHCP server.
        @param features: the feature the vxnet will enable in the router.
        1 - dhcp server.
        """
        action = const.ACTION_JOIN_ROUTER
        valid_keys = ['vxnet', 'router', 'ip_network', 'manager_ip',
                      'dyn_ip_start', 'dyn_ip_end', 'features']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=[
                                                      'vxnet', 'router', 'ip_network'],
                                                  integer_params=['features'],
                                                  list_params=[]
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def leave_router(self, router,
                     vxnets,
                     **ignore):
        """ Disconnect vxnets from router.
        @param vxnets: the IDs of vxnets that will leave the router.
        @param router: the ID of the router the vxnet will leave.
        """
        action = const.ACTION_LEAVE_ROUTER
        valid_keys = ['router', 'vxnets']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=[
                                                      'vxnets', 'router'],
                                                  integer_params=[],
                                                  list_params=['vxnets']
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def modify_router_attributes(self, router,
                                 vxnet=None,
                                 eip=None,
                                 security_group=None,
                                 router_name=None,
                                 description=None,
                                 features=None,
                                 dyn_ip_start=None,
                                 dyn_ip_end=None,
                                 **ignore):
        """ Modify router attributes.
        @param router: the ID of router you want to modify its attributes.
        @param vxnet: the ID of vxnet whose feature you want to modify.
        @param eip: the eip.
        @param security_group: the ID of the security_group you want to apply to router.
        @param router_name: the name of the router.
        @param description: the description of the router.
        @param features: the features of vxnet you want to re-define. 1: enable DHCP; 0: disable DHCP
        @param dyn_ip_start: starting IP that allocated from DHCP server
        @param dyn_ip_end: ending IP that allocated from DHCP server
        """
        action = const.ACTION_MODIFY_ROUTER_ATTRIBUTES
        valid_keys = ['router', 'vxnet', 'eip', 'security_group', 'features',
                      'router_name', 'description', 'dyn_ip_start', 'dyn_ip_end']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=['router'],
                                                  integer_params=[],
                                                  list_params=[]
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def describe_router_vxnets(self, router=None,
                               vxnet=None,
                               limit=None,
                               offset=None,
                               **ignore):
        """ Describe vxnets in router.
        @param router: filter by router ID.
        @param vxnet: filter by vxnet ID.
        @param offset: the starting offset of the returning results.
        @param limit: specify the number of the returning results.
        """
        action = const.ACTION_DESCRIBE_ROUTER_VXNETS
        valid_keys = ['router', 'vxnet', 'limit', 'offset']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=[],
                                                  integer_params=[
                                                      'limit', 'offset'],
                                                  list_params=[]
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def modify_router_static_attributes(self, router_static,
                                        router_static_name=None,
                                        val1=None,
                                        val2=None,
                                        val3=None,
                                        val4=None,
                                        val5=None,
                                        val6=None,
                                        disabled=None,
                                        **ignore):
        """ Modify router static attributes.
        @param router_static: the ID of router static you want to modify its attributes.
        @param val1 - val6: please see the doc. https://docs.qingcloud.com/api/router/modify_router_static_attributes.html
        @param disabled: disable the static when this is 1, or 0 to enable it.
        """
        action = const.ACTION_MODIFY_ROUTER_STATIC_ATTRIBUTES
        valid_keys = ['router_static', 'router_static_name', 'disabled',
                      'val1', 'val2', 'val3', 'val4', 'val5', 'val6']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=['router_static'],
                                                  integer_params=[],
                                                  list_params=[]
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def describe_router_statics(self, router_statics=None,
                                router=None,
                                vxnet=None,
                                static_type=None,
                                limit=None,
                                offset=None,
                                **ignore):
        """ Describe router statics filtered by condition.
        @param router_statics: the IDs of the router statics you want to describe.
        @param router: filter by router ID.
        @param vxnet: filter by vxnet ID.
        @param static_type: defined in `RouterStaticFactory`.
        @param offset: the starting offset of the returning results.
        @param limit: specify the number of the returning results.
        """
        action = const.ACTION_DESCRIBE_ROUTER_STATICS
        valid_keys = ['router_statics', 'router', 'vxnet', 'static_type',
                      'limit', 'offset']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=[],
                                                  integer_params=[
                                                      'limit', 'offset', 'static_type'],
                                                  list_params=[]
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def add_router_statics(self, router,
                           statics,
                           **ignore):
        """ Add statics to router.
        @param router: the ID of the router whose statics you want to add.
        @param statics: a list of statics you want to add,
        can be created by RouterStaticFactory.
        """
        action = const.ACTION_ADD_ROUTER_STATICS
        valid_keys = ['router', 'statics']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=[
                                                      'router', 'statics'],
                                                  integer_params=[],
                                                  list_params=['statics']
                                                  ):
            return None

        if not self.conn.req_checker.check_router_statics(body.get('statics', [])):
            return None

        return self.conn.send_request(action, body)

    def delete_router_statics(self, router_statics,
                              **ignore):
        """ Delete one or more router statics.
        @param router_statics: the IDs of router statics you want to delete.
        """
        action = const.ACTION_DELETE_ROUTER_STATICS
        body = {'router_statics': router_statics}
        if not self.conn.req_checker.check_params(body,
                                                  required_params=[
                                                      'router_statics'],
                                                  integer_params=[],
                                                  list_params=['router_statics']
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def modify_router_static_entry_attributes(self,
                                              router_static_entry,
                                              router_static_entry_name=None,
                                              val1=None,
                                              val2=None,
                                              **ignore):
        """ Modify router static entry attributes.
        @param router_static_entry: the ID of router static entry you want to modify.
        @param router_static_entry_name: the new name of router static entry.
        @param val1 - val2: please see the doc. https://docs.qingcloud.com/api/router/modify_router_static_entry_attributes.html
        """
        action = const.ACTION_MODIFY_ROUTER_STATIC_ENTRY_ATTRIBUTES
        valid_keys = ['router_static_entry', 'router_static_entry_name',
                      'val1', 'val2']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=[
                                                      'router_static_entry'],
                                                  integer_params=[],
                                                  list_params=[]
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def describe_router_static_entries(self,
                                       router_static_entries=None,
                                       router_static=None,
                                       limit=None,
                                       offset=None,
                                       **ignore):
        """ Describe router static entries filtered by condition.
        @param router_static_entries: the IDs of the router static entries you want to describe.
        @param router_static: filter by router static ID.
        @param offset: the starting offset of the returning results.
        @param limit: specify the number of the returning results.
        """
        action = const.ACTION_DESCRIBE_ROUTER_STATIC_ENTRIES
        valid_keys = ['router_static_entries', 'router_static',
                      'limit', 'offset']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=[],
                                                  integer_params=[
                                                      'limit', 'offset'],
                                                  list_params=[]
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def add_router_static_entries(self,
                                  router_static,
                                  entries,
                                  **ignore):
        """ Add entries to router static.
        @param router_static: the ID of the router static you want to add.
        @param entries: a list of entries you want to add.
        """
        action = const.ACTION_ADD_ROUTER_STATIC_ENTRIES
        valid_keys = ['router_static', 'entries']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=[
                                                      'router_static', 'entries'],
                                                  integer_params=[],
                                                  list_params=['entries']
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def delete_router_static_entries(self,
                                     router_static_entries,
                                     **ignore):
        """ Delete one or more router static entries.
        @param router_static_entries: the IDs of router static entries you want to delete.
        """
        action = const.ACTION_DELETE_ROUTER_STATIC_ENTRIES
        body = {'router_static_entries': router_static_entries}
        if not self.conn.req_checker.check_params(body,
                                                  required_params=[
                                                      'router_static_entries'],
                                                  integer_params=[],
                                                  list_params=[
                                                      'router_static_entries']
                                                  ):
            return None

        return self.conn.send_request(action, body)
