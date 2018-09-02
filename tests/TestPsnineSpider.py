# -*- coding: utf-8 -*-

import unittest
from app import db, createApp
from app.PsnineSpider import PsnineSpider
from app.IpSpider import IpSpider
from app.Models import Gamelog
from tests.TestSpider import TestTools


class TestPsnineSpider(unittest.TestCase):
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

    def testGetPlayerName(self):
        """
            测试获取球员姓名
        """
        spider = PsnineSpider()
        url = "https://www.basketball-reference.com/players/t/turneev01/gamelog/2018"
        playerName = spider.getPlayerName(url)
        self.assertEqual(playerName, "EvanMarcelTurner")

    def testGetGamelogs(self):
        """
            测试获取球员比赛数据
        """
        spider = PsnineSpider()
        url = "https://www.basketball-reference.com/players/t/turneev01/gamelog/2018"
        gameLogs = list(spider.getGameLogs(url))

        # 出场次数
        self.assertEqual(len(gameLogs), 79)
        # 随机抽取样本
        self.assertEqual(gameLogs[2][5], "MIL")

    def testGetPlayerUrls(self):
        """
            获取球员页面url
        """
        spider = PsnineSpider()
        url = "https://www.basketball-reference.com/teams/POR/2018.html"
        playerUrls = list(spider.getPlayerUrls(url))

        self.assertTrue(
            "https://www.basketball-reference.com/players/m/mccolcj01/gamelog/2018"
            in playerUrls)
        self.assertTrue(
            "https://www.basketball-reference.com/players/l/lillada01/gamelog/2018"
            in playerUrls)

    def testGetTeamUrls(self):
        """
            测试获取所有球队url
        """
        spider = PsnineSpider()
        url = "https://www.basketball-reference.com/teams/"
        teamUrls = list(spider.getTeamUrls(url))

        self.assertTrue(
            "https://www.basketball-reference.com/teams/POR/2018.html" in
            teamUrls)
        self.assertTrue(
            "https://www.basketball-reference.com/teams/HOU/2018.html" in
            teamUrls)

    # def testSaveToSql(self):
    #     spider = PsnineSpider()
    #     # 特纳-开拓者
    #     url = "https://www.basketball-reference.com/players/t/turneev01/gamelog/2018"
    #     playerName = spider.getPlayerName(url)
    #     gameLogs = list(spider.getGameLogs(url))

    #     # 存入数据库

    #     for each in gameLogs:
    #         gameLog = Gamelog(playerName, each)
    #         db.session.add(gameLog)
    #     db.session.commit()

    #     # 抽样测试
    #     gameLog = Gamelog.query.filter(
    #         Gamelog.Name == "EvanMarcelTurner",
    #         Gamelog.Date == "2017-11-05 00:00:00").first()

    #     self.assertEqual(gameLog.Opp, "OKC")
    #     self.assertEqual(gameLog.TPA, 1.0)
    #     self.assertEqual(gameLog.PTS, 3.0)
