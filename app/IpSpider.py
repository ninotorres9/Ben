# -*- coding: utf-8 -*-

from urllib import request
from app.Models import IP
from app import db


class IpSpider(object):
    """
        获取ip列表，存入数据库
    """

    def __init__(self):
        self.text_ = ""
        self.index = 0
        self.buffer = ""
        self.loop = True
        self.saveToText()
        self.ipList = self.generateIpList()

    def saveToText(self):
        url = "http://www.89ip.cn/tqdl.html?api=1&num=9999&port=&address=&isp="
        html = request.urlopen(url)
        self.text = html.read().decode("utf-8")

    def getChar(self):
        char = self.text[self.index]
        self.index += 1
        return char

    def peekChar(self):
        return self.text[self.index]

    def saveToSql(self):
        for ip in self.ipList:
            db.session.add(IP(address=ip))
        try:
            db.session.commit()
        except:
            db.session.rollback()

    def eat(self, word):
        if (self.peekChar() == word):
            self.buffer += self.getChar()
            return True
        else:
            return False

    def handleNumberState(self):
        while (self.peekChar().isdigit()):
            self.buffer += self.getChar()

    def generateIpList(self):
        self.loop = True
        while (self.loop is True):
            try:
                currentChar = self.peekChar()
            except:
                self.loop = False
            else:
                if currentChar.isdigit():
                    self.buffer = ""
                    self.handleNumberState()  # 192
                    if not self.eat("."):  # .
                        continue
                    self.handleNumberState()  # 168
                    if not self.eat("."):  # .
                        continue
                    self.handleNumberState()  # 1
                    if not self.eat("."):  # .
                        continue
                    self.handleNumberState()  # 1
                    if not self.eat(":"):  # :
                        continue
                    self.handleNumberState()  # 8080

                    yield "http://{ip}".format(ip=self.buffer)
                else:
                    self.getChar()