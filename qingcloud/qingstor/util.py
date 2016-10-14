# =========================================================================
# Copyright 2016 Yunify, Inc.
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

def load_data(response_data):
    """ Wrapper to load json data, to be compatible with Python3.
    Returns: JSON data

    Keyword arguments:
    response_data - Data from response read, may be bytes or str
    """
    if type(response_data) == bytes:
        return json.loads(response_data.decode("utf-8"))
    else:
        return json.loads(response_data)