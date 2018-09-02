# -*- coding: utf-8 -*-

import fire
import unittest
import threading
from app import db, createApp
from app.IpSpider import IpSpider
from app.PsnineSpider import PsnineSpider

app = createApp("default")
appContext = app.app_context()
appContext.push()

spider = PsnineSpider()


def test():
    """
        单元测试
    """
    tests = unittest.TestLoader().discover("tests")
    unittest.TextTestRunner(verbosity=2).run(tests)


def singleTest():
    """
        单项单元测试
    """
    from tests.TestPsnineSpider import TestPsnineSpider
    tests = unittest.TestLoader().loadTestsFromTestCase(TestPsnineSpider)
    unittest.TextTestRunner(verbosity=2).run(tests)


def updateIp():
    """
        更新ip池并进行测试
    """
    ipSpider = IpSpider()
    ipSpider.saveToSql()


def updateGamelog():
    """
        更新gamelog
    """
    global spider
    teamUrls = spider.getTeamUrls(
        "https://www.basketball-reference.com/teams/")

    threadList = [TeamThread(teamUrl) for teamUrl in teamUrls]

    for thread in threadList:
        thread.start()

    for thread in threadList:
        thread.join()

    with open("GAMELOG_LIST.txt", "w", encoding="utf-8") as outFile:
        for gamelog in spider.gamelogs:
            outFile.write(gamelog.toString())
            outFile.write("\n")

    with open("SQL_LIST.txt", "w", encoding="utf-8") as outFile:
        for gamelog in spider.gamelogs:
            outFile.write(gamelog.toSql())
            outFile.write("\n")


class TeamThread(threading.Thread):
    def __init__(self, url):
        threading.Thread.__init__(self)
        self.url = url

    def run(self):
        print("开启线程：{url}".format(url=self.url))
        global spider
        appContext = app.app_context()
        appContext.push()
        spider.saveToList(self.url)


def main():
    fire.Fire()


if __name__ == '__main__':
    main()