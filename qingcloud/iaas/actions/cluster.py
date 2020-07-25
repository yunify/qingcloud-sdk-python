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
                       **ignore):
        """ Resize cluster
        @param cluster: the ID of the cluster you want to resize.
        @param cpu: cpu core number.
        @param memory: memory size in MB.
        @param storage_size: The new larger size of the storage_size, unit is GB.
        """
        action = const.ACTION_RESIZE_CLUSTER
        valid_keys = ['cluster', 'node_role', 'cpu', 'memory', 'storage_size']
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

    def associate_eip_to_cluster_node(self, eip, cluster_node):
        """
        Associate eip to the cluster node
        @param eip: eip ID
        @param cluster_node: cluster node ID
        """
        action = const.ACTION_ASSOCIATE_EIP_TO_CLUSTER_NODE
        valid_keys = ["eip", "cluster_node"]
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(
                body, required_params=["eip", "cluster_node"]):
            return None

        return self.conn.send_request(action, body)

    def cease_clusters(self, clusters):
        """
        Cease one or more clusters
        @param clusters: the array of clusters IDs.
        """
        action = const.ACTION_CEASE_CLUSTERS
        valid_keys = ["clusters"]
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(
                body, required_params=["clusters"], list_params=["clusters"]):
            return None

        return self.conn.send_request(action, body)

    def change_cluster_vxnet(self, cluster, vxnet, roles=None, private_ips=None):
        """
        Cluster leaves current vxnet and join another one
        @param cluster: cluster ID.
        @param vxnet: vxnet ID.
        @param roles: the array of roles names.
        @param private_ips: the array of private_ips info of cluster nodes
            e.g. [{"node_id": "cln-nqop00oj", "private_ip": "192.168.1.4"}]
        """
        action = const.ACTION_CHANGE_CLUSTER_VXNET
        valid_keys = ["cluster", "vxnet", "roles", "private_ips"]
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(
                body, required_params=["cluster", "vxnet"],
                list_params=["roles", "private_ips"]):
            return None

        return self.conn.send_request(action, body)

    def deploy_app_version(self, version_id, conf, debug=0):
        """
        Deploy app version to create a cluster
        @param version_id: app version ID.
        @param conf: app configuration info
        @param debug: debug cluster(debug=1) or not debug cluster(debug=0)
        """
        action = const.ACTION_DEPLOY_APP_VERSION
        valid_keys = ["version_id", "conf", "debug"]
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(
                body, required_params=["version_id", "conf"],
                integer_params=["debug"]):
            return None

        return self.conn.send_request(action, body)

    def describe_app_version_attachments(self, attachment_ids, version_id, content_keys=None):
        """
        Get configuration content of the app version
        @param content_keys: the array of conf file names(default "config.json")
        @param attachment_ids: the array of app configuration file IDs.
        @param version_id: the app version ID
        """
        action = const.ACTION_DESCRIBE_APP_VERSION_ATTACHMENTS
        valid_keys = ["content_keys", "attachment_ids", "version_id"]
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(
                body, required_params=["attachment_ids", "version_id"],
                list_params=["content_keys", "attachment_ids"]):
            return None

        return self.conn.send_request(action, body)


    def describe_app_versions(self, app_ids=None, version_ids=None, name=None,
                              sort_key=None, owner=None, verbose=None,
                              offset=None, limit=None, reverse=None):
        """
        Get information of one or more app versions
        @param app_ids: the array of app IDs.
        @param version_ids:  the array of app version IDs.
        @param name: name of the app
        @param sort_key: the sort key.
        @param owner: the user ID of the owner
        @param offset: the starting offset of the returning results.
        @param limit: specify the number of the returning results.
        @param verbose: Whether to return redundant message.
                        if it is 1, return the details of the instance related other resources.
        @param reverse: 0 for Ascending order, 1 for Descending order.
        """
        action = const.ACTION_DESCRIBE_APP_VERSIONS
        valid_keys = ["app_ids", "version_ids", "name", "sort_key", "owner",
                      "verbose", "offset", "limit", "reverse"]
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(
                body, required_params=[],
                list_params=["app_ids", "version_ids"],
                integer_params=["verbose", "offset", "limit", "reverse"]):
            return None

        return self.conn.send_request(action, body)

    def describe_cluster_display_tabs(self, cluster, display_tabs):
        """
        Get information of cluster display tabs
        @param cluster: the cluster ID
        @param display_tabs: the name of display_tabs
        """
        action = const.ACTION_DESCRIBE_CLUSTER_DISPLAY_TABS
        valid_keys = ["cluster", "display_tabs"]
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(
                body, required_params=["cluster", "display_tabs"]):
            return None

        return self.conn.send_request(action, body)

    def describe_cluster_environment(self, cluster_id, role=None):
        """
        Get environment configuration
        @param cluster: the cluster ID.
        @param role: the role name
        """
        action = const.ACTION_DESCRIBE_CLUSTER_ENV
        valid_keys = ["cluster_id", "role"]
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body, required_params=["cluster_id"]):
            return None

        return self.conn.send_request(action, body)

    def describe_cluster_jobs(self, app, jobs=None, status=None, verbose=0, offset=None, limit=None):
        """
        Get job logs of the operation of one or more clusters
        @param app: the app ID.
        @param jobs: the array of job IDs.
        @param status: the status of logs.
        @param verbose: Whether to return redundant message.
                        if it is 1, return the details of the instance related other resources.
                        only 0 is supported now.
        """
        action = const.ACTION_DESCRIBE_CLUSTER_JOBS
        valid_keys = ["app", "jobs", "status", "verbose", "offset", "limit"]
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(
                body, required_params=["app"], list_params=["jobs", "status"],
                integer_params=["verbose", "offset", "limit"]):
            return None

        return self.conn.send_request(action, body)

    def describe_cluster_nodes(self, cluster, cluster_nodes=None, role=None,
                               verbose=None, offset=None, limit=None, reverse=None):
        """
        Get information of the cluster node
        :param cluster: the cluster ID.
        :param cluster_nodes: the cluster node ID.
        :param role: the role name
        """
        action = const.ACTION_DESCRIBE_CLUSTER_NODES
        valid_keys = ["cluster", "cluster_nodes", "role", "verbose", "offset", "limit", "reverse"]
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(
                body, required_params=["cluster"],
                list_params=["cluster_nodes"],
                integer_params=["verbose", "offset", "limit", "reverse"]):
            return None

        return self.conn.send_request(action, body)

    def dissociate_eip_from_cluster_node(self, eips):
        """
        Dissociate eip from cluster node
        @param eips: the array of eip IDs.
        """
        action = const.ACTION_DISSOCIATE_EIP_FROM_CLUSTER_NODE
        valid_keys = ["eips"]
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(
                body, required_params=["eips"], list_params=["eips"]):
            return None

        return self.conn.send_request(action, body)

    def get_cluster_monitor(self, resource, step, start_time, end_time, meters,
                            app_id=None, version_id=None, role=None):
        """
        Get cluster monitor
        @param app_id: the app ID of the cluster.
        @param version_id: the app version ID.
        @param resource: the cluster node ID.
        @param role: the role name.
        @param step: the gap time of the collected monitor data
        @param start_time: start timestamp of the monitor
        @param end_time: end timestamp of the monitor
        @param meters: data type of the monitor data
        """
        action = const.ACTION_GET_CLUSTER_MONITOR
        valid_keys = ["resource", "step", "start_time", "end_time",
                      "meters", "app_id", "version_id", "role"]
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(
                body, required_params=["resource", "step", "start_time", "end_time", "meters"],
                list_params=["meters"], datetime_params=["start_time", "end_time"]):
            return None

        return self.conn.send_request(action, body)

    def restart_cluster_service(self, cluster, role=None):
        """
        Restart cluster service
        @param cluster: the cluster ID.
        @param role: the role name.
        """
        action = const.ACTION_RESTART_CLUSTER_SERVICE
        valid_keys = ["cluster", "role"]
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body, required_params=["cluster"]):
            return None

        return self.conn.send_request(action, body)


    def update_cluster_environment(self, cluster, env, role=None):
        """
        Update cluster env configuration
        @param cluster: the cluster ID.
        @param env: new JSON formatted configuration.
        @param role: the role name.
        """
        action = const.ACTION_UPDATE_CLUSTER_ENV
        valid_keys = ["cluster", "env", "role"]
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body, required_params=["cluster", "env"]):
            return None

        return self.conn.send_request(action, body)

    def reset_cluster_upgrade_status(self, clusters):
        """
        Set cluster upgrade status to STATUS_FAILED
        @param clusters: the array of cluster IDs
        """
        action = const.ACTION_RESET_CLUSTER_UPGRADE_STATUS
        valid_keys = ["clusters"]
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body, required_params=["clusters"]):
            return None

        return self.conn.send_request(action, body)

    def create_auto_cluster_snapshots(self, cluster):
        """
        Create auto cluster snapshots
        @param cluster: the cluster ID.
        """
        action = const.ACTION_CREATE_AUTO_CLUSTER_SNAPSHOTS
        valid_keys = ["cluster"]
        body = filter_out_none(locals(), valid_keys)
        if not self.conn.req_checker.check_params(body, required_params=["cluster"]):
            return None

        return self.conn.send_request(action, body)

