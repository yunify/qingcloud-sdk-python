#!/usr/bin/env python
# coding: utf-8
# author: danta@secnium 
# time: 2020/2/27 5:47 下午


from qingcloud.iaas import constants as const
from qingcloud.misc.utils import filter_out_none


class NatAction(object):

    def __init__(self, conn):
        self.conn = conn

    def create_nfv(self, nfv_name=None, nfv_type=1, nfv_spec=1, vxnets=None, zone=None, security_group=None, owner=None,
                   eips=None, cluster_mode=None, **ignore):
        """ Create one nfv.
        :param vxnets: 绑定的公网私有网络
        :param cluster_mode: 集群模式 无论选啥值都为1
        :param eips: 绑定的公网ips
        :param nfv_name: the name of nfv
        :param nfv_type: 部署方式 无论选啥值都为1
        :param nfv_spec: nfv 规格 1：小型  2：中型 3：大型
        :param zone: 地区
        :param security_group: 防火墙策略
        :param owner: 账号，可以为子账号
        """
        action = const.ACTION_CREATE_NFV
        valid_keys = ['nfv_name', 'nfv_type', 'nfv_spec', 'zone', 'security_group',
                      'owner', 'cluster_mode', 'eips']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=[],
                                                  integer_params=[
                                                      'nfv_spec', 'nfv_type', 'cluster_mode'],
                                                  list_params=['eips', 'vxnets']
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def delete_nfvs(self, nfvs=None, owner=None, zone=None, **ignore):
        """
        删除nfvs
        :param nfv: the array of nfv
        :param owner: 可为子账号
        :param zone: 区域ID
        """
        action = const.ACTION_DELETE_NFVS
        valid_keys = ['nfvs', 'owner', 'zone']
        body = filter_out_none(locals(), valid_keys)

        if not self.conn.req_checker.check_params(body,
                                                  required_params=['nfvs'],
                                                  integer_params=[],
                                                  list_params=['nfvs']
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def describe_nfvs(self, nfvs=None, status=None, owner=None, sort_key=None, reverse=None, zone=None, verbose=None,
                      offset=None,
                      limit=None, **ignore):
        """
        get info of nfvs
        :param nfvs: id of nfvs
        :param status: nfv的状态 包括: pending, active, stopped, suspended等
        :param owner: 账号
        :param sort_key: the sort key, which defaults be create_time. 此参数并不管用
        :param reverse: 0 for Ascending order, 1 for Descending order. 此参数并不管用
        :param zone: zone id
        :param verbose: the number to specify the verbose level,
                        larger the number, the more detailed information will be returned.
        :param offset: the starting offset of the returning results. 此参数并不管用
        :param limit: specify the number of the returning results.
        """
        action = const.ACTION_DESCRIBE_NFVS
        valid_keys = ['nfvs', 'status', 'owner', 'sort_key', 'reverse', 'zone'
                                                                        'verbose', 'offset', 'limit']
        body = filter_out_none(locals(), valid_keys)

        if not self.conn.req_checker.check_params(body,
                                                  required_params=[],
                                                  integer_params=['verbose', 'offset', 'limit', 'reverse'],
                                                  list_params=['status', 'nfvs']
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def modify_nfv_attributes(self, nfv=None, nfv_name=None, description=None, owner=None, zone=None, **ignore):
        """
        修改nfv属性
        :param nfv: nfv id
        :param nfv_name:  nfv名字
        :param description: nfv 描述
        :param owner: 可为子账号
        :param zone: 区域ID
        """
        action = const.ACTION_MODIFY_NFV_ATTRIBUTES
        valid_keys = ['nfv', 'nfv_name', 'description', 'owner', 'zone']
        body = filter_out_none(locals(), valid_keys)

        if not self.conn.req_checker.check_params(body,
                                                  required_params=['nfv'],
                                                  integer_params=[],
                                                  list_params=[]
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def resize_nfv(self, nfv=None, nfv_spec=None, owner=None, zone=None, **ignore):
        """
        扩容
        :param nfv: nfv id
        :param nfv_spec:  nfv 规格 1：小型  2：中型 3：大型
        :param owner: 可为子账号
        :param zone: 区域ID
        """
        action = const.ACTION_RESIZE_NFV
        valid_keys = ['nfv', 'nfv_spec', 'owner', 'zone']
        body = filter_out_none(locals(), valid_keys)

        if not self.conn.req_checker.check_params(body,
                                                  required_params=['nfv', 'nfv_spec'],
                                                  integer_params=[],
                                                  list_params=[]
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def stop_nfvs(self, nfvs=None, reboot=0, owner=None, zone=None, **ignore):
        """
        nfvs关机
        :param nfvs: nfv ids
        :param reboot:  0:直接关机(默认值) 1：重启
        :param owner: 可为子账号
        :param zone: 区域ID
        """
        action = const.ACTION_STOP_NFVS
        valid_keys = ['nfvs', 'reboot', 'owner', 'zone']
        body = filter_out_none(locals(), valid_keys)

        if not self.conn.req_checker.check_params(body,
                                                  required_params=['nfvs'],
                                                  integer_params=['reboot'],
                                                  list_params=['nfvs']
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def start_nfvs(self, nfvs=None, owner=None, zone=None, **ignore):
        """
        nfvs开机
        :param nfvs: nfv ids
        :param owner: 可为子账号
        :param zone: 区域ID
        """
        action = const.ACTION_START_NFVS
        valid_keys = ['nfvs', 'owner', 'zone']
        body = filter_out_none(locals(), valid_keys)

        if not self.conn.req_checker.check_params(body,
                                                  required_params=['nfvs'],
                                                  integer_params=[],
                                                  list_params=['nfvs']
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def associate_eips_to_nfv(self, nfv=None, limit=None, eips=None, eip_addrs=None, owner=None, zone=None, **ignore):
        """
        nfv绑定公网IP
        :param nfv: nfv id
        :param eips: the array of eip
        :param owner: 可为子账号
        :param zone: 区域ID
        """
        action = const.ACTION_ASSOCIATE_EIPS_TO_NFV
        valid_keys = ['nfv', 'eips', 'owner', 'zone']
        body = filter_out_none(locals(), valid_keys)

        if not self.conn.req_checker.check_params(body,
                                                  required_params=['nfv', 'eips'],
                                                  integer_params=[],
                                                  list_params=['eips']
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def dissociate_eips_from_nfv(self, nfv=None, eips=None, owner=None, zone=None, **ignore):
        """
        nfv解绑公网IP
        :param nfv: nfv id
        :param eips: the array of eip
        :param owner: 可为子账号
        :param zone: 区域ID
        """
        action = const.ACTION_DISSOCIATE_EIPS_FROM_NFV
        valid_keys = ['nfv', 'eips', 'owner', 'zone']
        body = filter_out_none(locals(), valid_keys)

        if not self.conn.req_checker.check_params(body,
                                                  required_params=['nfv', 'eips'],
                                                  integer_params=[],
                                                  list_params=['eips']
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def nfv_join_vxnets(self, nfv=None, vxnets=None, owner=None, zone=None, **ignore):
        """
        nfv绑定私有网络
        :param nfv: nfv id
        :param vxnets: the array of 私有网络
        :param owner: 可为子账号
        :param zone: 区域ID
        """
        action = const.ACTION_NFV_JOIN_VXNETS
        valid_keys = ['nfv', 'vxnets', 'owner', 'zone']
        body = filter_out_none(locals(), valid_keys)

        if not self.conn.req_checker.check_params(body,
                                                  required_params=['nfv', 'vxnets'],
                                                  integer_params=[],
                                                  list_params=['vxnets']
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def nfv_leave_vxnets(self, nfv=None, vxnets=None, owner=None, zone=None, **ignore):
        """
        nfv解绑私有网络
        :param nfv: nfv id
        :param vxnets: the array of 私有网络
        :param owner: 可为子账号
        :param zone: 区域ID
        """
        action = const.ACTION_NFV_LEAVE_VXNETS
        valid_keys = ['nfv', 'vxnets', 'owner', 'zone']
        body = filter_out_none(locals(), valid_keys)

        if not self.conn.req_checker.check_params(body,
                                                  required_params=['nfv', 'vxnets'],
                                                  integer_params=[],
                                                  list_params=['vxnets']
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def modify_nfv_security_groups(self, nfv=None, vxnets=None, security_group=None, owner=None, zone=None, **ignore):
        """
        修改nfv安全策略
        :param nfv: nfv id
        :param vxnets: the array of 私有网络
        :param security_group: 安全策略
        :param owner: 可为子账号
        :param zone: 区域ID
        """
        action = const.ACTION_MODIFY_NFV_SECURITY_GROUPS
        valid_keys = ['nfv', 'vxnets', 'security_group', 'owner', 'zone']
        body = filter_out_none(locals(), valid_keys)

        if not self.conn.req_checker.check_params(body,
                                                  required_params=['nfv', 'vxnets', 'security_group'],
                                                  integer_params=[],
                                                  list_params=['vxnets']
                                                  ):
            return None

        return self.conn.send_request(action, body)
