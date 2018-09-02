# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from urllib import request
from app.ProxyPool import ProxyPool

# 问题出在相互调用


class Spider():
    baseUrl = "https://www.basketball-reference.com"

    def __init__(self):
        self.headers = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
        }
        self.proxyPool = ProxyPool()
        self.currentIP = self.getIP()

    def getIP(self):
        """
            从ip池中提取ip
        """
        return self.proxyPool.getIp()

    def getSoup(self, url):
        return BeautifulSoup(self.getHtml(url), "lxml")

    def getHtml(self, url):
        """
            获取html文本
        """
        loop = True
        # ip被封时更换下一组继续尝试连接
        while (loop):
            try:
                ip = self.currentIP
                proxyHandler = request.ProxyHandler({"http": ip})
                opener = request.build_opener(proxyHandler)
                page = opener.open(url, timeout=5)
            except Exception as err:
                self.currentIP = self.getIP()
                # print("更换IP...")
                print(err)
            else:
                loop = False

        return page.read().decode("utf-8")
