# -*- coding: utf-8 -*-

import unittest
from app import db, createApp
from app.ProxyPool import ProxyPool
from app.IpSpider import IpSpider
from tests.TestSpider import TestTools


class TestProxyPool(unittest.TestCase):
    def setUp(self):
        self.app = createApp(configName="testing")
        self.appContext = self.app.app_context()
        self.appContext.push()
        db.create_all()

        ipSpider = IpSpider()
        ipSpider.saveToSql()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.appContext.pop()

    def testGetIpList(self):
        proxyPool = ProxyPool()
        iplist = proxyPool.loadIpList()
        for ip in iplist:
            self.assertTrue(TestTools.validateIpAddress(ip.address))

    def testGetIp(self):
        proxyPool = ProxyPool()
        ip_1 = proxyPool.getIp()
        ip_2 = proxyPool.getIp()
        self.assertTrue(TestTools.validateIpAddress(ip_1))
        self.assertTrue(TestTools.validateIpAddress(ip_2))
        self.assertNotEqual(ip_1, ip_2)

    def testOutOfRange(self):
        proxyPool = ProxyPool()

        for each in range(5000):
            proxyPool.getIp()