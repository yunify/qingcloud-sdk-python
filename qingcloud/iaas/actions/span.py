#!/usr/bin/env python
# coding: utf-8
# author: danta@secnium 
# time: 2020/2/27 6:19 下午


from qingcloud.iaas import constants as const
from qingcloud.misc.utils import filter_out_none


class SpanAction(object):

    def __init__(self, conn):
        self.conn = conn

    def create_span(self, span_name=None, flag=3, ip_addr=None, tunnel_type="gre", tunnel_key=0, zone=None,
                    **ignore):
        """ Create one span.
        :param span_name:
        :param flag: 镜像流量的类型：入流量：1；出流量：2；出入流量：3（默认值）
        :param ip_addr: 接受流量的服务器IP地址
        :param tunnel_type: 数据封装类型，支持：gre（默认值）
        :param tunnel_key: 数据封装使用的密钥，默认0
        :param zone: 区域ID，要小写
        """
        action = const.ACTION_CREATE_SPAN
        valid_keys = ['span_name', 'flag', 'ip_addr', 'tunnel_type', 'tunnel_key',
                      'zone']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=['ip_addr'],
                                                  integer_params=[
                                                      'flag', 'tunnel_key'],
                                                  list_params=[]
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def describe_spans(self, spans=None, span_name=None, ip_addr=None, tags=None, offset=0, limit=20, zone=None,
                       **ignore):
        """ 获取一个或多个SPAN的配置。
        可根据SPAN ID，名称， ip地址作过滤条件，来获取SPAN列表。 如果不指定任何过滤条件，默认返回你的所有SPAN。
        :param spans: SPAN ID
        :param span_name: SPAN名称
        :param ip_addr: 接收流量的服务器IP地址
        :param tags: 按照标签ID过滤, 只返回已绑定某标签的资源
        :param offset: 数据偏移量，默认为0
        :param limit: 返回数据长度，默认为20，最大100
        :param zone: 区域ID，要小写
        """
        action = const.ACTION_DESCRIBE_SPANS
        valid_keys = ['spans', 'span_name', 'ip_addr', 'tags', 'offset', 'limit', 'zone']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=[],
                                                  integer_params=[
                                                      'offset', 'limit'],
                                                  list_params=['spans']
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def delete_spans(self, spans=None, zone=None, **ignore):
        """
        删除一个或多个SPAN。
        删除SPAN的前提是没有资源依赖这个SPAN。请在删除SPAN之前，先删除所有SPAN成员。
        :param spans: SPAN ID
        :param zone: 区域ID，注意小写
        :return:
        """
        action = const.ACTION_DELETE_SPANS
        valid_keys = ['spans', 'zone']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=['spans'],
                                                  integer_params=[],
                                                  list_params=['spans']
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def add_span_members(self, span=None, resources=None, zone=None, **ignore):
        """
        给SPAN添加成员，成员可以是instance id或vxnet id。
        :param span: SPAN ID
        :param resources: SPAN成员，可以是instance id或vxnet id
        :param zone: 区域id，注意要小写
        """
        action = const.ACTION_ADD_SPAN_MEMBERS
        valid_keys = ['spans', 'resources', 'zone']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=['span', 'resources'],
                                                  integer_params=['resources'],
                                                  list_params=[]
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def remove_span_members(self, span=None, resources=None, zone=None, **ignore):
        """
        给SPAN删除成员，成员可以是instance id或vxnet id。
        :param span: SPAN ID
        :param resources: SPAN成员，可以是instance id或vxnet id
        :param zone: 区域ID，注意要小写
        """
        action = const.ACTION_REMOVE_SPAN_MEMBERS
        valid_keys = ['span', 'resources', 'zone']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=['span', 'resources'],
                                                  integer_params=['resources'],
                                                  list_params=[]
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def modify_span_attributes(self, span_id=None, span_name=None, flag=3, ip_addr=None, tunnel_type="gre",
                               tunnel_key=0, zone=None, **ignore):
        """
        修改SPAN属性，包括IP地址，流量类型
        :param span_id: SPAN ID
        :param span_name: SPAN名称
        :param flag: 镜像流量的类型：入流量：1；出流量：2；出入流量：3（默认值）
        :param ip_addr: 接受流量的服务器IP地址
        :param tunnel_type: 数据封装类型：支持：gre（默认值）
        :param tunnel_key: 数据封装使用的俄密钥，默认0
        :param zone: 区域ID，注意要小写
        """
        action = const.ACTION_MODIFY_SPAN_ATTRIBUTES
        valid_keys = ['span_id', 'span_name', 'flag', 'ip_addr', 'tunnel_type', 'tunnel_key', 'zone']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=['span_id'],
                                                  integer_params=['flag', 'tunnel_key'],
                                                  list_params=[]
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def updata_span(self, span=None, zone=None, **ignore):
        """
        在修改SPAN属性后使用，应用变更到所有主机
        :param span: SPAN ID
        :param zone: 区域 ID，注意要小写
        """
        action = const.ACTION_UPDATE_SPAN
        valid_keys = ['span', 'zone']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=['span'],
                                                  integer_params=[],
                                                  list_params=[]
                                                  ):
            return None

        return self.conn.send_request(action, body)
