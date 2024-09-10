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
import random
import sys
import time
import uuid

from qingcloud.iaas.actions.instance import InstanceAction
from qingcloud.iaas.actions.instance_groups import InstanceGroupsAction
from qingcloud.iaas.actions.volume import VolumeAction
from qingcloud.iaas.actions.eip import EipAction
from qingcloud.iaas.actions.router import RouterAction
from qingcloud.iaas.actions.vxnet import VxnetAction
from qingcloud.iaas.actions.keypair import KeypairAction
from qingcloud.iaas.actions.image import ImageAction
from qingcloud.iaas.actions.loadbalancer import LoadBalancerAction
from qingcloud.iaas.actions.security_group import SecurityGroupAction
from qingcloud.iaas.actions.snapshot import SnapshotAction
from qingcloud.iaas.actions.tag import TagAction
from qingcloud.iaas.actions.alarm_policy import AlarmPolicy
from qingcloud.iaas.actions.cluster import ClusterAction
from qingcloud.iaas.actions.nic import NicAction
from qingcloud.iaas.actions.s2 import S2Action
from qingcloud.iaas.actions.sdwan import SdwanAction
from qingcloud.iaas.actions.migrate import MigrateAction
from qingcloud.iaas.actions.vpc_border import VpcBorder

from qingcloud.conn.auth import QuerySignatureAuthHandler
from qingcloud.conn.connection import HttpConnection, HTTPRequest
from qingcloud.misc.json_tool import json_load, json_dump
from qingcloud.misc.utils import filter_out_none
from . import constants as const
from .consolidator import RequestChecker
from .monitor import MonitorProcessor
from .errors import InvalidAction


