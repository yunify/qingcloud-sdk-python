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

########## API Actions ##########

# images
ACTION_DESCRIBE_IMAGES = "DescribeImages"
ACTION_CAPTURE_INSTANCE = "CaptureInstance"
ACTION_DELETE_IMAGES = "DeleteImages"
ACTION_MODIFY_IMAGE_ATTRIBUTES = "ModifyImageAttributes"

# instances
ACTION_DESCRIBE_INSTANCES = "DescribeInstances"
ACTION_RUN_INSTANCES = "RunInstances"
ACTION_TERMINATE_INSTANCES = "TerminateInstances"
ACTION_START_INSTANCES = "StartInstances"
ACTION_RESTART_INSTANCES = "RestartInstances"
ACTION_STOP_INSTANCES = "StopInstances"
ACTION_RESIZE_INSTANCES = "ResizeInstances"
ACTION_RESET_INSTANCES = "ResetInstances"
ACTION_MODIFY_INSTANCE_ATTRIBUTES = "ModifyInstanceAttributes"

# user data
ACTION_UPLOAD_USERDATA_ATTACHMENT = "UploadUserDataAttachment"

# volumes
ACTION_DESCRIBE_VOLUMES = "DescribeVolumes"
ACTION_CREATE_VOLUMES = "CreateVolumes"
ACTION_DELETE_VOLUMES = "DeleteVolumes"
ACTION_ATTACH_VOLUMES = "AttachVolumes"
ACTION_DETACH_VOLUMES = "DetachVolumes"
ACTION_RESIZE_VOLUMES = "ResizeVolumes"
ACTION_MODIFY_VOLUME_ATTRIBUTES = "ModifyVolumeAttributes"

# key pair
ACTION_DESCRIBE_KEY_PAIRS = "DescribeKeyPairs"
ACTION_CREATE_KEY_PAIR = "CreateKeyPair"
ACTION_DELETE_KEY_PAIRS = "DeleteKeyPairs"
ACTION_ATTACH_KEY_PAIRS = "AttachKeyPairs"
ACTION_DETACH_KEY_PAIRS = "DetachKeyPairs"
ACTION_MODIFY_KEYPAIR_ATTRIBUTES = "ModifyKeyPairAttributes"

# security group
ACTION_DESCRIBE_SECURITY_GROUPS = "DescribeSecurityGroups"
ACTION_CREATE_SECURITY_GROUP = "CreateSecurityGroup"
ACTION_MODIFY_SECURITY_GROUP_ATTRIBUTES = "ModifySecurityGroupAttributes"
ACTION_APPLY_SECURITY_GROUP = "ApplySecurityGroup"
ACTION_DELETE_SECURITY_GROUPS = "DeleteSecurityGroups"
ACTION_DESCRIBE_SECURITY_GROUP_RULES = "DescribeSecurityGroupRules"
ACTION_ADD_SECURITY_GROUP_RULES = "AddSecurityGroupRules"
ACTION_DELETE_SECURITY_GROUP_RULES = "DeleteSecurityGroupRules"
ACTION_MODIFY_SECURITY_GROUP_RULE_ATTRIBUTES = "ModifySecurityGroupRuleAttributes"

# vxnets
ACTION_DESCRIBE_VXNETS = "DescribeVxnets"
ACTION_CREATE_VXNETS = "CreateVxnets"
ACTION_DELETE_VXNETS = "DeleteVxnets"
ACTION_JOIN_VXNET = "JoinVxnet"
ACTION_LEAVE_VXNET = "LeaveVxnet"
ACTION_MODIFY_VXNET_ATTRIBUTES = "ModifyVxnetAttributes"
ACTION_DESCRIBE_VXNET_INSTANCES = "DescribeVxnetInstances"

