# -*- coding: UTF-8 -*-

import pymysql
import operator


class Player:
    def __init__(self, stats):
        self.name = stats[0]
        self.PTS = stats[1]
        self.AT = stats[2]
        self.FGM = stats[3]
        self.FGA = stats[4]
        self.FG = stats[5]
        self.TPM = stats[6]
        self.TPA = stats[7]
        self.TP = stats[8]
        self.FTM = stats[9]
        self.FTA = stats[10]
        self.FT = stats[11]
        self.ORB = stats[12]
        self.DRB = stats[13]
        self.TRB = stats[14]
        self.AST = stats[15]
        self.STL = stats[16]
        self.BLK = stats[17]
        self.TOV = stats[18]
        self.PF = stats[19]
        self.GP = stats[20]
        # 稳定性
        self.STA = stats[21]

    def __str__(self):

        attributes = [
            ":".join([each, str(getattr(self, each))])
            for each in self.__dict__ if not callable(getattr(self, each))
        ]

        return " | ".join(attributes)

    def div(self, lhs, rhs):
        return float(lhs) / float(rhs)

    def executeScore(self, average):
        """
            计算球员范特西得分（[单项数据/均值]*系数）
        """
        # PTS, ORB, TRB, AST, STL, BLK, TOV, AT, FG, FT, TPM

        factor = 3.0
        factor2 = 6.0

        return sum([
            self.div(self.PTS, average.PTS) * factor,
            self.div(self.ORB, average.ORB) * factor2,
            self.div(self.TRB, average.TRB) * factor,
            self.div(self.AST, average.AST),
            self.div(self.STL, average.STL),
            -self.div(self.TOV, average.TOV) * factor2,
            self.div(self.AT, average.AT),
            self.div(self.FG, average.FG) * factor,
            self.div(self.FT, average.FT) * factor2,
            self.div(self.TPM, average.TPM),
            self.div(self.GP, average.GP)
        ]) * self.STA


class Pair:
    def __init__(self, name, score):
        self.name = name
        self.score = score

    def toString(self):
        return "{name}: {score}".format(name=self.name, score=self.score)


def connectDB():
    db = pymysql.connect(
        host="localhost",
        user="root",
        passwd="9gad9name",
        db="BEN",
        autocommit=True)
    return db


def executeAverage():
    '''
        计算数据库中每个字段的平均值，存入class Player
    '''
    db = connectDB()
    cursor = db.cursor()

    sql = "SELECT AVG(PTS), AVG(AT), AVG(FGM), AVG(FGA), AVG(FG), AVG(TPM), AVG(TPA), AVG(TP), AVG(FTM), AVG(FTA), AVG(FT), AVG(ORB), AVG(DRB), AVG(TRB), AVG(AST), AVG(STL), AVG(BLK), AVG(TOV), AVG(PF) FROM gamelogs;"
    cursor.execute(sql)
    stats = ["average"]
    # 解双层嵌套
    for i in cursor.fetchall():
        for j in i:
            stats.append(j)

    stats.append(50.0)  # 出场次数GP的平均值设为50
    stats.append(0)  # 标准差部分添零防止报错

    db.close()

    return Player(stats)


def getPlayersStats():
    '''
        导出球员数据， 存入class Player
    '''
    db = connectDB()
    cursor = db.cursor()

    # 导出球员数据
    sql = """
    SELECT Name, AVG(PTS), AVG(AT), AVG(FGM), AVG(FGA), AVG(FG), AVG(TPM), AVG(TPA), AVG(TP), AVG(FTM), AVG(FTA), AVG(FT), AVG(ORB), AVG(DRB), AVG(TRB), AVG(AST), AVG(STL), AVG(BLK), AVG(TOV), AVG(PF), COUNT(*), stddev(PTS), stddev(PTS) * 0.3 + stddev(AT) * 0.92 + stddev(FG) * 0.77 + stddev(TPM) * 5.54 + stddev(FT) * 0.66 + stddev(ORB) * 1.1 + stddev(TRB) * 0.57 + stddev(AST) * 0.79 + stddev(STL) * 1.73 + stddev(BLK) * 1.54 + stddev(TOV) * 1.26 AS "Stable" FROM gamelogs GROUP BY Name;
    """
    # sql = """
    # SELECT Name, AVG(PTS), AVG(AT), AVG(FGM), AVG(FGA), AVG(FG), AVG(TPM), AVG(TPA), AVG(TP), AVG(FTM), AVG(FTA), AVG(FT), AVG(ORB), AVG(DRB), AVG(TRB), AVG(AST), AVG(STL), AVG(BLK), AVG(TOV), AVG(PF), COUNT(*), stddev(PTS) FROM gamelogs GROUP BY Name;
    # """
    cursor.execute(sql)
    players = [Player(stats) for stats in cursor.fetchall()]

    db.close()

    return players


def getPlayersScore(average):
    '''
        计算球员范特西得分
    '''
    players = getPlayersStats()
    scores = [round(player.executeScore(average), 2) for player in players]
    names = [player.name for player in players]
    return names, scores


def main():

    # playerStats = getPlayersStats()
    # for each in playerStats:
    #     print(str(each))

    # db = connectDB()
    # cursor = db.cursor()

    # sql = """
    #     SELECT Name, AVG(PTS), AVG(AT), AVG(FGM), AVG(FGA), AVG(FG), AVG(TPM), AVG(TPA), AVG(TP), AVG(FTM), AVG(FTA), AVG(FT), AVG(ORB), AVG(DRB), AVG(TRB), AVG(AST), AVG(STL), AVG(BLK), AVG(TOV), AVG(PF), COUNT(*), stddev(PTS), stddev(PTS) * 0.3 + stddev(AT) * 0.92 + stddev(FG) * 0.77 + stddev(TPM) * 5.54 + stddev(FT) * 0.66 + stddev(ORB) * 1.1 + stddev(TRB) * 0.57 + stddev(AST) * 0.79 + stddev(STL) * 1.73 + stddev(BLK) * 1.54 + stddev(TOV) * 1.26 AS "Stable" FROM gamelogs GROUP BY Name;
    # """
    # cursor.execute(sql)

    # for each in cursor.fetchall():
    #     print(each)

    # db.close()

    average = executeAverage()
    names, scores = getPlayersScore(average)

    # 结构化
    Pairs = [Pair(name, score) for name, score in zip(names, scores)]
    Pairs.sort(key=operator.attrgetter("score"))
    for pair in Pairs:
        print(pair.toString())


if __name__ == '__main__':
    main()
