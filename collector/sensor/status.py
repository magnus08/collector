import os
from datetime import datetime


def status():
    statvfs = os.statvfs('/')

    reply = {
        "size": statvfs.f_frsize * statvfs.f_blocks,
        "free": statvfs.f_frsize * statvfs.f_bavail,
        "timestamp": datetime.now()
    }

    return reply
