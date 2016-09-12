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

import unittest

from qingcloud.iaas.errors import InvalidRouterStatic
from qingcloud.iaas.router_static import (RouterStaticFactory, _StaticForTunnel,
                                          _StaticForFiltering, _StaticForVPN, _StaticForPortForwarding)


class RouterStaticFactoryTestCase(unittest.TestCase):

    def test_port_forwarding_static(self):
        name = 'unittest'
        src_port = 10
        dst_ip = '192.168.1.1'
        dst_port = 80
        protocol = 'udp'
        static = RouterStaticFactory.create(RouterStaticFactory.TYPE_PORT_FORWARDING,
                                            router_static_name=name, protocol=protocol,
                                            src_port=10, dst_ip='192.168.1.1', dst_port=80)

        json_data = static.to_json()
        self.assertEqual(json_data['router_static_name'], name)
        self.assertEqual(json_data['val1'], src_port)
        self.assertEqual(json_data['val2'], dst_ip)
        self.assertEqual(json_data['val3'], dst_port)
        self.assertEqual(json_data['val4'], protocol)

    def test_vpn_static(self):
        ip = '192.168.1.1'
        vpn_type = 'openvpn'
        static = RouterStaticFactory.create(RouterStaticFactory.TYPE_VPN,
                                            vpn_type=vpn_type, ip_network=ip)
        json_data = static.to_json()
        self.assertEqual(json_data['val1'], 'openvpn')
        self.assertEqual(json_data['val2'], '1194')
        self.assertEqual(json_data['val3'], 'udp')
        self.assertEqual(json_data['val4'], ip)

        vpn_type = 'pptp'
        usr = 'tester'
        pwd = 'passwd'
        static = RouterStaticFactory.create(RouterStaticFactory.TYPE_VPN,
                                            vpn_type=vpn_type, usr=usr, pwd=pwd, ip_network=ip)
        json_data = static.to_json()
        self.assertEqual(json_data['val1'], 'pptp')
        self.assertEqual(json_data['val2'], '%s:%s' % (usr, pwd))
        self.assertEqual(json_data['val3'],
                         RouterStaticFactory.PPTP_DEFAULT_CONNS)
        self.assertEqual(json_data['val4'], ip)

    def test_invalid_vpn_static(self):
        vpn_type = 'invalid'
        usr = 'tester'
        pwd = 'passwd'
        ip = '192.168.1.1'
        self.assertRaises(InvalidRouterStatic, RouterStaticFactory.create,
                          RouterStaticFactory.TYPE_VPN, vpn_type=vpn_type,
                          usr=usr, pwd=pwd, ip_network=ip)

    def test_tunnel_static(self):
        vxnet = 'vxnet-1234abcd'
        tunnel_entries = [
            ('gre', '112.144.3.54', '123'),
            ('gre', '112.144.5.54', 'abc'),
        ]
        static = RouterStaticFactory.create(RouterStaticFactory.TYPE_TUNNEL,
                                            vxnet_id=vxnet, tunnel_entries=tunnel_entries)

        json_data = static.to_json()
        self.assertEqual(json_data['val1'],
                         'gre|112.144.3.54|123;gre|112.144.5.54|abc')

    def test_filtering_static(self):
        name = 'unittest'
        src_ip = '192.168.1.1'
        src_port = 10
        dst_ip = '192.168.2.1'
        dst_port = 80
        priority = 5
        action = 'drop'
        static = RouterStaticFactory.create(RouterStaticFactory.TYPE_FILTERING,
                                            router_static_name=name, src_ip=src_ip, src_port=src_port,
                                            dst_ip=dst_ip, dst_port=dst_port, priority=priority, action=action)

        json_data = static.to_json()
        self.assertEqual(json_data['val1'], src_ip)
        self.assertEqual(json_data['val2'], src_port)
        self.assertEqual(json_data['val3'], dst_ip)
        self.assertEqual(json_data['val4'], dst_port)
        self.assertEqual(json_data['val5'], priority)
        self.assertEqual(json_data['val6'], action)

    def test_static_with_existing_id(self):
        static = RouterStaticFactory.create(RouterStaticFactory.TYPE_VPN,
                                            vpn_type='openvpn', ip_network='', router_static_id='fakeid')

        json_data = static.to_json()
        self.assertEqual(json_data['router_static_id'], 'fakeid')

    def test_unsupported_static_type(self):
        self.assertRaises(InvalidRouterStatic,
                          RouterStaticFactory.create, 'unsupported')

    def test_create_multiple_statics_from_string(self):
        string = '''
        [{
          "router_id": "rtr-1234abcd", "vxnet_id": "",
          "router_static_name": "filter", "static_type": 5,
          "router_static_id": "rtrs-1234abcd", "console_id": "qingcloud",
          "val3": "192.168.100.3", "controller": "self",
          "create_time": "2013-11-11T07:02:14Z", "val2": "80",
          "val1": "192.168.1.2", "val6": "drop", "val5": "4", "val4": "800"
        },

        {
          "router_id":"rtr-1234abcd","vxnet_id":"","router_static_name":null,
          "static_type":2,"router_static_id":"rtrs-1234abcd",
          "console_id":"qingcloud","val3":"tcp","controller":"self",
          "create_time":"2014-01-27T11:22:30Z",
          "val2":"1194","val1":"openvpn","val6":"","val5":"","val4":"10.255.1.0/24"
        },

        {
          "router_id":"rtr-ji5ais2q",
          "entry_set": [{"router_static_entry_id":"rse-gbgwguzq","val1":"test"}],
          "vxnet_id":"","router_static_id":"rtrs-9fh7wxrf","static_type":2,
          "router_static_name":null,"console_id":"qingcloud","val3":"253",
          "controller":"self","create_time":"2014-01-27T11:22:42Z",
          "owner":"usr-qkMLt5Oo","val2":"","val1":"pptp","val6":"","val5":"",
          "val4":"10.255.2.0/24"
        },

        {
          "router_id": "rtr-1234abcd", "vxnet_id": "",
          "router_static_name": "fp1", "static_type": 1,
          "router_static_id": "rtrs-1234abcd", "console_id": "qingcloud",
          "val3": "80", "controller": "self", "create_time": "2014-01-26T16:58:51Z",
          "val2": "192.168.100.2", "val1": "80", "val6": "", "val5": "", "val4": "tcp"
        },

        {
          "router_id": "rtr-1234abcd", "vxnet_id": "vxnet-1234abcd",
          "router_static_name": null, "static_type": 4,
          "router_static_id": "rtrs-1234abcd", "console_id": "qingcloud",
          "val3": "", "controller": "self", "create_time": "2013-11-11T03:02:37Z",
          "val2": "", "val1": "gre|182.32.32.1|1234;gre|12.1.12.2|123123",
          "val6": "", "val5": "", "val4": ""
        }]
        '''
        rtrs = RouterStaticFactory.create_from_string(string)
        self.assertEqual(len(rtrs), 5)
        self.assertTrue(isinstance(rtrs[0], _StaticForFiltering))
        self.assertTrue(isinstance(rtrs[1], _StaticForVPN))
        self.assertTrue(isinstance(rtrs[2], _StaticForVPN))
        self.assertTrue(isinstance(rtrs[3], _StaticForPortForwarding))
        self.assertTrue(isinstance(rtrs[4], _StaticForTunnel))

    def test_create_single_static_from_string(self):
        string = '''
        {
          "router_id": "rtr-1234abcd", "vxnet_id": "",
          "router_static_name": "filter", "static_type": 5,
          "router_static_id": "rtrs-1234abcd", "console_id": "qingcloud",
          "val3": "192.168.100.3", "controller": "self",
          "create_time": "2013-11-11T07:02:14Z", "val2": "80",
          "val1": "192.168.1.2", "val6": "drop", "val5": "4", "val4": "800"
        }
        '''
        rtr = RouterStaticFactory.create_from_string(string)
        self.assertTrue(isinstance(rtr, _StaticForFiltering))