class APIConnection(HttpConnection):
    """ Public connection to qingcloud service
    """
    req_checker = RequestChecker()

    def __init__(self, qy_access_key_id, qy_secret_access_key, zone,
                 host="api.qingcloud.com", port=443, protocol="https",
                 pool=None, expires=None,
                 retry_time=2, http_socket_timeout=60, debug=False,
                 credential_proxy_host="169.254.169.254", credential_proxy_port=80):
        """
        @param qy_access_key_id - the access key id
        @param qy_secret_access_key - the secret access key
        @param zone - the zone id to access
        @param host - the host to make the connection to
        @param port - the port to use when connect to host
        @param protocol - the protocol to access to web server, "http" or "https"
        @param pool - the connection pool
        @param retry_time - the retry_time when message send fail
        """
        # Set default zone
        self.zone = zone
        # Set retry times
        self.retry_time = retry_time

        super(APIConnection, self).__init__(
            qy_access_key_id, qy_secret_access_key, host, port, protocol,
            pool, expires, http_socket_timeout, debug, credential_proxy_host, credential_proxy_port)

        if not self.qy_access_key_id and not self.qy_secret_access_key:
            self._check_token()

        else:
            self._auth_handler = QuerySignatureAuthHandler(self.host,
                                                           self.qy_access_key_id, self.qy_secret_access_key)

        # other apis
        self.actions = [
            InstanceAction(self),
            InstanceGroupsAction(self),
            VolumeAction(self),
            EipAction(self),
            RouterAction(self),
            VxnetAction(self),
            LoadBalancerAction(self),
            KeypairAction(self),
            SecurityGroupAction(self),
            SnapshotAction(self),
            ImageAction(self),
            TagAction(self),
            NicAction(self),
            AlarmPolicy(self),
            S2Action(self),
            ClusterAction(self),
            SdwanAction(self),
            MigrateAction(self),
            VpcBorder(self),
        ]

    def send_request(self, action, body, url="/iaas/", verb="GET"):
        """ Send request
        """
        request = body
        request['action'] = action
        request.setdefault('zone', self.zone)
        if self.debug:
            print(json_dump(request))
            sys.stdout.flush()
        if self.expires:
            request['expires'] = self.expires

        retry_time = 0
        while retry_time < self.retry_time:
            # Use binary exponential backoff to desynchronize client requests
            next_sleep = random.random() * (2 ** retry_time)
            try:
                response = self.send(verb, url, request)
                if response.status == 200:
                    resp_str = response.read()
                    if type(resp_str) != str:
                        resp_str = resp_str.decode()
                    if self.debug:
                        print(resp_str)
                        sys.stdout.flush()
                    if resp_str and json_load(resp_str).get("ret_code") in (5000, 5100) and retry_time < self.retry_time - 1:
                        # 5000: INTERNAL ERROR
                        # 5100: SERVER BUSY
                        self._get_conn(self.host, self.port)
                        time.sleep(next_sleep)
                        retry_time += 1
                        continue
                    return json_load(resp_str) if resp_str else ""
            except Exception:
                if retry_time < self.retry_time - 1:
                    self._get_conn(self.host, self.port)
                else:
                    raise

            time.sleep(next_sleep)
            retry_time += 1

    def _gen_req_id(self):
        return uuid.uuid4().hex

    def build_http_request(self, verb, url, base_params, auth_path=None,
                           headers=None, host=None, data=""):
        params = {}
        for key, values in base_params.items():
            if values is None:
                continue
            if isinstance(values, list):
                for i in range(1, len(values) + 1):
                    if isinstance(values[i - 1], dict):
                        for sk, sv in values[i - 1].items():
                            if isinstance(sv, dict) or isinstance(sv, list):
                                sv = json_dump(sv)
                            params['%s.%d.%s' % (key, i, sk)] = sv
                    else:
                        params['%s.%d' % (key, i)] = values[i - 1]
            else:
                params[key] = values

        # add req_id
        params.setdefault('req_id', self._gen_req_id())

        return HTTPRequest(verb, self.protocol, headers, self.host, self.port,
                           url, params)

    def describe_access_keys(self,
                             access_keys=None,
                             status=None,
                             limit=None,
                             offset=None,
                             **ignore):
        """ Describe access keys.

        @param jobs: the IDs of access key you want to describe.
        @param status: filter by status: active, inactive, disabled.
        @param offset: the starting offset of the returning results.
        @param limit: specify the number of the returning results.
        """
        action = const.ACTION_DESCRIBE_ACCESS_KEYS
        valid_keys = ['access_keys', 'status', 'offset', 'limit']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             integer_params=["offset", "limit"],
                                             list_params=["access_keys", "status"]):
            return None

        return self.send_request(action, body)

    def create_sub_user(self,
                        email,
                        passwd,
                        user_name=None,
                        phone=None,
                        notify_email=None,
                        nologin=None,
                        change_passwd_first_login=None,
                        **ignore):
        """
        @Param email string enums{} true public "子用户的电子邮件地址"
        @Param notify_email string enums{} true public "子用户的告警电子邮件地址"
        @Param passwd string enums{} true public "子用户的密码"
        @Param user_name string enums{} false public "子用户的用户名称"
        @Param phone string enums{} false public "子用户的电话号码"
        @Param nologin int enums{} false public "子用户是否禁止登录"
        @Param change_passwd_first_login int enums{} false public "子用户第一次登录是否需要修改密码"
        """
        action = const.ACTION_CREATE_SUB_USER
        valid_keys = ["email", "passwd", "user_name", "phone", "notify_email", "nologin", "change_passwd_first_login"]
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             required_params=["email", "passwd"],
                                             integer_params=["nologin", "change_passwd_first_login"],
                                             list_params=[]):
            return None
        return self.send_request(action, body)

    def delete_sub_user(self,
                        users,
                        status=None,
                        **ignore):
        """
        @Param users list enums{} true public "子用户ID列表"
        @Param status string enums{} false public "状态"
        """
        action = const.ACTION_DELETE_SUB_USERS
        valid_keys = ["users", "status"]
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             required_params=["users"],
                                             integer_params=[],
                                             list_params=["users"]):
            return None
        return self.send_request(action, body)

    def restore_sub_user(self,
                         users,
                         **ignore):
        """
        @Param users list enums{} true public "子用户ID列表"
        """
        action = const.RestoreSubUsers
        valid_keys = ["users"]
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             required_params=["users"],
                                             integer_params=[],
                                             list_params=["users"]):
            return None
        return self.send_request(action, body)

    def describe_sub_users(self,
                           users=None,
                           email=None,
                           status=None,
                           search_word=None,
                           owner=None,
                           offset=None,
                           desensitize=0,
                           limit=20,
                           **ignore):
        """
        @Param offset int enums{} false public "起始坐标"
        @Param limit int enums{} false public "偏移量"
        @Param email string enums{} false public "电子邮件地址"
        @Param search_word string enums{} false public "搜索关键字"
        @Param owner string enums{} false public "子用户的所有者"
        @Param users list enums{} false public "子用户的用户ID的集合"
        @Param status string enums{} false public "子用户的状态"
        """
        action = const.ACTION_DESCRIBE_SUB_USERS
        valid_keys = ["users", "offset", "limit", "desensitize", "email", "search_word", "owner", "status"]
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             required_params=[],
                                             integer_params=["offset", "limit", "desensitize"],
                                             list_params=["users"]):
            return None

        return self.send_request(action, body)

    def modify_sub_user_attributes(self,
                                   user,
                                   user_name=None,
                                   email=None,
                                   nologin=None,
                                   passwd=None,
                                   notify_email=None,
                                   change_passwd_first_login=None,
                                   **ignore):
        """
        @Param email string enums{} false public "电子邮件地址"
        @Param search_word string enums{} false public "搜索关键字"
        @Param owner string enums{} false public "子用户的所有者"
        @Param user string enums{} false public "子用户ID"
        @Param status string enums{} false public "子用户的状态"
        @Param nologin int enums{} false public "子用户是否禁止登录"
        @Param change_passwd_first_login int enums{} false public "子用户第一次登录是否需要修改密码"
        """
        action = const.ACTION_MODIFY_SUB_USER_ATTRIBUTES
        valid_keys = ["email", "passwd", "user_name", "user", "notify_email", "nologin", "change_passwd_first_login"]
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             required_params=["user"],
                                             integer_params=["nologin", "change_passwd_first_login"],
                                             list_params=[]):
            return None
        return self.send_request(action, body)

    def describe_notification_center_user_posts(self,
                                                post_type=None,
                                                status=None,
                                                limit=None,
                                                offset=None,
                                                **ignore):
        """ Describe posts in notification center

        @param post_type: specify the type of post, valid values: failures, products
        @param status: filter by status: new, read
        @param offset: the starting offset of the returning results.
        @param limit: specify the number of the returning results.
        """
        action = const.ACTION_DESCRIBE_NOTIFICATION_CENTER_USER_POSTS
        valid_keys = ['post_type', 'status', 'offset', 'limit']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             integer_params=["offset", "limit"],
                                             list_params=["post_type", "status"]):
            return None

        return self.send_request(action, body)

    def describe_zones(self):
        """ Describe zones
        """
        action = const.ACTION_DESCRIBE_ZONES
        body = {}
        if not self.req_checker.check_params(body,
                                             required_params=[],
                                             ):
            return None

        return self.send_request(action, body)

    def describe_jobs(self, jobs=None,
                      status=None,
                      job_action=None,
                      offset=None,
                      limit=None,
                      **ignore):
        """ Describe jobs.
        @param jobs: the IDs of job you want to describe.
        @param status: valid values include pending, working, failed, successful.
        @param job_action: the action of job you want to describe.
        @param offset: the starting offset of the returning results.
        @param limit: specify the number of the returning results.
        """
        action = const.ACTION_DESCRIBE_JOBS
        valid_keys = ['jobs', 'status', 'job_action', 'offset', 'limit']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             required_params=[],
                                             integer_params=[
                                                 "offset", "limit"],
                                             list_params=["jobs"]
                                             ):
            return None

        return self.send_request(action, body)

    def create_server_certificate(self, server_certificate_name=None,
                                  certificate_content=None,
                                  private_key=None,
                                  **ignore):
        """ Create server certificate
        @param server_certificate_name: the name of server certificate
        @param certificate_content: the name of server certificate
        @param private_key: the private key of server certificate
        """
        action = const.ACTION_CREATE_SERVER_CERTIFICATE
        body = {'server_certificate_name': server_certificate_name,
                'certificate_content': certificate_content,
                'private_key': private_key}
        if not self.req_checker.check_params(body,
                                             required_params=[
                                                 'certificate_content', 'private_key'],
                                             integer_params=[],
                                             list_params=[]
                                             ):
            return None

        return self.send_request(action, body, verb='POST')

    def describe_server_certificates(self, server_certificates=None,
                                     search_word=None,
                                     verbose=0,
                                     offset=None,
                                     limit=None,
                                     **ignore):
        """  Describe server certificates.
        @param server_certificates: filter by server certificates ID.
        @param search_word: filter by server certificates name.
        @param verbose: the number to specify the verbose level,
                        larger the number, the more detailed information will be returned.
        @param offset: the starting offset of the returning results.
        @param limit: specify the number of the returning results.
        """

        action = const.ACTION_DESCRIBE_SERVER_CERTIFICATES
        valid_keys = ['server_certificates', 'search_word',
                      'verbose', 'offset', 'limit']
        body = filter_out_none(locals(), valid_keys)

        if not self.req_checker.check_params(body,
                                             required_params=[],
                                             integer_params=['verbose', 'offset', 'limit'],
                                             list_params=['server_certificates']
                                             ):
            return None

        return self.send_request(action, body)

    def modify_server_certificate_attributes(self,
                                             server_certificate=None,
                                             server_certificate_name=None,
                                             description=None,
                                             **ignore):
        """ Modify server certificate attributes
        @param server_certificate: the ID of server certificate.
        @param server_certificate_name: server certificate new name.
        @param description: server certificate new description.
        :return:
        """

        action = const.ACTION_MODIFY_SERVER_CERTIFICATE_ATTRIBUTES
        valid_keys = ['server_certificate', 'server_certificate_name', 'description']
        body = filter_out_none(locals(), valid_keys)

        if not self.req_checker.check_params(body,
                                             required_params=['server_certificate'],
                                             integer_params=[],
                                             list_params=[]
                                             ):
            return None

        return self.send_request(action, body)

    def delete_server_certificates(self, server_certificates,
                                   **ignore):
        """ Delete server certificates.
        @param server_certificates: the array of policy rule IDs.
        """
        action = const.ACTION_DELETE_SERVER_CERTIFICATES
        body = {'server_certificates': server_certificates}
        if not self.req_checker.check_params(body,
                                             required_params=[
                                                 'server_certificates'],
                                             integer_params=[],
                                             list_params=[
                                                 'server_certificates']
                                             ):
            return None

        return self.send_request(action, body)

    def get_monitoring_data(self, resource,
                            meters,
                            step,
                            start_time,
                            end_time,
                            decompress=False,
                            **ignore):
        """ Get resource monitoring data.
        @param resource: the ID of resource, can be instance_id, volume_id, eip_id or router_id.
        @param meters: list of metering types you want to get.
                       If resource is instance, meter can be "cpu", "disk-os", "memory",
                       "disk-%s" % attached_volume_id, "if-%s" % vxnet_mac_address.
                       If resource is volume, meter should be "disk-%s" % volume_id.
                       If resource is eip, meter should be "traffic".
                       If resource is router, meter can be "vxnet-0" and joint vxnet ID.
        @param step: The metering time step, valid steps: "5m", "15m", "30m", "1h", "2h", "1d".
        @param start_time: the starting UTC time, in the format YYYY-MM-DDThh:mm:ssZ.
        @param end_time: the ending UTC time, in the format YYYY-MM-DDThh:mm:ssZ.
        """
        action = const.ACTION_GET_MONITOR
        valid_keys = ['resource', 'meters', 'step', 'start_time', 'end_time']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             required_params=[
                                                 'resource', 'meters', 'step', 'start_time', 'end_time'],
                                             integer_params=[],
                                             datetime_params=[
                                                 'start_time', 'end_time'],
                                             list_params=['meters']
                                             ):
            return None

        resp = self.send_request(action, body)
        if resp and resp.get('meter_set') and decompress:
            p = MonitorProcessor(resp['meter_set'], start_time, end_time, step)
            resp['meter_set'] = p.decompress_monitoring_data()
        return resp

    def get_loadbalancer_monitoring_data(self, resource,
                                         meters,
                                         step,
                                         start_time,
                                         end_time,
                                         decompress=False,
                                         **ignore):
        """ Get load balancer monitoring data.
        @param resource: the ID of resource, can be loadbalancer_id, listener_id or backend_id.
        @param meters: list of metering types you want to get, valid values: request, traffic.
        @param step: The metering time step, valid steps: "5m", "15m", "30m", "1h", "2h", "1d".
        @param start_time: the starting UTC time, in the format YYYY-MM-DDThh:mm:ssZ.
        @param end_time: the ending UTC time, in the format YYYY-MM-DDThh:mm:ssZ.
        """
        action = const.ACTION_GET_LOADBALANCER_MONITOR
        valid_keys = ['resource', 'meters', 'step', 'start_time', 'end_time']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             required_params=[
                                                 'resource', 'meters', 'step', 'start_time', 'end_time'],
                                             integer_params=[],
                                             datetime_params=[
                                                 'start_time', 'end_time'],
                                             list_params=['meters']
                                             ):
            return None

        resp = self.send_request(action, body)
        if resp and resp.get('meter_set') and decompress:
            p = MonitorProcessor(resp['meter_set'], start_time, end_time, step)
            resp['meter_set'] = p.decompress_lb_monitoring_data()
        return resp

    def describe_rdbs(self, rdbs=None,
                      rdb_engine=None,
                      status=None,
                      owner=None,
                      verbose=0,
                      search_word=None,
                      offset=None,
                      limit=None,
                      tags=None,
                      **ignore):
        """ Describe rdbs filtered by condition.
        @param rdbs: an array including IDs of the rdbs you want to list.
                     No ID specified means list all.
        @param rdb_engine: filter by rdb engine: mysql, psql.
        @param status: valid values include pending, available, suspended, deleted, ceased.
        @param verbose: the number to specify the verbose level,
                        larger the number, the more detailed information will be returned.
        @param search_word: the search word.
        @param offset: the starting offset of the returning results.
        @param limit: specify the number of the returning results.
        @param tags : the array of IDs of tags.
        """
        action = const.ACTION_DESCRIBE_RDBS
        valid_keys = ['rdbs', 'rdb_engine', 'status', 'owner',
                      'verbose', 'search_word', 'offset', 'limit', 'tags']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             required_params=[],
                                             integer_params=[
                                                 "offset", "limit", "verbose"],
                                             list_params=["rdbs", "tags"]
                                             ):
            return None

        return self.send_request(action, body)

    def create_rdb(self, vxnet=None,
                   rdb_engine=None,
                   engine_version=None,
                   rdb_username=None,
                   rdb_password=None,
                   rdb_type=None,
                   storage_size=None,
                   rdb_name=None,
                   private_ips=None,
                   description=None,
                   auto_backup_time=None,
                   **ignore):
        """ Create one rdb.
        @param vxnet: vxnet_id.
        @param rdb_engine: set rdb engine: mysql, psql.
        @param engine_version: set rdb version, mysql support 5.5, psql support 9.4.
                               the default is 5.5.
        @param rdb_username: the rdb's username
        @param rdb_password: the rdb's password
        @param rdb_type: defined by qingcloud: 1, 2, 3, 4, 5
        @param storage_size: the size of rdb storage, min 10G, max 1000G
        @param rdb_name: the rdb's name
        @param private_ips: set node's ip, like [{"master":"192.168.100.14","topslave":"192.168.100.17"}]
        @param description: the description of this rdb
        @param auto_backup_time: auto backup time, valid value is [0, 23], any value over 23 means close
                                 autp backup. If skipped, it will choose a value randomly.
        """
        action = const.ACTION_CREATE_RDB
        valid_keys = ['vxnet', 'rdb_engine', 'engine_version', 'rdb_username',
                      'rdb_password', 'rdb_type', 'storage_size', 'rdb_name',
                      'private_ips', 'description', 'auto_backup_time']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             required_params=['vxnet', 'engine_version', 'rdb_username', 'rdb_password',
                                                              'rdb_type', 'storage_size'],
                                             integer_params=['rdb_type',
                                                             'storage_size', 'auto_backup_time'],
                                             list_params=[]
                                             ):
            return None

        return self.send_request(action, body)

    def resize_rdbs(self, rdbs,
                    rdb_type=None,
                    storage_size=None,
                    **ignore):
        """ Resize one or more rdbs.
        @param rdbs: the IDs of the rdbs you want to resize.
        @param rdb_type: defined by qingcloud: 1, 2, 3, 4, 5
        @param cpu: cpu core number.
        @param memory: memory size in MB.
        """
        action = const.ACTION_RESIZE_RDBS
        valid_keys = ['rdbs', 'rdb_type', 'storage_size']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             required_params=['rdbs'],
                                             integer_params=[
                                                 'rdb_type', 'storage_size'],
                                             list_params=['rdbs']
                                             ):
            return None

        return self.send_request(action, body)

    def start_rdbs(self, rdbs,
                   **ignore):
        """ Start one or more rdbs.
        @param rdbs: the IDs of the rdbs you want to start.
        """
        action = const.ACTION_START_RDBS
        valid_keys = ['rdbs']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             required_params=['rdbs'],
                                             list_params=['rdbs']
                                             ):
            return None

        return self.send_request(action, body)

    def stop_rdbs(self, rdbs,
                  **ignore):
        """ Stop one or more rdbs.
        @param rdbs: the IDs of the rdbs you want to stop.
        """
        action = const.ACTION_STOP_RDBS
        valid_keys = ['rdbs']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             required_params=['rdbs'],
                                             list_params=['rdbs']
                                             ):
            return None

        return self.send_request(action, body)

    def describe_mongos(self, mongos=None,
                        status=None,
                        verbose=0,
                        owner=None,
                        search_word=None,
                        offset=None,
                        limit=None,
                        tags=None,
                        **ignore):
        """ Describe mongos filtered by condition.
        @param mongos: an array including IDs of the mongos you want to list.
                     No ID specified means list all.
        @param status: valid values include pending, available, suspended, deleted, ceased.
        @param verbose: the number to specify the verbose level,
                        larger the number, the more detailed information will be returned.
        @param search_word: the search word.
        @param offset: the starting offset of the returning results.
        @param limit: specify the number of the returning results.
        @param tags : the array of IDs of tags.
        """
        action = const.ACTION_DESCRIBE_MONGOS
        valid_keys = ['mongos', 'status', 'verbose', 'search_word',
                      'offset', 'limit', 'tags', 'owner']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             required_params=[],
                                             integer_params=[
                                                 "offset", "limit", "verbose"],
                                             list_params=["mongos", "tags"]
                                             ):
            return None

        return self.send_request(action, body)

    def resize_mongos(self, mongos,
                      mongo_type=None,
                      storage_size=None,
                      **ignore):
        """ Resize one or more mongos.
        @param mongos: the IDs of the mongos you want to resize.
        @param mongo_type: defined by qingcloud: 1, 2, 3, 4.
                           see: https://docs.qingcloud.com/api/mongo/resize_mongos.html
        @param cpu: cpu core number.
        @param memory: memory size in MB.
        """
        action = const.ACTION_RESIZE_MONGOS
        valid_keys = ['mongos', 'mongo_type', 'storage_size']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             required_params=['mongos'],
                                             integer_params=[
                                                 'mongo_type', 'storage_size'],
                                             list_params=['mongos']
                                             ):
            return None

        return self.send_request(action, body)

    def start_mongos(self, mongos,
                     **ignore):
        """ Start one or more mongos.
        @param mongos: the IDs of the mongos you want to start.
        """
        action = const.ACTION_START_MONGOS
        valid_keys = ['mongos']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             required_params=['mongos'],
                                             list_params=['mongos']
                                             ):
            return None

        return self.send_request(action, body)

    def stop_mongos(self, mongos,
                    **ignore):
        """ Stop one or more mongos.
        @param mongos: the IDs of the mongos you want to stop.
        """
        action = const.ACTION_STOP_MONGOS
        valid_keys = ['mongos']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             required_params=['mongos'],
                                             list_params=['mongos']
                                             ):
            return None

        return self.send_request(action, body)

    def describe_caches(self, caches=None,
                        status=None,
                        verbose=0,
                        owner=None,
                        search_word=None,
                        offset=None,
                        limit=None,
                        tags=None,
                        **ignore):
        """ Describe caches filtered by condition.
        @param caches: an array including IDs of the caches you want to list.
                     No ID specified means list all.
        @param status: valid values include pending, available, suspended, deleted, ceased.
        @param verbose: the number to specify the verbose level,
                        larger the number, the more detailed information will be returned.
        @param search_word: the search word.
        @param offset: the starting offset of the returning results.
        @param limit: specify the number of the returning results.
        @param tags : the array of IDs of tags.
        """
        action = const.ACTION_DESCRIBE_CACHES
        valid_keys = ['caches', 'status', 'verbose', 'search_word',
                      'offset', 'limit', 'tags', 'owner']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             required_params=[],
                                             integer_params=[
                                                 "offset", "limit", "verbose"],
                                             list_params=["caches", "tags"]
                                             ):
            return None

        return self.send_request(action, body)

    def create_cache(self, vxnet=None,
                     cache_size=None,
                     cache_type=None,
                     node_count=None,
                     cache_name=None,
                     cache_parameter_group=None,
                     private_ips=None,
                     auto_backup_time=None,
                     cache_class=None,
                     **ignore):
        """ Create a cache.
        @param vxnet: the vxnet id that cache added.
        @param cache_size: cache size, unit is GB
        @param cache_type: cache service type, now support redis2.8.17 and memcached1.4.13.
        @param node_count: cache service node number, default set 1.
        @param cache_name: cache service's name
        @param cache_parameter_group: cache service configuration group ID, if not given,
                                      set to default one.
        @param private_ips: the array of private_ips setting, include cache_role and specify private_ips
        @param auto_backup_time: auto backup time, valid value is [0, 23], any value over 23 means close
                                 autp backup. If skipped, it will choose a value randomly.
        @param cache_class: property type set 0 and high property type set 1
        """
        action = const.ACTION_CREATE_CACHE
        valid_keys = ['vxnet', 'cache_size', 'cache_type', 'node_count',
                      'cache_name', 'cache_parameter_group', 'private_ips',
                      'auto_backup_time', 'cache_class']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             required_params=[
                                                 'vxnet', 'cache_size', 'cache_type'],
                                             integer_params=['cache_size', 'node_count',
                                                             'auto_backup_time', 'cache_class'],
                                             list_params=['private_ips']
                                             ):
            return None

        return self.send_request(action, body)

    def resize_caches(self, caches,
                      cache_size=None,
                      storage_size=None,
                      **ignore):
        """ Resize one or more caches.
        @param caches: the IDs of the caches you want to resize.
        @param cache_size: defined by qingcloud: 1 - 32 GB.
        @param cpu: cpu core number.
        @param memory: memory size in MB.
        """
        action = const.ACTION_RESIZE_CACHES
        valid_keys = ['caches', 'cache_size', 'storage_size']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             required_params=['caches'],
                                             integer_params=[
                                                 'cache_size', 'storage_size'],
                                             list_params=['caches']
                                             ):
            return None

        return self.send_request(action, body)

    def start_caches(self, caches,
                     **ignore):
        """ Start one or more caches.
        @param caches: the IDs of the caches you want to start.
        """
        action = const.ACTION_START_CACHES
        valid_keys = ['caches']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             required_params=['caches'],
                                             list_params=['caches']
                                             ):
            return None

        return self.send_request(action, body)

    def stop_caches(self, caches,
                    **ignore):
        """ Stop one or more caches.
        @param caches: the IDs of the caches you want to stop.
        """
        action = const.ACTION_STOP_CACHES
        valid_keys = ['caches']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             required_params=['caches'],
                                             list_params=['caches']
                                             ):
            return None

        return self.send_request(action, body)

    def create_spark(self, vxnet=None,
                     spark_version=None,
                     enable_hdfs=None,
                     storage_size=None,
                     spark_type=None,
                     node_count=None,
                     spark_name=None,
                     private_ips=None,
                     spark_class=None,
                     description=None,
                     zk_id=None,
                     parameter_group=None,
                     **ignore):
        """ Create a spark cluster.
        @param vxnet: the vxnet id that spark want to join.
        @param spark_version: the version of spark, suck as 1.4.1, 1.5.0, 1.6.0
        @param enabled_hdfs: whether to use hdfs as storage or not
        @param storage_size: storage size, unit is GB
        @param spark_type: cpu-memory size of spark cluster, such as 1:1c2g, 2:2c4g, 3:2c8g, 4:4c8g, 5:8c16g
        @param node_count: spark cluster node number, at least 2 for hdfs enabled.
        @param spark_name: spark cluster's name
        @param private_ips: the array of private_ips setting, include spark_role and specified private_ips
        @param spark_class: high performance is set 0 and super-high 1
        @param zk_id: the zookeeper id which ha-enabled spark will use
        @param parameter_group: the parameter configuration group which will be applied to spark cluster
        """
        action = const.ACTION_CREATE_SPARK
        valid_keys = ['vxnet', 'storage_size', 'spark_type', 'node_count',
                      'spark_name', 'spark_version', 'private_ips',
                      'enable_hdfs', 'spark_class', "description",
                      "zk_id", "parameter_group"]
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             required_params=["vxnet", "spark_type",
                                                              "spark_version", "node_count",
                                                              "storage_size", "enable_hdfs"],
                                             integer_params=["node_count", "spark_type",
                                                             "storage_size", "enable_hdfs", "spark_class"],
                                             list_params=['private_ips']
                                             ):
            return None

        return self.send_request(action, body)

    def describe_sparks(self, sparks=None,
                        status=None,
                        verbose=0,
                        owner=None,
                        search_word=None,
                        offset=None,
                        limit=None,
                        tags=None,
                        **ignore):
        """ Describe sparks filtered by condition.
        @param sparks: the array of spark IDs.
        @param status: pending, active, stopped, deleted, suspended, ceased
        @param verbose: the number to specify the verbose level, larger the number, the more detailed information will be returned.
        @param search_word: search word column.
        @param offset: the starting offset of the returning results.
        @param limit: specify the number of the returning results.
        @param tags : the array of IDs of tags.
        """
        action = const.ACTION_DESCRIBE_SPARKS
        valid_keys = ['sparks', 'status', 'verbose', 'search_word',
                      'offset', 'limit', 'tags', 'owner']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             required_params=[],
                                             integer_params=[
                                                 'offset', 'limit'],
                                             list_params=[
                                                 'sparks', 'status', 'tags']
                                             ):
            return None

        return self.send_request(action, body)

    def start_sparks(self, sparks,
                     **ignore):
        """ Start one or more sparks.
        @param sparks: the IDs of the spark you want to start.
        """
        action = const.ACTION_START_SPARKS
        valid_keys = ['sparks']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             required_params=['sparks'],
                                             list_params=['sparks']
                                             ):
            return None

        return self.send_request(action, body)

    def stop_sparks(self, sparks,
                    **ignore):
        """ Stop one or more sparks.
        @param sparks: the IDs of the spark you want to stop.
        """
        action = const.ACTION_STOP_SPARKS
        valid_keys = ['sparks']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             required_params=['sparks'],
                                             list_params=['sparks']
                                             ):
            return None

        return self.send_request(action, body)

    def delete_sparks(self, sparks, **ignore):
        '''Delete one or more sparks
        @param sparks: the IDs of the spark you want to stop.
        '''
        action = const.ACTION_DELETE_SPARKS
        valid_keys = ['sparks']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             required_params=['sparks'],
                                             list_params=['sparks']
                                             ):
            return None

        return self.send_request(action, body)

    def add_spark_nodes(self, spark, node_count, node_name=None, private_ips=None, **params):
        """ Add one or more spark nodes
        """
        action = const.ACTION_ADD_SPARK_NODES
        valid_keys = ['spark', 'node_count', 'node_name', 'private_ips']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             required_params=[
                                                 'spark', 'node_count'],
                                             integer_params=['node_count'],
                                             list_params=['private_ips']
                                             ):
            return None

        return self.send_request(action, body)

    def delete_spark_nodes(self, spark, spark_nodes):
        """ Delete one or more spark nodes
        """
        action = const.ACTION_DELETE_SPARK_NODES
        valid_keys = ['spark', 'spark_nodes']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             required_params=[
                                                 'spark', 'spark_nodes'],
                                             list_params=['spark_nodes']):
            return None

        return self.send_request(action, body)

    def describe_hadoops(self, hadoops=None,
                         status=None,
                         verbose=0,
                         owner=None,
                         search_word=None,
                         offset=None,
                         limit=None,
                         tags=None,
                         **ignore):
        """ Describe hadoops filtered by condition.
        @param hadoops: the array of hadoop IDs.
        @param status: pending, active, stopped, deleted, suspended, ceased
        @param verbose: the number to specify the verbose level, larger the number, the more detailed information will be returned.
        @param search_word: search word column.
        @param offset: the starting offset of the returning results.
        @param limit: specify the number of the returning results.
        @param tags : the array of IDs of tags.
        """
        action = const.ACTION_DESCRIBE_HADOOPS
        valid_keys = ['hadoops', 'status', 'verbose', 'search_word',
                      'offset', 'limit', 'tags', 'owner']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             required_params=[],
                                             integer_params=[
                                                 'offset', 'limit'],
                                             list_params=[
                                                 'hadoops', 'status', 'tags']
                                             ):
            return None

        return self.send_request(action, body)

    def start_hadoops(self, hadoops,
                      **ignore):
        """ Start one or more hadoops.
        @param hadoops: the IDs of the hadoop you want to start.
        """
        action = const.ACTION_START_HADOOPS
        valid_keys = ['hadoops']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             required_params=['hadoops'],
                                             list_params=['hadoops']
                                             ):
            return None

        return self.send_request(action, body)

    def stop_hadoops(self, hadoops,
                     **ignore):
        """ Stop one or more hadoops.
        @param hadoops: the IDs of the hadoop you want to stop.
        """
        action = const.ACTION_STOP_HADOOPS
        valid_keys = ['hadoops']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             required_params=['hadoops'],
                                             list_params=['hadoops']
                                             ):
            return None

        return self.send_request(action, body)

    def describe_dns_aliases(self, dns_aliases=None,
                             resource_id=None,
                             offset=None,
                             limit=None,
                             **ignore):
        """ Describe dns aliases filtered by condition.
        @param dns_aliases: the array of dns alias IDs.
        @param resource_id: search word column.
        @param offset: the starting offset of the returning results.
        @param limit: specify the number of the returning results.
        """
        action = const.ACTION_DESCRIBE_DNS_ALIASES
        valid_keys = ['dns_aliases', 'resource_id', 'offset', 'limit']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             required_params=[],
                                             integer_params=[
                                                 'offset', 'limit'],
                                             list_params=['dns_aliases']
                                             ):
            return None

        return self.send_request(action, body)

    def associate_dns_alias(self, prefix,
                            resource,
                            **ignore):
        """ Associate DNS alias.
        @param prefix: the DNS prefix.
        @param resource: The id of resource you want to associate DNS alias with.
        """
        action = const.ACTION_ASSOCIATE_DNS_ALIAS
        valid_keys = ['prefix', 'resource']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             required_params=[
                                                 'prefix', 'resource'],
                                             list_params=[]
                                             ):
            return None

        return self.send_request(action, body)

    def dissociate_dns_aliases(self, dns_aliases,
                               **ignore):
        """ Dissociate DNS aliases.
        @param dns_aliases: The array of dns alias IDs you want to dissociate.
        """
        action = const.ACTION_DISSOCIATE_DNS_ALIASES
        valid_keys = ['dns_aliases']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             required_params=['dns_aliases'],
                                             list_params=['dns_aliases']
                                             ):
            return None

        return self.send_request(action, body)

    def get_dns_label(self, **ignore):
        """ Get DNS label and domain name in this zone.
        """
        action = const.ACTION_GET_DNS_LABEL
        valid_keys = []
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             required_params=[],
                                             ):
            return None

        return self.send_request(action, body)

    def describe_zookeepers(self, zookeepers=None,
                            status=None,
                            verbose=0,
                            search_word=None,
                            owner=None,
                            offset=None,
                            limit=None,
                            tags=None,
                            **ignore):
        """ Describe zookeepers filtered by condition.
        @param zookeepers: the array of zookeeper IDs.
        @param status: pending, active, stopped, deleted, suspended, ceased
        @param verbose: the number to specify the verbose level, larger the number, the more detailed information will be returned.
        @param search_word: search word column.
        @param offset: the starting offset of the returning results.
        @param limit: specify the number of the returning results.
        @param tags : the array of IDs of tags.
        """
        action = const.ACTION_DESCRIBE_ZOOKEEPERS
        valid_keys = ['zookeepers', 'status', 'verbose', 'search_word',
                      'offset', 'limit', 'tags', 'owner']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             required_params=[],
                                             integer_params=[
                                                 'offset', 'limit'],
                                             list_params=['zookeepers', 'tags']
                                             ):
            return None

        return self.send_request(action, body)

    def start_zookeepers(self, zookeepers,
                         **ignore):
        """ Start one or more zookeepers.
        @param zookeepers: the IDs of the zookeeper you want to start.
        """
        action = const.ACTION_START_ZOOKEEPERS
        valid_keys = ['zookeepers']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             required_params=['zookeepers'],
                                             list_params=['zookeepers']
                                             ):
            return None

        return self.send_request(action, body)

    def stop_zookeepers(self, zookeepers,
                        **ignore):
        """ Stop one or more zookeepers.
        @param zookeepers: the IDs of the zookeeper you want to stop.
        """
        action = const.ACTION_STOP_ZOOKEEPERS
        valid_keys = ['zookeepers']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             required_params=['zookeepers'],
                                             list_params=['zookeepers']
                                             ):
            return None

        return self.send_request(action, body)

    def describe_elasticsearchs(self, elasticsearchs=None,
                                status=None,
                                verbose=0,
                                search_word=None,
                                owner=None,
                                offset=None,
                                limit=None,
                                tags=None,
                                **ignore):
        """ Describe elasticsearchs filtered by condition.
        @param elasticsearchs: the array of elasticsearchs IDs.
        @param status: pending, active, stopped, deleted, suspended, ceased
        @param verbose: the number to specify the verbose level, larger the number, the more detailed information will be returned.
        @param search_word: search word column.
        @param offset: the starting offset of the returning results.
        @param limit: specify the number of the returning results.
        @param tags : the array of IDs of tags.
        """
        action = const.ACTION_DESCRIBE_ELASTICSEARCHS
        valid_keys = ['elasticsearchs', 'status', 'verbose', 'search_word',
                      'offset', 'limit', 'tags', 'owner']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             required_params=[],
                                             integer_params=[
                                                 'offset', 'limit'],
                                             list_params=['elasticsearchs', 'tags']
                                             ):
            return None

        return self.send_request(action, body)

    def start_elasticsearchs(self, elasticsearchs,
                             **ignore):
        """ Start one or more elasticsearchs.
        @param elasticsearchs: the IDs of the elasticsearch you want to start.
        """
        action = const.ACTION_START_ELASTICSEARCHS
        valid_keys = ['elasticsearchs']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             required_params=['elasticsearchs'],
                                             list_params=['elasticsearchs']
                                             ):
            return None

        return self.send_request(action, body)

    def stop_elasticsearchs(self, elasticsearchs,
                            **ignore):
        """ Stop one or more elasticsearchs.
        @param elasticsearchs: the IDs of the elasticsearch you want to stop.
        """
        action = const.ACTION_STOP_ELASTICSEARCHS
        valid_keys = ['elasticsearchs']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             required_params=['elasticsearchs'],
                                             list_params=['elasticsearchs']
                                             ):
            return None

        return self.send_request(action, body)

    def describe_queues(self, queues=None,
                        status=None,
                        verbose=0,
                        owner=None,
                        search_word=None,
                        offset=None,
                        limit=None,
                        tags=None,
                        **ignore):
        """ Describe queues filtered by condition.
        @param queues: the array of queue IDs.
        @param status: pending, active, stopped, deleted, suspended, ceased
        @param verbose: the number to specify the verbose level, larger the number, the more detailed information will be returned.
        @param search_word: search word column.
        @param offset: the starting offset of the returning results.
        @param limit: specify the number of the returning results.
        @param tags : the array of IDs of tags.
        """
        action = const.ACTION_DESCRIBE_QUEUES
        valid_keys = ['queues', 'status', 'verbose', 'search_word',
                      'offset', 'limit', 'tags', 'owner']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             required_params=[],
                                             integer_params=[
                                                 'offset', 'limit'],
                                             list_params=[
                                                 'queues', 'status', 'tags']
                                             ):
            return None

        return self.send_request(action, body)

    def start_queues(self, queues,
                     **ignore):
        """ Start one or more queues.
        @param queues: the IDs of the queue you want to start.
        """
        action = const.ACTION_START_QUEUES
        valid_keys = ['queues']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             required_params=['queues'],
                                             list_params=['queues']
                                             ):
            return None

        return self.send_request(action, body)

    def stop_queues(self, queues,
                    **ignore):
        """ Stop one or more queues.
        @param queues: the IDs of the queue you want to stop.
        """
        action = const.ACTION_STOP_QUEUES
        valid_keys = ['queues']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             required_params=['queues'],
                                             list_params=['queues']
                                             ):
            return None

        return self.send_request(action, body)

    def __getattr__(self, attr):
        """ Get api functions from each Action class
        """
        for action in self.actions:
            if hasattr(action, attr):
                return getattr(action, attr)

        raise InvalidAction(attr)

    def get_balance(self, **ignore):
        """Get the balance information filtered by conditions.
        """
        action = const.ACTION_GET_BALANCE
        valid_keys = []
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body):
            return None

        return self.send_request(action, body)

    def get_lease_info(self,
                       resource,
                       user=None,
                       **ignore):
        """ Get the lease info filtered by conditions.
        @param resource: the ID of resource.
        @param user : the ID of user.
        """
        action = const.ACTION_GET_LEASE_INFO
        valid_keys = ['resource', 'user']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             required_params=['resource']):
            return None

        return self.send_request(action, body)

    def describe_shared_resource_groups(self,
                                        resource_groups=None,
                                        owner=None,
                                        **ignore):
        """ Describe resource groups which be shared with oneself.
        @param resource_groups: An array including IDs of resource groups.
        @param owner: The people who shares resource groups with oneself.
        """
        action = const.ACTION_DESCRIBE_SHARED_RESOURCE_GROUPS
        valid_keys = ['resource_groups', 'owner']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             list_params=['resource_groups']
                                             ):
            return None

        return self.send_request(action, body)

    def describe_resource_groups(self,
                                 resource_groups=None,
                                 search_word=None,
                                 limit=None,
                                 offset=None,
                                 verbose=None,
                                 sort_key=None,
                                 reverse=None,
                                 **ignore):
        """ Describe the messages of resource groups filtered by condition.
        @param resource_groups: an array including IDs of resource groups.
        @param search_word: the search word which can be instance id and instance name.
        @param limit: specify the number of the returning results.
        @param offset: the starting offset of the returning results.
        @param verbose: Whether to return redundant message.
                        if it is 1, return the details of the instance related other resources.
        @param sort_key: the sort key, which defaults be create_time.
        @param reverse: 0 for Ascending order, 1 for Descending order.
        """
        action = const.ACTION_DESCRIBE_RESOURCE_GROUPS
        valid_keys = [
            'resource_groups', 'search_word', 'limit',
            'offset', 'verbose', 'sort_key', 'reverse'
        ]
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             integer_params=[
                                                 'offset', 'limit',
                                                 'verbose', 'reverse'
                                             ],
                                             list_params=['resource_groups']
                                             ):
            return None

        return self.send_request(action, body)

    def create_resource_groups(self,
                               resource_group_name=None,
                               description=None,
                               count=None,
                               **ignore):
        """ Create resource groups.
        @param resource_group_name: the name of resource groups.
        @param description: the description of resource groups.
        @param count: the number of resource groups created at one time.
        """
        action = const.ACTION_CREATE_RESOURCE_GROUPS
        valid_keys = ['resource_group_name', 'description', 'count']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             integer_params=['count']
                                             ):
            return None

        return self.send_request(action, body)

    def modify_resource_group_attributes(self,
                                         resource_group,
                                         resource_group_name=None,
                                         description=None,
                                         **ignore):
        """ Modify resource group attributes.
        @param resource_group: The ID of resource group which attributes you want to modify.
        @param resource_group_name: The new name of the resource group which will be modified.
        @param description: The description of the resource group.
        """
        action = const.ACTION_MODIFY_RESOURCE_GROUP_ATTRIBUTES
        valid_keys = ['resource_group', 'resource_group_name', 'description']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             required_params=['resource_group']
                                             ):
            return None

        return self.send_request(action, body)

    def delete_resource_groups(self,
                               resource_groups,
                               **ignore):
        """ Delete resource groups.
        @param resource_groups: An array including IDs of the resource groups which you want to delete.
        """
        action = const.ACTION_DELETE_RESOURCE_GROUPS
        valid_keys = ['resource_groups']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             required_params=['resource_groups'],
                                             list_params=['resource_groups']
                                             ):
            return None

        return self.send_request(action, body)

    def describe_resource_group_items(self,
                                      resource_groups=None,
                                      resources=None,
                                      limit=None,
                                      offset=None,
                                      verbose=None,
                                      sort_key=None,
                                      reverse=None,
                                      **ignore):
        """ Describe the items of resource groups filtered by condition.
        @param resource_groups: an array including IDs of resource groups.
        @param resources: an array including IDs of resources, used to query all resource groups for the resource.
        @param limit: specify the number of the returning results.
        @param offset: the starting offset of the returning results.
        @param verbose: Whether to return redundant message.
                        if it is 1, return the details of the instance related other resources.
        @param sort_key: the sort key, which defaults be create_time.
        @param reverse: 0 for ascending order, 1 for descending order.
        """
        action = const.ACTION_DESCRIBE_RESOURCE_GROUP_ITEMS
        valid_keys = [
            'resource_groups', 'search_word', 'limit',
            'offset', 'verbose', 'sort_key', 'reverse'
        ]
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             integer_params=[
                                                 'offset', 'limit',
                                                 'verbose', 'reverse'
                                             ],
                                             list_params=['resource_groups', 'resources']
                                             ):
            return None

        return self.send_request(action, body)

    def add_resource_group_items(self,
                                 resource_group,
                                 resources,
                                 **ignore):
        """ Add resources to the specified resource group.
        @param resource_group: the ID of the resource group.
        @param resources: a list of resources which you want to add.
        """
        action = const.ACTION_ADD_RESOURCE_GROUP_ITEMS
        valid_keys = ['resource_group', 'resources']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             required_params=['resource_group', 'resources'],
                                             list_params=['resources']
                                             ):
            return None

        return self.send_request(action, body)

    def delete_resource_group_items(self,
                                    resource_group,
                                    resources,
                                    **ignore):
        """ Delete resources from the specified resource group.
        @param resource_group: the ID of the resource group.
        @param resources: An array including IDs of resources which you want to delete.
        """
        action = const.ACTION_DELETE_RESOURCE_GROUP_ITEMS
        valid_keys = ['resource_group', 'resources']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             required_params=['resource_group', 'resources'],
                                             list_params=['resources']
                                             ):
            return None

        return self.send_request(action, body)

    def describe_user_groups(self,
                             user_groups=None,
                             status=None,
                             search_word=None,
                             limit=None,
                             offset=None,
                             verbose=None,
                             sort_key=None,
                             reverse=None,
                             **ignore):
        """ Describe the messages of user groups filtered by condition.
        @param user_groups: an array including IDs of user groups.
        @param status: an array including filtering status.
        @param search_word: the search word which can be instance id and instance name.
        @param limit: specify the number of the returning results.
        @param offset: the starting offset of the returning results.
        @param verbose: Whether to return redundant message.
                        if it is 1, return the details of the instance related other resources.
        @param sort_key: the sort key, which defaults be create_time.
        @param reverse: 0 for Ascending order, 1 for Descending order.
        """
        action = const.ACTION_DESCRIBE_USER_GROUPS
        valid_keys = [
            'user_groups', 'status',
            'search_word', 'limit',
            'offset', 'verbose',
            'sort_key', 'reverse'
        ]
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             integer_params=[
                                                 'offset', 'limit',
                                                 'verbose', 'reverse'
                                             ],
                                             list_params=['user_groups', 'status']
                                             ):
            return None

        return self.send_request(action, body)

    def create_user_groups(self,
                           user_group_name=None,
                           description=None,
                           count=None,
                           **ignore):
        """ Create user groups.
        @param user_group_name: the name of user groups.
        @param description: the description of user groups.
        @param count: the number of user groups created at one time, defaults 1.
        """
        action = const.ACTION_CREATE_USER_GROUPS
        valid_keys = ['user_group_name', 'description', 'count']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             integer_params=['count']
                                             ):
            return None

        return self.send_request(action, body)

    def modify_user_group_attributes(self,
                                     user_group,
                                     user_group_name=None,
                                     description=None,
                                     status=None,
                                     **ignore):
        """ Modify user group attributes.
        @param user_group: The ID of user group which attributes you want to modify.
        @param user_group_name: The new name of the user group which will be modified.
        @param description: The description of the resource group.
        @param status: the status of user group.
        """
        action = const.ACTION_MODIFY_USER_GROUP_ATTRIBUTES
        valid_keys = ['user_group', 'user_group_name', 'description', 'status']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             required_params=['user_group']
                                             ):
            return None

        return self.send_request(action, body)

    def delete_user_groups(self,
                           user_groups,
                           **ignore):
        """ Delete the specified user groups.
        @param user_groups: An array including the IDs of the user groups.
        """
        action = const.ACTION_DELETE_USER_GROUPS
        valid_keys = ['user_groups']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             required_params=['user_groups'],
                                             list_params=['user_groups']
                                             ):
            return None

        return self.send_request(action, body)

    def describe_user_group_members(self,
                                    user_groups=None,
                                    users=None,
                                    status=None,
                                    search_word=None,
                                    limit=None,
                                    offset=None,
                                    verbose=None,
                                    sort_key=None,
                                    reverse=None,
                                    **ignore):
        """ Describe the messages of user group members filtered by condition.
        @param user_groups: an array including IDs of user groups.
        @param users: an array including IDs of users.
        @param status: an array including filtering status.
        @param search_word: the search word which can be instance id and instance name.
        @param limit: specify the number of the returning results.
        @param offset: the starting offset of the returning results.
        @param verbose: Whether to return redundant message.
                        if it is 1, return the details of the instance related other resources.
        @param sort_key: the sort key, which defaults be create_time.
        @param reverse: 0 for Ascending order, 1 for Descending order.
        """
        action = const.ACTION_DESCRIBE_USER_GROUP_MEMBERS
        valid_keys = [
            'user_groups', 'users', 'status',
            'search_word', 'limit', 'offset',
            'verbose', 'sort_key', 'reverse'
        ]
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             integer_params=[
                                                 'offset', 'limit',
                                                 'verbose', 'reverse'
                                             ],
                                             list_params=['user_groups', 'users', 'status']
                                             ):
            return None

        return self.send_request(action, body)

    def add_user_group_members(self,
                               user_group,
                               users,
                               **ignore):
        """ Add users to the specified user group.
        @param user_group: the ID of the user group.
        @param users: an array including IDs or emails of users which you want to add.
        """
        action = const.ACTION_ADD_USER_GROUP_MEMBERS
        valid_keys = ['user_group', 'users']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             required_params=['user_group', 'users'],
                                             list_params=['users']
                                             ):
            return None

        return self.send_request(action, body)

    def modify_user_group_member_attributes(self,
                                            user_group,
                                            user,
                                            remarks=None,
                                            status=None,
                                            **ignore):
        """ Modify user group member attributes.
        @param user_group: The ID of user group which attributes you want to modify.
        @param user: The ID of user which attributes you want to modify.
        @param remarks: The remarks information.
        @param status: The status of user group.
        """
        action = const.ACTION_MODIFY_USER_GROUP_MEMBER_ATTRIBUTES
        valid_keys = ['user_group', 'user', 'remarks', 'status']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             required_params=['user_group', 'user']
                                             ):
            return None

        return self.send_request(action, body)

    def delete_user_group_members(self,
                                  user_group,
                                  users,
                                  **ignore):
        """ Delete the specified user group members.
        @param user_group: the ID of the specified user group.
        @param users: an array including IDs of users which you want delete.
        """
        action = const.ACTION_DELETE_USER_GROUP_MEMBERS
        valid_keys = ['user_group', 'users']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             required_params=['user_group', 'users'],
                                             list_params=['users']
                                             ):
            return None

        return self.send_request(action, body)

    def describe_group_roles(self,
                             group_roles=None,
                             status=None,
                             search_word=None,
                             limit=None,
                             offset=None,
                             verbose=None,
                             sort_key=None,
                             reverse=None,
                             **ignore):
        """ Describe the group roles filtered by condition.
        @param group_roles: an array including IDs of user group roles.
        @param status: an array including role status.
        @param search_word: the search word which can be instance id and instance name.
        @param limit: specify the number of the returning results.
        @param offset: the starting offset of the returning results.
        @param verbose: Whether to return redundant message.
                        if it is 1, return the details of the instance related other resources.
        @param sort_key: the sort key, which defaults be create_time.
        @param reverse: 0 for Ascending order, 1 for Descending order.
        """
        action = const.ACTION_DESCRIBE_GROUP_ROLES
        valid_keys = [
            'group_roles', 'status',
            'search_word', 'limit',
            'offset', 'verbose',
            'sort_key', 'reverse'
        ]
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             integer_params=[
                                                 'offset', 'limit',
                                                 'verbose', 'reverse'
                                             ],
                                             list_params=['group_roles', 'status']
                                             ):
            return None

        return self.send_request(action, body)

    def create_group_roles(self,
                           role_type,
                           group_role_name=None,
                           description=None,
                           count=None,
                           **ignore):
            """ Create group roles.
            @param role_type: the type of role, Currently only support 'rule'.
            @param group_role_name: the name of group role.
            @param description: the description of group role.
            @param count: the number of user roles created at one time.
            """
            action = const.ACTION_CREATE_GROUP_ROLES
            valid_keys = ['role_type', 'group_role_name', 'description', 'count']
            body = filter_out_none(locals(), valid_keys)
            if not self.req_checker.check_params(body,
                                                 required_params=['role_type'],
                                                 integer_params=['count']
                                                 ):
                return None

            return self.send_request(action, body)

    def modify_group_role_attributes(self,
                                     group_role,
                                     role_type=None,
                                     group_role_name=None,
                                     description=None,
                                     status=None,
                                     **ignore):
        """ Modify group role attributes.
        @param group_role: The ID of group role which attributes you want to modify.
        @param role_type: The type of role, Currently only support 'rule'.
        @param group_role_name: The name of group role.
        @param description: the description of group role.
        @param status: The status of group role which could be 'disabled' or 'enabled'.
        """
        action = const.ACTION_MODIFY_GROUP_ROLE_ATTRIBUTES
        valid_keys = [
            'group_role', 'role_type', 'group_role_name', 'description', 'status'
        ]
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             required_params=['group_role']
                                             ):
            return None

        return self.send_request(action, body)

    def delete_group_roles(self,
                           group_roles,
                           **ignore):
        """ Delete the specified user group members.
        @param group_roles: an array including the IDs of group roles.
        """
        action = const.ACTION_DELETE_GROUP_ROLES
        valid_keys = ['group_roles']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             required_params=['group_roles'],
                                             list_params=['group_roles']
                                             ):
            return None

        return self.send_request(action, body)

    def describe_group_role_rules(self,
                                  group_role_rules=None,
                                  group_roles=None,
                                  status=None,
                                  limit=None,
                                  offset=None,
                                  verbose=None,
                                  sort_key=None,
                                  reverse=None,
                                  **ignore):
        """ Describe the group role rules filtered by condition.
        @param group_role_rules: an array including IDs of group role rules.
        @param group_roles: an array including IDs of group roles.
        @param status: an array including status which could be 'disabled' or 'enabled'.
        @param limit: specify the number of the returning results.
        @param offset: the starting offset of the returning results.
        @param verbose: Whether to return redundant message.
                        if it is 1, return the details of the instance related other resources.
        @param sort_key: the sort key, which defaults be create_time.
        @param reverse: 0 for Ascending order, 1 for Descending order.
        """
        action = const.ACTION_DESCRIBE_GROUP_ROLE_RULES
        valid_keys = [
            'group_role_rules', 'group_roles',
            'status', 'limit', 'offset',
            'verbose', 'sort_key', 'reverse'
        ]
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             integer_params=[
                                                 'offset', 'limit',
                                                 'verbose', 'reverse'
                                             ],
                                             list_params=[
                                                 'group_role_rules', 'group_roles', 'status'
                                             ]
                                             ):
            return None

        return self.send_request(action, body)

    def add_group_role_rules(self,
                             group_role,
                             policy,
                             description=None,
                             **ignore):
        """ Add rules to the specified group role.
        @param group_role: the ID of the group role.
        @param policy: the policy whose format is 'resource_typeor.operation_type'.
                        See: https://docs.qingcloud.com/api/resource_acl/AddGroupRoleRules.html
        @param description: the description of rule.
        """
        action = const.ACTION_ADD_GROUP_ROLE_RULES
        valid_keys = ['group_role', 'policy', 'description']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             required_params=['group_role', 'policy'],
                                             ):
            return None

        return self.send_request(action, body)

    def modify_group_role_rule_attributes(self,
                                          group_role_rule,
                                          description=None,
                                          policy=None,
                                          **ignore):
        """ Modify group role rule attributes.
        @param group_role_rule: the ID of group role rule whose attributes you want to modify.
        @param description: the description of group role rule.
        @param policy: the policy whose format is 'resource_type' or 'operation_type'.
        """
        action = const.ACTION_MODIFY_GROUP_ROLE_RULE_ATTRIBUTES
        valid_keys = ['group_role_rule', 'description', 'policy']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             required_params=['group_role_rule']
                                             ):
            return None

        return self.send_request(action, body)

    def delete_group_role_rules(self,
                                group_role_rules=None,
                                group_roles=None,
                                **ignore):
        """ Delete some rules of group role.
        @param group_role_rules: an array including the IDs of group role rules.
        @param group_roles: an array including the IDs of group roles.
        """
        action = const.ACTION_DELETE_GROUP_ROLE_RULES
        valid_keys = ['group_role_rules', 'group_roles']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             list_params=['group_role_rules', 'group_roles']
                                             ):
            return None

        return self.send_request(action, body)

    def grant_resource_groups_to_user_groups(self,
                                             rur_set,
                                             **ignore):
        """ Grant the resource groups to user groups.
        @param rur_set: a list which contains ID of resource group,
                        ID of user group and ID of group role.
        """
        action = const.ACTION_GRANT_RESOURCE_GROUPS_TO_USER_GROUPS
        valid_keys = ['rur_set']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             required_params=['rur_set'],
                                             list_params=['rur_set']
                                             ):
            return None

        if not self.req_checker.check_sg_rules(body.get('rur_set', [])):
            return None

        return self.send_request(action, body)

    def revoke_resource_groups_from_user_groups(self,
                                                ru_set,
                                                resource_groups=None,
                                                user_groups=None,
                                                group_roles=None,
                                                **ignore):
        """ Revoke the resource groups from user groups.
        @param ru_set: a list which contains ID of resource group and ID of user group.
        @param resource_groups: an array including IDs of resource groups.
                                if it is not empty, will revoke all authorization relationships of specified resource groups.
        @param user_groups: an array including IDs of user groups.
                            if it is not empty, will revoke all authorization relationships of specified user groups.
        @param group_roles: an array including IDs of group roles.
                            if it is not empty, will revoke all authorization relationships of specified group roles.
        """
        action = const.ACTION_REVOKE_RESOURCE_GROUPS_FROM_USER_GROUPS
        valid_keys = [
            'ru_set', 'resource_groups', 'user_groups', 'group_roles'
        ]
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             required_params=['ru_set'],
                                             list_params=[
                                                 'ru_set', 'resource_groups',
                                                 'user_groups', 'group_roles'
                                             ]
                                             ):
            return None

        if not self.req_checker.check_sg_rules(body.get('ru_set', [])):
            return None

        return self.send_request(action, body)

    def describe_resource_user_groups(self,
                                      resource_groups=None,
                                      user_groups=None,
                                      group_roles=None,
                                      limit=None,
                                      offset=None,
                                      verbose=None,
                                      sort_key=None,
                                      reverse=None,
                                      **ignore):
        """ Describe the authorization relations between resource groups and user groups.
        @param resource_groups: an array including IDs of resource groups.
        @param user_groups: an array including IDs of user groups.
        @param group_roles: an array including IDs of group roles.
        @param limit: specify the number of the returning results.
        @param offset: the starting offset of the returning results.
        @param verbose: Whether to return redundant message.
                        if it is 1, return the details of the instance related other resources.
        @param sort_key: the sort key, which defaults be create_time.
        @param reverse: 0 for Ascending order, 1 for Descending order.
        """
        action = const.ACTION_DESCRIBE_RESOURCE_USER_GROUPS
        valid_keys = [
            'resource_groups', 'user_groups',
            'group_roles', 'limit', 'offset',
            'verbose', 'sort_key', 'reverse'
        ]
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             integer_params=[
                                                 'offset', 'limit',
                                                 'verbose', 'reverse'
                                             ],
                                             list_params=[
                                                 'resource_groups',
                                                 'user_groups',
                                                 'group_roles'
                                             ]
                                             ):
            return None

        return self.send_request(action, body)

    def create_notification_list(self, notification_list_name,
                                 notification_items,
                                 **ignore):
        """ Create new notification list.
        @param notification_list_name: the name of the notification list.
        @param notification_items: an array including IDs of the notification items.
        """
        action = const.ACTION_CREATE_NOTIFICATION_LIST
        valid_keys = ['notification_list_name', 'notification_items']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             required_params=['notification_list_name', 'notification_items'],
                                             list_params=['notification_items']
                                             ):
            return None

        return self.send_request(action, body)

    def describe_notification_lists(self, notification_lists=None,
                                    search_word=None,
                                    offset=None,
                                    limit=None,
                                    **ignore):
        """ Describe notification lists filtered by condition.
        @param notification_lists: an array including the IDs of the notification lists.
        @param search_word: the search word of notification list name.
        @param offset: the starting offset of the returning results.
        @param limit: specify the number of the returning results.
        """
        action = const.ACTION_DESCRIBE_NOTIFICATION_LISTS
        valid_keys = ['notification_lists', 'search_word', 'offset', 'limit']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             required_params=[],
                                             integer_params=['offset', 'limit'],
                                             list_params=['notification_lists']):
            return None

        return self.send_request(action, body)

    def modify_notification_list_attributes(self, notification_list,
                                            notification_list_name=None,
                                            notification_items=None,
                                            **ignore):
        """ Modify notification list attributes.
        @param notification_list: The ID of notification list which attributes you want to modify.
        @param notification_list_name: The new name of the notification list which will be modified.
        @param notification_items: An array including IDs of notification items.
        """
        action = const.ACTION_MODIFY_NOTIFICATION_LIST_ATTRIBUTES
        valid_keys = ['notification_list', 'notification_list_name', 'notification_items']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             required_params=['notification_list'],
                                             integer_params=[],
                                             list_params=['notification_items']
                                             ):
            return None

        return self.send_request(action, body)

    def delete_notification_lists(self, notification_lists,
                                  **ignore):
        """ Delete one or more notification lists.
            the notification list will not be deleted along with the notification items.
        @param notification_lists: An array including IDs of the notification lists which you want to delete.
        """
        action = const.ACTION_DELETE_NOTIFICATION_LISTS
        valid_keys = ['notification_lists']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             required_params=['notification_lists'],
                                             integer_params=[],
                                             list_params=['notification_lists']
                                             ):
            return None

        return self.send_request(action, body)

    def create_notification_items(self, notification_items,
                                  **ignore):
        """ Create new notification items.
        @param notification_items: The message of notification items,each item in the array is an Object,
                                   including 'content','notification_item_type' and 'remarks'.
        """
        action = const.ACTION_CREATE_NOTIFICATION_ITEMS
        valid_keys = ['notification_items']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             required_params=['notification_items'],
                                             integer_params=[],
                                             list_params=['notification_items']
                                             ):
            return None

        return self.send_request(action, body)

    def describe_notification_items(self,
                                    notification_items=None,
                                    notification_list=None,
                                    notification_item_type=None,
                                    offset=None,
                                    limit=None,
                                    **ignore):
        """ Describe notification items filtered by condition.
        @param notification_items: An array including IDs of notification items.
        @param notification_list: The ID of notification list.
        @param notification_item_type: The type of notification item, including 'email', 'phone' and 'webhook'.
        @param offset: the starting offset of the returning results.
        @param limit: specify the number of the returning results.
        """
        action = const.ACTION_DESCRIBE_NOTIFICATION_ITEMS
        valid_keys = ['notification_items', 'notification_list', 'notification_item_type', 'offset', 'limit']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             integer_params=['offset', 'limit'],
                                             list_params=['notification_items']
                                             ):
            return None

        return self.send_request(action, body)

    def delete_notification_items(self, notification_items,
                                  **ignore):
        """ Delete one or more notification items.
        @param notification_items: An array including IDs of the notification items which you want to delete.
        """
        action = const.ACTION_DELETE_NOTIFICATION_ITEMS
        valid_keys = ['notification_items']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             required_params=['notification_items'],
                                             integer_params=[],
                                             list_params=['notification_items']
                                             ):
            return None

        return self.send_request(action, body)

    def verify_notification_item(self,
                                 notification_item_content,
                                 verification_code,
                                 **ignore):
        """ Verify the notification item.
            All notification items need to be verified to receive notifications.
        @param notification_item_content: The content of notification item which will be verified.
        @param verification_code: The verification code.
        """
        action = const.ACTION_VERIFY_NOTIFICATION_ITEM
        valid_keys = ['notification_item_content', 'verification_code']
        body = filter_out_none(locals(), valid_keys)
        if not self.req_checker.check_params(body,
                                             required_params=['notification_item_content', 'verification_code'],
                                             integer_params=[],
                                             list_params=[]
                                             ):
            return None

        return self.send_request(action, body)