# router
ACTION_CREATE_ROUTERS = "CreateRouters"
ACTION_UPDATE_ROUTERS = "UpdateRouters"
ACTION_DELETE_ROUTERS = "DeleteRouters"
ACTION_JOIN_ROUTER = "JoinRouter"
ACTION_LEAVE_ROUTER = "LeaveRouter"
ACTION_POWEROFF_ROUTERS = "PowerOffRouters"
ACTION_POWERON_ROUTERS = "PowerOnRouters"
ACTION_DESCRIBE_ROUTERS = "DescribeRouters"
ACTION_DESCRIBE_ROUTER_VXNETS = "DescribeRouterVxnets"
ACTION_MODIFY_ROUTER_ATTRIBUTES = "ModifyRouterAttributes"
ACTION_DESCRIBE_ROUTER_STATICS = "DescribeRouterStatics"
ACTION_ADD_ROUTER_STATICS = "AddRouterStatics"
ACTION_DELETE_ROUTER_STATICS = "DeleteRouterStatics"

# eip
ACTION_ASSOCIATE_EIP = "AssociateEip"
ACTION_DISSOCIATE_EIPS = "DissociateEips"
ACTION_ALLOCATE_EIPS = "AllocateEips"
ACTION_RELEASE_EIPS = "ReleaseEips"
ACTION_DESCRIBE_EIPS = "DescribeEips"
ACTION_MODIFY_EIP_ATTRIBUTES = "ModifyEipAttributes"
ACTION_CHANGE_EIPS_BANDWIDTH = "ChangeEipsBandwidth"

# lb
ACTION_DESCRIBE_LOADBALANCERS = "DescribeLoadBalancers"
ACTION_CREATE_LOADBALANCER = "CreateLoadBalancer"
ACTION_DELETE_LOADBALANCERS = "DeleteLoadBalancers"
ACTION_ASSOCIATE_EIPS_TO_LOADBALANCER = "AssociateEipsToLoadBalancer"
ACTION_DISSOCIATE_EIPS_FROM_LOADBALANCER = "DissociateEipsFromLoadBalancer"
ACTION_UPDATE_LOADBALANCERS = "UpdateLoadBalancers"
ACTION_STOP_LOADBALANCERS = "StopLoadBalancers"
ACTION_START_LOADBALANCERS = "StartLoadBalancers"
ACTION_MODIFY_LOADBALANCER_ATTRIBUTES = "ModifyLoadBalancerAttributes"

ACTION_DESCRIBE_LOADBALANCER_LISTENERS = "DescribeLoadBalancerListeners"
ACTION_ADD_LOADBALANCER_LISTENERS = "AddLoadBalancerListeners"
ACTION_DELETE_LOADBALANCER_LISTENERS = "DeleteLoadBalancerListeners"
ACTION_MODIFY_LOADBALANCER_LISTENER_ATTRIBUTES = "ModifyLoadBalancerListenerAttributes"
ACTION_ADD_LOADBALANCER_BACKENDS = "AddLoadBalancerBackends"
ACTION_DELETE_LOADBALANCER_BACKENDS = "DeleteLoadBalancerBackends"
ACTION_MODIFY_LOADBALANCER_BACKEND_ATTRIBUTES = "ModifyLoadBalancerBackendAttributes"
ACTION_DESCRIBE_LOADBALANCER_BACKENDS = "DescribeLoadBalancerBackends"

# monitor
ACTION_GET_MONITOR = "GetMonitor"
ACTION_GET_LOADBALANCER_MONITOR = "GetLoadBalancerMonitor"

# snapshot
ACTION_CREATE_SNAPSHOTS = "CreateSnapshots"
ACTION_DELETE_SNAPSHOTS = "DeleteSnapshots"
ACTION_APPLY_SNAPSHOTS = "ApplySnapshots"
ACTION_DESCRIBE_SNAPSHOTS = "DescribeSnapshots"
ACTION_MODIFY_SNAPSHOT_ATTRIBUTES = "ModifySnapshotAttributes"
ACTION_CAPTURE_INSTANCE_FROM_SNAPSHOT = "CaptureInstanceFromSnapshot"
ACTION_CREATE_VOLUME_FROM_SNAPSHOT = "CreateVolumeFromSnapshot"

########## Constants for resource ##########

# sg
DIRECTION_EGRESS = 1
DIRECTION_INGRESS = 0

# vxnet
VXNET_TYPE_MANAGED = 1
VXNET_TYPE_UNMANAGED = 0

# lb
BALANCE_ROUNDROBIN = "roundrobin"
BALANCE_LEASTCONN = "leastconn"
HEADER_X_FORWARD_FOR = 1
HEADER_QC_LBID = 2
HEADER_QC_LBIP = 4
