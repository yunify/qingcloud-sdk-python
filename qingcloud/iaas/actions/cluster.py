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

from qingcloud.iaas import constants as const
from qingcloud.misc.utils import filter_out_none


class ClusterAction(object):

    def __init__(self, conn):
        self.conn = conn

    def start_clusters(self, clusters,
                       **ignore):
        """ Start one or more clusters.
        @param clusters: the array of clusters IDs.
        """
        action = const.ACTION_START_CLUSTERS
        body = {'clusters': clusters}
        if not self.conn.req_checker.check_params(body,
                                                  required_params=['clusters'],
                                                  integer_params=[],
                                                  list_params=['clusters']
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def stop_clusters(self, clusters,
                      **ignore):
        """ Stop one or more clusters.
        @param clusters: the array of clusters IDs.
        """
        action = const.ACTION_STOP_CLUSTERS
        body = {'clusters': clusters}
        if not self.conn.req_checker.check_params(body,
                                                  required_params=['clusters'],
                                                  integer_params=[],
                                                  list_params=['clusters']
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def resize_cluster(self, cluster,
                       node_role=None,
                       cpu=None,
                       memory=None,
                       storage_size=None,
                       instance_class=None,
                       **ignore):
        """ Resize cluster
        @param cluster: the ID of the cluster you want to resize.
        @param cpu: cpu core number.
        @param memory: memory size in MB.
        @param storage_size: The new larger size of the storage_size, unit is GB.
        @param instance_class: The new class of instance
        """
        action = const.ACTION_RESIZE_CLUSTER
        valid_keys = ['cluster', 'node_role', 'cpu', 'memory', 'storage_size', 'instance_class']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=['cluster'],
                                                  integer_params=['cpu', 'memory']
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def describe_clusters(self, clusters=None,
                          role=None,
                          status=None,
                          verbose=1,
                          search_word=None,
                          owner=None,
                          offset=None,
                          limit=None,
                          tags=None,
                          **ignore):
        """ Describe clusters filtered by condition.
        @param clusters: the array of cluster IDs.
        @param status: pending, active, stopped, deleted, suspended, ceased
        @param verbose: the number to specify the verbose level, larger the number, the more detailed information will be returned.
        @param search_word: search word column.
        @param offset: the starting offset of the returning results.
        @param limit: specify the number of the returning results.
        @param tags : the array of IDs of tags.
        """
        action = const.ACTION_DESCRIBE_CLUSTERS
        valid_keys = ['clusters', 'status', 'verbose', 'search_word',
                      'owner', 'offset', 'limit', 'tags', 'role']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=[],
                                                  integer_params=[
                                                      'offset', 'limit'],
                                                  list_params=[
                                                      'clusters', 'status', 'tags']
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def describe_cluster_jobs(self, cluster=None,
                             limit=None,
                             offset=None,
                             reverse=True,
                             sort_key=None,
                             status=None,
                             verbose=1,
                             zone=None,
                             **ignore):
        """ Describe cluster job filtered by condition.
        @param cluster: the array of cluster IDs.
        @param limit: specify the number of the returning results.
        @param sort_key: sort the result by sort key
        """
        action = const.ACTION_DESCRIBE_CLUSTER_JOBS
        valid_keys = ['cluster', 'limit', 'offset', 'reverse',
                      'sort_key', 'status', 'verbose', 'zone']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=['cluster'],
                                                  integer_params=[
                                                      'limit', 'offset','reverse','verbose']
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def add_cluster_nodes(self, cluster, node_count, owner=None, node_name=None, node_role=None, resource_conf=None, **params):
        """ Add one or more cluster nodes
        """
        action = const.ACTION_ADD_CLUSTER_NODES
        valid_keys = ['cluster', 'node_count', 'owner', 'node_name', 'node_role', 'resource_conf']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=[
                                                      'cluster', 'node_count'],
                                                  integer_params=['node_count']
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def delete_cluster_nodes(self, cluster, nodes, owner=None):
        """ Delete one or more cluster nodes
        """
        action = const.ACTION_DELETE_CLUSTER_NODES
        valid_keys = ['cluster', 'nodes', 'owner']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=[
                                                      'cluster', 'nodes'],
                                                  list_params=['nodes']):
            return None

        return self.conn.send_request(action, body)

    def delete_clusters(self, clusters, direct_cease=0):
        """ Delete one or more clusters.
        @param clusters: the array of clusters IDs.
        @param direct_cease: whether to keep deleted resource in recycle bin (direct_cease=0) or not (direct_cease=1).
        """
        action = const.ACTION_DELETE_CLUSTERS
        valid_keys = ['clusters', 'direct_cease']
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body,
                                                  required_params=['clusters'],
                                                  integer_params=['direct_cease'],
                                                  list_params=['clusters']
                                                  ):
            return None

        return self.conn.send_request(action, body)

    def deploy_app_version(self, version_id, conf, debug=None,
                           charge_mode=None, duration=None, hypervisor=None, **ignore):
        """ deploy a cluster using a application version
        Args:
            version_id: application version
            conf: the configuration of cluster
            debug: whether the cluster is for dev/test
            charge_mode:
            duration:
            hypervisor:
            **ignore:

        Returns:

        """
        action = const.ACTION_DEPLOY_APP_VERSION
        body = filter_out_none(locals(), ['version_id', 'conf', 'debug', 'charge_mode', 'duration', 'hypervisor'])
        if not self.conn.req_checker.check_params(body, required_params=['version_id', 'conf'], integer_params=['debug']):
            return None

        return self.conn.send_request(action, body)
