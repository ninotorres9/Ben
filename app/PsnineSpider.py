# -*- coding: utf-8 -*-

from app.Spider import Spider
from app.Models import Gamelog
from app import db
import re
import time


class PsnineSpider(Spider):
    gamelogs = []

    def saveToList(self, teamUrl):

        for playerUrl in self.getPlayerUrls(teamUrl):
            name = self.getPlayerName(playerUrl)
            for gamelog in self.getGameLogs(playerUrl):
                print("{name}: {gamelog}".format(name=name, gamelog=gamelog))
                self.gamelogs.append(Gamelog(name, gamelog))
            time.sleep(0.2)

    def getPlayerName(self, playerUrl):
        """
            获取球员姓名（去除空白符）
        """
        soup = self.getSoup(playerUrl)
        playerName = soup.findAll("strong")[2].getText()
        return playerName.replace('\n', ' ').replace(' ', '')

    def getGameLogs(self, playerUrl):
        """
            获取球员数据列表（每场）
        """
        soup = self.getSoup(playerUrl)
        for tr in soup.findAll("tr", id={re.compile("pgl_basic.\d+")}):
            player = []
            for td in tr.findAll("td"):
                player.append(td.getText())
            yield player

    def getPlayerUrls(self, teamUrl):
        """
            获取球员页面url
        """
        soup = self.getSoup(teamUrl)
        for a in soup.findAll(
                "a", href={re.compile("/players/.+html")}, title=""):
            # 获取球员url
            playUrl = self.baseUrl + a['href']
            # 更换为gamelog页面
            yield playUrl.split(".html")[0] + "/gamelog/2018"

    def getTeamUrls(self, url):
        """
            获取球队url列表
        """
        soup = self.getSoup(url)
        for a in soup.findAll(
                "a", href={re.compile("/teams/.+2018.html")}, title=""):
            # 获取球员url
            yield self.baseUrl + a['href']