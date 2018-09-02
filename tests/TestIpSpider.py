# -*- coding: utf-8 -*-

import unittest
from app import db, createApp
from app.IpSpider import IpSpider
from app.Models import IP
from tests.TestSpider import TestTools


class TestIpSpider(unittest.TestCase):
    def setUp(self):
        self.app = createApp(configName="testing")
        self.appContext = self.app.app_context()
        self.appContext.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.appContext.pop()

    def testGetHtmlText(self):
        ipSpider = IpSpider()
        self.assertTrue("高效高匿名代理IP提取地址" in ipSpider.text)

    def testGetChar(self):
        ipSpider = IpSpider()
        self.assertEqual(ipSpider.getChar(), "<")
        self.assertEqual(ipSpider.getChar(), "a")

    def testPeekChar(self):
        ipSpider = IpSpider()
        self.assertEqual(ipSpider.peekChar(), "<")
        ipSpider.getChar()
        self.assertEqual(ipSpider.peekChar(), "a")

    def testEndOfText(self):
        ipSpider = IpSpider()

        with self.assertRaises(IndexError):
            for i in range(100000):
                ipSpider.getChar()

        with self.assertRaises(IndexError):
            ipSpider.peekChar()

    def testGenerateIpList(self):
        ipSpider = IpSpider()
        ipList = ipSpider.generateIpList()
        for ip in ipList:
            self.assertTrue(TestTools.validateIpAddress(ip))

    def testSaveToSql(self):
        ipSpider = IpSpider()
        ipSpider.saveToSql()
        self.assertEqual(len(IP.query.all()), 2750)

        for ip in IP.query.all():
            self.assertTrue(TestTools.validateIpAddress(ip.address))
