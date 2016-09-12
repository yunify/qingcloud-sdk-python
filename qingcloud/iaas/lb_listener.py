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

from qingcloud.iaas.constants import HEADER_X_FORWARD_FOR, HEADER_QC_LBID, HEADER_QC_LBIP

HEADERS = {
    'X-FORWARD-FOR': HEADER_X_FORWARD_FOR,
    'QC-LBID': HEADER_QC_LBID,
    'QC-LBIP': HEADER_QC_LBIP,
}


class LoadBalancerListener(object):
    """ LoadBalancerListener is used to define listener in load balancer.
    """
    loadbalancer_listener_id = None
    loadbalancer_listener_name = None
    listener_port = None
    listener_protocol = None
    backend_protocol = None
    balance_mode = None
    forwardfor = None
    session_sticky = None
    healthy_check_method = None
    healthy_check_option = None

    def __init__(self, listener_port, listener_protocol, backend_protocol,
                 balance_mode='roundrobin', forwardfor=None, headers=None, session_sticky='',
                 healthy_check_method='tcp', healthy_check_option='10|5|2|5',
                 loadbalancer_listener_name=None, loadbalancer_listener_id=None,
                 **kw):
        self.listener_port = listener_port
        self.listener_protocol = listener_protocol
        self.backend_protocol = backend_protocol
        self.balance_mode = balance_mode
        self.forwardfor = forwardfor or LoadBalancerListener.get_forwardfor(
            headers)
        self.session_sticky = session_sticky
        self.healthy_check_method = healthy_check_method
        self.healthy_check_option = healthy_check_option
        self.loadbalancer_listener_name = loadbalancer_listener_name
        if loadbalancer_listener_id:
            self.loadbalancer_listener_id = loadbalancer_listener_id

    def __repr__(self):
        return '<%s>%s' % (self.__class__.__name__, self.to_json())

    @staticmethod
    def get_forwardfor(headers):
        """ Get forwardfor from header array.
        """
        if not headers:
            return 0

        forwardfor = 0
        for head in headers:
            if head in HEADERS:
                forwardfor |= HEADERS[head]
        return forwardfor

    @classmethod
    def create_from_string(cls, string):
        """ Create load balancer listener from json formatted string.
        """
        data = json.loads(string)
        if isinstance(data, dict):
            return cls(**data)
        if isinstance(data, list):
            return [cls(**item) for item in data]

    def to_json(self):
        return {
            'loadbalancer_listener_name': self.loadbalancer_listener_name,
            'listener_port': self.listener_port,
            'listener_protocol': self.listener_protocol,
            'backend_protocol': self.backend_protocol,
            'balance_mode': self.balance_mode,
            'forwardfor': self.forwardfor,
            'session_sticky': self.session_sticky,
            'healthy_check_method': self.healthy_check_method,
            'healthy_check_option': self.healthy_check_option,
        }
