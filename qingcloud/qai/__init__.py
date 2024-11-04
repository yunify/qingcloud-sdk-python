"""
Connect to QAI.
"""
from qingcloud.qai.connection import QAIConnection


def connect(access_key_id, secret_access_key, zone):
    return QAIConnection(access_key_id, secret_access_key, zone)