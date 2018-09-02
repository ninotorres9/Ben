# -*- coding: utf-8 -*-

import re
from app import db
from app.Models import IP


class ProxyPool(object):
    """
        从数据库中读取ip list
    """

    def __init__(self):
        self.ipList = iter(self.loadIpList())

    def loadIpList(self):
        return IP.query.all()

    def getIp(self):
        try:
            return next(self.ipList).address
        except StopIteration:
            self.ipList = iter(self.loadIpList())
            return next(self.ipList).address
