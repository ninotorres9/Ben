# -*- coding: utf-8 -*-

import unittest
import requests
import re
from app.Spider import Spider
from app.IpSpider import IpSpider
from app import createApp, db


class TestTools:
    @staticmethod
    def validateIpAddress(ip):
        import re
        protocolPattern = "http(.)?://"
        segmentPattern = "[0-9][0-9]?[0-9]?"
        ipAddressPattern = ".".join([segmentPattern] * 4)
        portPattern = ":[0-9][0-9]?[0-9]?[0-9]?[0-9]?"

        result = re.match(protocolPattern + ipAddressPattern + portPattern, ip)

        try:
            # 检查是否完全匹配
            return (len(result.group()) == len(ip))
        except AttributeError:
            return False


class TestSpider(unittest.TestCase):
    def setUp(self):
        self.app = createApp()
        self.appContext = self.app.app_context()
        self.appContext.push()
        db.create_all()

        ipSpider = IpSpider()
        ipSpider.saveToSql()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.appContext.pop()

    def testvalidateIpAddress(self):
        """
            检测getIp返回ip地址格式
        """
        # 示范
        self.assertTrue(
            TestTools.validateIpAddress("https://192.168.1.1:8080"))
        self.assertFalse(
            TestTools.validateIpAddress("https://192.168.1.1:810603"))

        # 测试
        spider = Spider()
        self.assertTrue(TestTools.validateIpAddress(spider.getIP()))
        self.assertTrue(TestTools.validateIpAddress(spider.getIP()))
        self.assertTrue(TestTools.validateIpAddress(spider.getIP()))

    def testGetHtml(self):
        """
            检测抓到的html文本
        """
        spider = Spider()
        html = spider.getHtml("https://www.basketball-reference.com")
        self.assertTrue("Basketball Stats and History" in html)
        self.assertTrue("Full Site Menu" in html)
