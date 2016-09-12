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


import json as jsmod


def json_dump(obj, indent=None):
    """ Dump an object to json string, only basic types are supported.
        @return json string or `None` if failed

        >>> json_dump({'int': 1, 'none': None, 'str': 'string'})
        '{"int":1,"none":null,"str":"string"}'
    """
    try:
        jstr = jsmod.dumps(obj, separators=(',', ':'),
                           indent=indent, sort_keys=True)
    except:
        jstr = None
    return jstr


def json_load(json):
    """ Load from json string and create a new python object
        @return object or `None` if failed

        >>> json_load('{"int":1,"none":null,"str":"string"}')
        {u'int': 1, u'none': None, u'str': u'string'}
    """
    try:
        obj = jsmod.loads(json)
    except:
        obj = None
    return obj

__all__ = [json_dump, json_load]
