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
from past.builtins import basestring


class LoadBalancerBackend(object):
    """ LoadBalancerBackend is used to define backend in load balancer listener.
    """
    resource_id = None
    loadbalancer_backend_name = None
    port = None
    weight = None

    def __init__(self, resource_id, port, weight=1,
                 loadbalancer_backend_id=None, loadbalancer_backend_name=None,
                 **kw):
        self.resource_id = resource_id
        self.port = port
        self.weight = weight
        self.loadbalancer_backend_name = loadbalancer_backend_name
        if loadbalancer_backend_id:
            self.loadbalancer_backend_id = loadbalancer_backend_id

    def __repr__(self):
        return '<%s>%s' % (self.__class__.__name__, self.to_json())

    @classmethod
    def create_from_string(cls, string):
        """ Create load balancer backend from json formatted string.
        """
        if not isinstance(string, basestring):
            return string
        data = json.loads(string)
        if isinstance(data, dict):
            return cls(**data)
        if isinstance(data, list):
            return [cls(**item) for item in data]

    def to_json(self):
        return {
            'resource_id': self.resource_id,
            'loadbalancer_backend_name': self.loadbalancer_backend_name,
            'port': self.port,
            'weight': self.weight,
        }
