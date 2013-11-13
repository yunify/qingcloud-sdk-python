# coding: utf-8

import json

class RouterStatic(object):
    """
    RouterStatic is used to define static rule in router.
    """
    TYPE_PORT_FORWARDING = 1
    TYPE_VPN = 2
    TYPE_TUNNEL = 4
    TYPE_FILTERING = 5

    router_static_id = None
    static_type = None

    @classmethod
    def create(cls, static_type, router_static_id='', **kw):
        clazz = STATIC_MAPPER.get(static_type)
        if not clazz:
            return None

        inst = clazz(**kw)
        inst.static_type = static_type
        inst.router_static_id = router_static_id
        return inst

    def extra_props(self):
        raise NotImplementedError

    def to_json(self):
        props = {
                'router_static_id': self.router_static_id,
                'static_type': self.static_type,
                }
        props.update(self.extra_props())
        return props

    @classmethod
    def create_from_string(cls, string):
        if not isinstance(string, basestring):
            return string
        data = json.loads(string)
        if isinstance(data, dict):
            return cls.create(**data)
        if isinstance(data, list):
            return [cls.create(**item) for item in data]

    def __repr__(self):
        return '<%s>%s' % (self.__class__.__name__, self.to_json())
 

class StaticForPortForwarding(RouterStatic):

    def __init__(self, router_static_name='', src_port='', dst_ip='',
            dst_port='', protocol='tcp', **kw):
        super(StaticForPortForwarding, self).__init__()
        self.router_static_name = router_static_name
        self.src_port = src_port or kw.get('val1', '')
        self.dst_ip = dst_ip or kw.get('val2', '')
        self.dst_port = dst_port or kw.get('val3', '')
        self.protocol = protocol or kw.get('val4', '')

    def extra_props(self):
        return {
                'router_static_name': self.router_static_name,
                'val1': self.src_port,
                'val2': self.dst_ip,
                'val3': self.dst_port,
                'val4': self.protocol,
                }


class StaticForVPN(RouterStatic):

    def __init__(self, vpn_type='openvpn', serv_port='1194',
            serv_protocol='udp', ip_network='', **kw):
        super(StaticForVPN, self).__init__()
        self.vpn_type = vpn_type or kw.get('val1', '')
        self.serv_port = serv_port or kw.get('val2', '')
        self.serv_protocol = serv_protocol or kw.get('val3', '')
        self.ip_network = ip_network or kw.get('val4', '')

    def extra_props(self):
        return {
                'val1': self.vpn_type,
                'val2': self.serv_port,
                'val3': self.serv_protocol,
                'val4': self.ip_network,
                }


class StaticForTunnel(RouterStatic):

    def __init__(self, vxnet='', value='', **kw):
        """
        @param value: formatted string "tunnel_type|remote_ip|key"
        """
        super(StaticForTunnel, self).__init__()
        self.vxnet = vxnet
        self.value = value or kw.get('val1', '')

    def extra_props(self):
        return {
                'vxnet_id': self.vxnet,
                'val1': self.value,
                }


class StaticForFiltering(RouterStatic):

    def __init__(self, router_static_name='', src_ip='', src_port='',
            dst_ip='', dst_port='', priority='1', action='', **kw):
        super(StaticForFiltering, self).__init__()
        self.router_static_name = router_static_name
        self.src_ip = src_ip or kw.get('val1', '')
        self.src_port = src_port or kw.get('val2', '')
        self.dst_ip = dst_ip or kw.get('val3', '')
        self.dst_port = dst_port or kw.get('val4', '')
        self.priority = priority if priority != '' else kw.get('val5', '')
        self.action = action or kw.get('val6', '')

    def extra_props(self):
        return {
                'router_static_name': self.router_static_name,
                'val1': self.src_ip,
                'val2': self.src_port,
                'val3': self.dst_ip,
                'val4': self.dst_port,
                'val5': self.priority,
                'val6': self.action,
                }

STATIC_MAPPER = {
        RouterStatic.TYPE_PORT_FORWARDING: StaticForPortForwarding,
        RouterStatic.TYPE_VPN: StaticForVPN,
        RouterStatic.TYPE_TUNNEL: StaticForTunnel,
        RouterStatic.TYPE_FILTERING: StaticForFiltering,
        }


