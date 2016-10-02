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

import json

from qingcloud.iaas.errors import InvalidRouterStatic


class RouterStaticFactory(object):
    """ Use this factory to facilitate to create router static

    Example:
    static = RouterStaticFactory.create(
        RouterStaticFactory.TYPE_PORT_FORWARDING,
        src_port=80,
        dst_ip="192.168.0.2",
        dst_port=80,
        protocol="tcp",
    )
    statics = [static.to_json()]
    conn.add_router_statics(router_id, statics)
    """

    TYPE_PORT_FORWARDING = 1
    TYPE_VPN = 2
    TYPE_DHCP = 3
    TYPE_TUNNEL = 4
    TYPE_FILTERING = 5
    TYPE_L3GRE = 6
    TYPE_IPSEC = 7
    TYPE_DNS = 8

    PPTP_DEFAULT_CONNS = 100

    @classmethod
    def create(cls, static_type, router_static_id='', **kw):
        """ Create router static.
        """
        if static_type not in STATIC_MAPPER:
            raise InvalidRouterStatic('invalid static type[%s]' % static_type)

        clazz = STATIC_MAPPER[static_type]
        kw = clazz.extract(kw)
        inst = clazz(**kw)
        inst.router_static_id = router_static_id
        return inst

    @classmethod
    def create_from_string(cls, string):
        """ Create router static from json formatted string.
        """
        data = json.loads(string)
        if isinstance(data, dict):
            return cls.create(**data)
        if isinstance(data, list):
            return [cls.create(**item) for item in data]


class _RouterStatic(object):
    """ _RouterStatic is used to define static rule in router.
    """

    router_static_id = None
    static_type = None

    def __repr__(self):
        return '<%s>%s' % (self.__class__.__name__, self.to_json())

    @staticmethod
    def extract(kw):
        raise NotImplementedError

    def extra_props(self):
        raise NotImplementedError

    def to_json(self):
        props = {
            'router_static_id': self.router_static_id,
            'static_type': self.static_type,
        }
        props.update(self.extra_props())
        return props


class _StaticForPortForwarding(_RouterStatic):

    static_type = RouterStaticFactory.TYPE_PORT_FORWARDING

    def __init__(self, src_port, dst_ip, dst_port, protocol='tcp',
                 router_static_name='', **kw):
        super(_StaticForPortForwarding, self).__init__()
        self.router_static_name = router_static_name
        self.src_port = src_port
        self.dst_ip = dst_ip
        self.dst_port = dst_port
        self.protocol = protocol

    @staticmethod
    def extract(kw):
        if 'val1' in kw:
            kw['src_port'] = kw.pop('val1')
        if 'val2' in kw:
            kw['dst_ip'] = kw.pop('val2')
        if 'val3' in kw:
            kw['dst_port'] = kw.pop('val3')
        if 'val4' in kw:
            kw['protocol'] = kw.pop('val4')
        return kw

    def extra_props(self):
        return {
            'router_static_name': self.router_static_name,
            'val1': self.src_port,
            'val2': self.dst_ip,
            'val3': self.dst_port,
            'val4': self.protocol,
        }


class _StaticForVPN(_RouterStatic):

    class OpenVPN(object):

        def __init__(self, ip_network, serv_port='1194', serv_protocol='udp',
                     **kw):
            self.serv_port = serv_port
            self.serv_protocol = serv_protocol
            self.ip_network = ip_network

        def extra_props(self):
            return {
                'val1': 'openvpn',
                'val2': self.serv_port,
                'val3': self.serv_protocol,
                'val4': self.ip_network,
            }

    class PPTP(object):

        def __init__(self, usr, pwd, ip_network,
                     max_conn_cnt=RouterStaticFactory.PPTP_DEFAULT_CONNS, **kw):
            self.usr = usr
            self.pwd = pwd
            self.max_conn_cnt = max_conn_cnt
            self.ip_network = ip_network

        def extra_props(self):
            return {
                'val1': 'pptp',
                'val2': '%s:%s' % (self.usr, self.pwd),
                'val3': self.max_conn_cnt,
                'val4': self.ip_network,
            }

    static_type = RouterStaticFactory.TYPE_VPN

    def __init__(self, vpn_type='', **kw):
        super(_StaticForVPN, self).__init__()
        vpn_type = vpn_type or kw.get('val1')
        if vpn_type == 'openvpn':
            self.inst = _StaticForVPN.OpenVPN(**kw)
        elif vpn_type == 'pptp':
            self.inst = _StaticForVPN.PPTP(**kw)
        else:
            raise InvalidRouterStatic('unsupported vpn type[%s]' % vpn_type)

    @staticmethod
    def extract(kw):
        vpn_type = kw.get('val1')
        if vpn_type == 'openvpn':
            if 'val2' in kw:
                kw['serv_port'] = kw.pop('val2')
            if 'val3' in kw:
                kw['serv_protocol'] = kw.pop('val3')
            if 'val4' in kw:
                kw['ip_network'] = kw.pop('val4')
        elif vpn_type == 'pptp':
            if 'entry_set' in kw:
                entry_set = kw['entry_set']
                kw['usr'] = entry_set[0]['val1']
                kw['pwd'] = ''
            if 'val3' in kw:
                kw['max_conn_cnt'] = kw.pop('val3')
            if 'val4' in kw:
                kw['ip_network'] = kw.pop('val4')
        return kw

    def extra_props(self):
        return self.inst.extra_props()


