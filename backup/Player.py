# -*- coding: utf-8 -*-

from Tools import *


class Player:
    def __init__(self, url):
        name, stats = getStatsByUrl(url)
        stats = formatStats(stats)
        self.name = name
        self.GP = stats[0]
        self.MIN = stats[1]
        self.FGM = stats[2]
        self.FGA = stats[3]
        self.FG = stats[4]
        self.TPM = stats[5]
        self.TPA = stats[6]
        self.TP = stats[7]
        self.FTM = stats[8]
        self.FTA = stats[9]
        self.FT = stats[10]
        self.RED = stats[11]
        self.AST = stats[12]
        self.STL = stats[13]
        self.BLK = stats[14]
        self.TOV = stats[15]
        self.PF = stats[16]
        self.PTS = stats[17]
        if float(self.TOV) == 0.0:
            self.AT = "0.0"
        else:
            self.AT = str(float(self.AST) / float(self.TOV))

    def toSql(self):
        values = [
            str(getattr(self, each)) for each in self.__dict__
            if not callable(getattr(self, each))
        ]

        values[0] = "\"{value}\"".format(value=values[0])
        stats = "({values})".format(values=", ".join(values))
        sql = "REPLACE INTO stats VALUES {values};".format(
            name=self.name, values=stats)

        return sql

    def toFile(self):
        values = [
            str(getattr(self, each)) for each in self.__dict__
            if not callable(getattr(self, each))
        ]

        return " | ".join(values)

    def toString(self):

        attributes = [
            ":".join([each, str(getattr(self, each))])
            for each in self.__dict__ if not callable(getattr(self, each))
        ]

        return " | ".join(attributes)