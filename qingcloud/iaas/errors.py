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
Exception classes
"""


class InvalidParameterError(Exception):
    """ Error when invalid parameter found in request
    """
    pass


class APIError(Exception):
    """ Error in response from api
    """

    def __init__(self, err_code, err_msg):
        super(APIError, self).__init__(self)
        self.err_code = err_code
        self.err_msg = err_msg

    def __repr__(self):
        return '%s: %s-%s' % (self.__class__.__name__,
                              self.err_code, self.err_msg)

    def __str__(self):
        return '%s: %s-%s' % (self.__class__.__name__,
                              self.err_code, self.err_msg)


class InvalidRouterStatic(Exception):
    pass


class InvalidSecurityGroupRule(Exception):
    pass


class InvalidAction(Exception):
    pass
