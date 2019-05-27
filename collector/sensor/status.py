#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Full credit to https://github.com/IDCFChannel/bme280-meshblu-py (or who ever
originally wrote bme280_sample.py)
"""

import os
from datetime import datetime

def status():
    statvfs = os.statvfs('/')

    reply = {
        "size": statvfs.f_frsize * statvfs.f_blocks,
        "free": statvfs.f_frsize * statvfs.f_bavail,
        "timestamp": datetime.now().isoformat()
    }

    return reply
