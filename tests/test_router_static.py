import unittest

from qingcloud.iaas.router_static import RouterStatic, StaticForTunnel, StaticForFiltering

class RouterStaticTestCase(unittest.TestCase):

    def test_port_forwarding_static(self):
        name = 'unittest'
        src_port = 10
        dst_ip = '192.168.1.1'
        dst_port = 80
        static = RouterStatic.create(RouterStatic.TYPE_PORT_FORWARDING,
                router_static_name='unittest',
                src_port=10, dst_ip='192.168.1.1', dst_port=80)

        json_data = static.to_json()
        self.assertEqual(json_data['router_static_name'], name)
        self.assertEqual(json_data['val1'], src_port)
        self.assertEqual(json_data['val2'], dst_ip)
        self.assertEqual(json_data['val3'], dst_port)

    def test_vpn_static(self):
        ip = '192.168.1.1'
        static = RouterStatic.create(RouterStatic.TYPE_VPN,
                ip_network=ip)

        json_data = static.to_json()
        self.assertEqual(json_data['val1'], 'openvpn')
        self.assertEqual(json_data['val2'], '1194')
        self.assertEqual(json_data['val3'], 'udp')
        self.assertEqual(json_data['val4'], ip)

    def test_tunnel_static(self):
        value = 'gre|112.144.3.54|666666'
        static = RouterStatic.create(RouterStatic.TYPE_TUNNEL,
                value=value)

        json_data = static.to_json()
        self.assertEqual(json_data['val1'], value)

    def test_filtering_static(self):
        name = 'unittest'
        src_ip = '192.168.1.1'
        src_port = 10
        dst_ip = '192.168.2.1'
        dst_port = 80
        priority = 5
        action = 'drop'
        static = RouterStatic.create(RouterStatic.TYPE_FILTERING,
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
        static = RouterStatic.create(RouterStatic.TYPE_VPN,
                router_static_id='fakeid')

        json_data = static.to_json()
        self.assertEqual(json_data['router_static_id'], 'fakeid')

    def test_unsupported_static_type(self):
        static = RouterStatic.create('notsupport')
        self.assertFalse(static)

    def test_create_from_string(self):
        string = '''
        [{
          "router_id": "rtr-dskfecv6", "vxnet_id": "",
          "router_static_name": "filter", "static_type": 5,
          "router_static_id": "rtrs-lz29w0te", "console_id": "qingcloud",
          "val3": "192.168.100.3", "controller": "self",
          "create_time": "2013-11-11T07:02:14Z", "owner": "usr-F5iqdERj",
          "val2": "80", "val1": "192.168.1.2", "val6": "drop", "val5": "4",
          "val4": "800"
        },

        {"router_id": "rtr-dskfecv6", "vxnet_id": "vxnet-bctyex9",
          "router_static_name": null, "static_type": 4,
          "router_static_id": "rtrs-j6yzruhw", "console_id": "qingcloud",
          "val3": "", "controller": "self", "create_time": "2013-11-11T03:02:37Z",
          "owner": "usr-F5iqdERj", "val2": "",
          "val1": "gre|182.32.32.1|1234;gre|12.1.12.2|123123",
          "val6": "", "val5": "", "val4": ""}]
        '''
        rtrs = RouterStatic.create_from_string(string)
        self.assertEqual(len(rtrs), 2)
        self.assertTrue(isinstance(rtrs[0], StaticForFiltering))
        self.assertTrue(isinstance(rtrs[1], StaticForTunnel))
