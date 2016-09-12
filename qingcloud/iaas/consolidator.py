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

"""
Check parameters in request
"""
import re

from qingcloud.iaas.errors import InvalidParameterError
from qingcloud.iaas.router_static import RouterStaticFactory
from qingcloud.misc.utils import parse_ts


class RequestChecker(object):

    def err_occur(self, error_msg):
        raise InvalidParameterError(error_msg)

    def is_integer(self, value):
        try:
            int(value)
        except:
            return False
        return True

    def check_integer_params(self, directive, params):
        """ Specified params should be `int` type if in directive
        @param directive: the directive to check
        @param params: the params that should be `int` type.
        """
        for param in params:
            if param not in directive:
                continue
            val = directive[param]
            if self.is_integer(val):
                directive[param] = int(val)
            else:
                self.err_occur(
                    "parameter [%s] should be integer in directive [%s]" % (param, directive))

    def check_list_params(self, directive, params):
        """ Specified params should be `list` type if in directive
        @param directive: the directive to check
        @param params: the params that should be `list` type.
        """
        for param in params:
            if param not in directive:
                continue
            if not isinstance(directive[param], list):
                self.err_occur(
                    "parameter [%s] should be list in directive [%s]" % (param, directive))

    def check_required_params(self, directive, params):
        """ Specified params should be in directive
        @param directive: the directive to check
        @param params: the params that should be in directive.
        """
        for param in params:
            if param not in directive:
                self.err_occur(
                    "[%s] should be specified in directive [%s]" % (param, directive))

    def check_datetime_params(self, directive, params):
        """ Specified params should be `date` type if in directive
        @param directive: the directive to check
        @param params: the params that should be `date` type.
        """
        for param in params:
            if param not in directive:
                continue
            if not parse_ts(directive[param]):
                self.err_occur(
                    "[%s] should be 'YYYY-MM-DDThh:mm:ssZ' in directive [%s]" % (param, directive))

    def check_params(self, directive, required_params=None,
                     integer_params=None, list_params=None, datetime_params=None):
        """ Check parameters in directive
        @param directive: the directive to check, should be `dict` type.
        @param required_params: a list of parameter that should be in directive.
        @param integer_params: a list of parameter that should be `integer` type
                               if it exists in directive.
        @param list_params: a list of parameter that should be `list` type
                            if it exists in directive.
        @param datetime_params: a list of parameter that should be `date` type
                                if it exists in directive.
        """
        if not isinstance(directive, dict):
            self.err_occur('[%s] should be dict type' % directive)
            return False

        if required_params:
            self.check_required_params(directive, required_params)
        if integer_params:
            self.check_integer_params(directive, integer_params)
        if list_params:
            self.check_list_params(directive, list_params)
        if datetime_params:
            self.check_datetime_params(directive, datetime_params)
        return True

    def check_sg_rules(self, rules):
        return all(self.check_params(rule,
                                     required_params=['priority', 'protocol'],
                                     integer_params=['priority', 'direction'],
                                     list_params=[]
                                     ) for rule in rules)

    def check_router_statics(self, statics):
        def check_router_static(static):
            required_params = ['static_type']
            integer_params = []
            static_type = static.get('static_type')
            if static_type == RouterStaticFactory.TYPE_PORT_FORWARDING:
                # src port, dst ip, dst port
                required_params.extend(['val1', 'val2', 'val3'])
                integer_params = []
            elif static_type == RouterStaticFactory.TYPE_VPN:
                # vpn type
                required_params.extend(['val1'])
            elif static_type == RouterStaticFactory.TYPE_TUNNEL:
                required_params.extend(['vxnet_id', 'val1'])
            elif static_type == RouterStaticFactory.TYPE_FILTERING:
                integer_params = []
            else:
                integer_params = []

            return self.check_params(static, required_params, integer_params)

        return all(check_router_static(static) for static in statics)

    def check_lb_listener_port(self, port):
        if port in [25, 80, 443] or 1024 <= port <= 65535:
            return
        self.err_occur(
            'illegal port[%s], valid ones are [25, 80, 443, 1024~65535]' % port)

    def check_lb_listener_healthy_check_method(self, method):
        # valid methods: "tcp", "http|/url", "http|/url|host"
        if method == 'tcp' or re.match('http\|\/[^|]*(\|.+)?', method):
            return
        self.err_occur('illegal healthy check method[%s]' % method)

    def check_lb_listener_healthy_check_option(self, options):
        # options format string: inter | timeout | fall | rise
        items = options.split('|')
        if len(items) != 4:
            self.err_occur('illegal healthy check options[%s]' % options)

        inter, timeout, fall, rise = [int(item) for item in items]
        if not 2 <= inter <= 60:
            self.err_occur(
                'illegal inter[%s], should be between 2 and 60' % inter)
        if not 5 <= timeout <= 300:
            self.err_occur(
                'illegal timeout[%s], should be between 5 and 300' % timeout)
        if not 2 <= fall <= 10:
            self.err_occur(
                'illegal fall[%s], should be between 2 and 10' % fall)
        if not 2 <= rise <= 10:
            self.err_occur(
                'illegal rise[%s], should be between 2 and 10' % rise)

    def check_lb_backend_port(self, port):
        if 1 <= port <= 65535:
            return
        self.err_occur(
            'illegal port[%s], should be between 1 and 65535' % port)

    def check_lb_backend_weight(self, weight):
        if 1 <= weight <= 100:
            return
        self.err_occur(
            'illegal weight[%s], should be between 1 and 100' % weight)

    def check_lb_listeners(self, listeners):
        required_params = ['listener_protocol',
                           'listener_port', 'backend_protocol']
        integer_params = ['forwardfor', 'listener_port']
        for listener in listeners:
            self.check_params(listener,
                              required_params=required_params,
                              integer_params=integer_params,
                              )
            self.check_lb_listener_port(listener['listener_port'])
            if 'healthy_check_method' in listener:
                self.check_lb_listener_healthy_check_method(
                    listener['healthy_check_method'])
            if 'healthy_check_option' in listener:
                self.check_lb_listener_healthy_check_option(
                    listener['healthy_check_option'])

    def check_lb_backends(self, backends):
        required_params = ['resource_id', 'port']
        integer_params = ['weight', 'port']
        for backend in backends:
            self.check_params(backend,
                              required_params=required_params,
                              integer_params=integer_params,
                              )
            self.check_lb_backend_port(backend['port'])
            if 'weight' in backend:
                self.check_lb_backend_weight(backend['weight'])
