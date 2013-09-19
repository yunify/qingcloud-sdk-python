"""
interface to the IaaS service from QingCloud.
"""

from qingcloud.iaas.connection import APIConnection


def get_zones():
    """ Get all valid zones in qingcloud.
    """
    return ['pek1',]

def connect_to_zone(zone, access_key_id, secret_access_key):
    """ Connect to one of zones in qingcloud by access key.
    """
    if zone not in get_zones():
        raise ValueError('invalid zone: %s' % zone)
    return APIConnection(access_key_id, secret_access_key, zone)