class _StaticForDHCP(_RouterStatic):

    static_type = RouterStaticFactory.TYPE_DHCP

    def __init__(self, instance_id, dhcp_config, **kw):
        """
        @param instance_id: ID of instance
        @param dhcp_config: Formatted string "key1=val1&key2=val2" such as
                            "domain-name-servers=8.8.8.8;fixed-address=192.168.1.2"
        """
        super(_StaticForDHCP, self).__init__()
        self.instance_id = instance_id
        self.dhcp_config = dhcp_config

    @staticmethod
    def extract(kw):
        if "val1" in kw:
            kw['instance_id'] = kw["val1"]
        if "val2" in kw:
            kw['dhcp_config'] = kw["val2"]
        return kw

    def extra_props(self):
        return {
            'val1': self.instance_id,
            'val2': self.dhcp_config,
        }


class _StaticForTunnel(_RouterStatic):

    static_type = RouterStaticFactory.TYPE_TUNNEL

    def __init__(self, vxnet_id, tunnel_entries, **kw):
        """
        @param tunnel_entries: [(tunnel_type, ip_network, key), ...]
        """
        super(_StaticForTunnel, self).__init__()
        self.vxnet_id = vxnet_id
        self.tunnel_entries = tunnel_entries

    @staticmethod
    def extract(kw):
        if 'val1' in kw:
            kw['tunnel_entries'] = [tuple(entry.split('|'))
                                    for entry in kw.pop('val1').split(';')]
        return kw

    def extra_props(self):
        return {
            'vxnet_id': self.vxnet_id,
            'val1': ';'.join('%s|%s|%s' % entry for entry in self.tunnel_entries),
        }


class _StaticForFiltering(_RouterStatic):

    static_type = RouterStaticFactory.TYPE_FILTERING

    def __init__(self, router_static_name='', src_ip='', src_port='',
                 dst_ip='', dst_port='', priority='1', action='', **kw):
        super(_StaticForFiltering, self).__init__()
        self.router_static_name = router_static_name
        self.src_ip = src_ip
        self.src_port = src_port
        self.dst_ip = dst_ip
        self.dst_port = dst_port
        self.priority = priority
        self.action = action

    @staticmethod
    def extract(kw):
        if 'val1' in kw:
            kw['src_ip'] = kw.pop('val1')
        if 'val2' in kw:
            kw['src_port'] = kw.pop('val2')
        if 'val3' in kw:
            kw['dst_ip'] = kw.pop('val3')
        if 'val4' in kw:
            kw['dst_port'] = kw.pop('val4')
        if 'val5' in kw:
            kw['priority'] = kw.pop('val5')
        if 'val6' in kw:
            kw['action'] = kw.pop('val6')
        return kw

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


class _StaticForL3GRE(_RouterStatic):

    static_type = RouterStaticFactory.TYPE_L3GRE

    def __init__(self, peer_config, target_network, **kw):
        """
        @param peer_config: GRE peer config, formatted as
                "remote ip|key|local peer ip|remote peer ip",
                such as "6.6.6.6|1010|10.254.1.2|10.254.1.3"
        @param target_network: "|" separated multiple networks,
                such as "172.17.10.0/24|172.17.20.0/24"
        """
        super(_StaticForL3GRE, self).__init__()
        self.peer_config = peer_config
        self.target_network = target_network

    @staticmethod
    def extract(kw):
        if "val1" in kw:
            kw['peer_config'] = kw["val1"]
        if "val2" in kw:
            kw['target_network'] = kw["val2"]
        return kw

    def extra_props(self):
        return {
            'val1': self.peer_config,
            'val2': self.target_network,
        }


class _StaticForIPSEC(_RouterStatic):

    static_type = RouterStaticFactory.TYPE_IPSEC

    def __init__(self, peer_config, local_network, target_network, **kw):
        """
        @param peer_config: IPSec peer config, formatted as
                "remote ip|alg|key|remote device",
                such as "1.2.3.4|aes|passw0rd|device-id"
        @param target_network: "|" separated multiple networks,
                such as "172.17.10.0/24|172.17.20.0/24"
        """
        super(_StaticForIPSEC, self).__init__()
        self.peer_config = peer_config
        self.local_network = local_network
        self.target_network = target_network

    @staticmethod
    def extract(kw):
        if "val1" in kw:
            kw['peer_config'] = kw["val1"]
        if "val2" in kw:
            kw['local_network'] = kw["val2"]
        if "val3" in kw:
            kw['target_network'] = kw["val2"]
        return kw

    def extra_props(self):
        return {
            'val1': self.peer_config,
            'val2': self.local_network,
            'val3': self.target_network,
        }


class _StaticForDNS(_RouterStatic):

    static_type = RouterStaticFactory.TYPE_DNS

    def __init__(self, local_domain, local_addr, **kw):
        """
        @param local_domain: domain in private network
        @param local_addr: comma separated local IP address
        """
        super(_StaticForDNS, self).__init__()
        self.local_domain = local_domain
        self.local_addr = local_addr

    @staticmethod
    def extract(kw):
        if "val1" in kw:
            kw['local_domain'] = kw["val1"]
        if "val2" in kw:
            kw['local_addr'] = kw["val2"]
        return kw

    def extra_props(self):
        return {
            'val1': self.local_domain,
            'val2': self.local_addr,
        }


STATIC_MAPPER = {
    RouterStaticFactory.TYPE_PORT_FORWARDING: _StaticForPortForwarding,
    RouterStaticFactory.TYPE_VPN: _StaticForVPN,
    RouterStaticFactory.TYPE_DHCP: _StaticForDHCP,
    RouterStaticFactory.TYPE_TUNNEL: _StaticForTunnel,
    RouterStaticFactory.TYPE_FILTERING: _StaticForFiltering,
    RouterStaticFactory.TYPE_L3GRE: _StaticForL3GRE,
    RouterStaticFactory.TYPE_IPSEC: _StaticForIPSEC,
    RouterStaticFactory.TYPE_DNS: _StaticForDNS,
}
