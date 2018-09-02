from urllib import request
from bs4 import BeautifulSoup
from Player import Player
from Spider import Spider
from GameLog import GameLog
import re
import time
import threading
import pymysql
import requests

spider = Spider()


class TeamThread(threading.Thread):
    def __init__(self, url):
        threading.Thread.__init__(self)
        self.url = url

    def run(self):
        global spider
        for playerUrl in spider.getPlayerUrlByTeamUrl(self.url):
            time.sleep(1)
            insertToTable(playerUrl)


def truncateTable():
    db = pymysql.connect(
        host="localhost",
        user="root",
        passwd="9gad9name",
        db="BEN",
        autocommit=True)
    cursor = db.cursor()
    cursor.execute("truncate table gamelogs;")
    db.close()


def insertToTable(url):

    global spider

    db = pymysql.connect(
        host="localhost",
        user="root",
        passwd="9gad9name",
        db="BEN",
        autocommit=True)
    cursor = db.cursor()

    playerName = spider.getPlayerNameByPlayerUrl(url)
    gameLogs = spider.getGameLogsByPlayerUrl(url)
    for gameLog in gameLogs:
        sql = GameLog(playerName, gameLog).toSql()
        print(sql)
        cursor.execute(sql)

    db.close()


def getTeamThreadList(url):
    global spider
    teamUrls = spider.getTeamUrls(url)
    for teamUrl in teamUrls:
        yield TeamThread(teamUrl)


def formatIP(ip):
    return "http://{ip}".format(ip=ip)


def main():
    truncateTable()

    threadList = getTeamThreadList(
        "https://www.basketball-reference.com/teams/")
    for thread in threadList:
        thread.start()

    for thread in threadList:
        thread.join()


if __name__ == '__main__':
    # startTime = time.clock()
    main()

    # ipList = []
    # with open("Source.txt") as inFile:
    #     index = 0
    #     for line in inFile.readlines():
    #         ipList.append(line)

    # with open("IP.txt", "w", encoding="utf-8") as outFile:
    #     for ip in ipList:
    #         outFile.write("http://{ip}".format(ip=ip))