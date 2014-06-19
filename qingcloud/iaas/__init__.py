"""
interface to the IaaS service from QingCloud.
"""

from qingcloud.iaas.connection import APIConnection


def connect_to_zone(zone, access_key_id, secret_access_key):
    """ Connect to one of zones in qingcloud by access key.
    """
    zone = zone.lower().strip()
    return APIConnection(access_key_id, secret_access_key, zone)
