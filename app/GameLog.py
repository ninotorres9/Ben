# -*- coding: utf-8 -*-


class AGameLog:
    def __init__(self, name, stats):
        self.Name = self.toQuote(name)
        self.Date = self.toQuote(stats[1])
        self.Tm = self.toQuote(stats[3])
        self.Home = 0 if stats[4] == "@" else 1
        self.Opp = self.toQuote(stats[5])
        self.Win = 1 if "W" in stats[6] else 0
        self.MIN = self.toQuote(stats[8])
        self.FG = stats[9]
        self.FGA = stats[10]
        self.FGM = 0.0 if (stats[11] == "") else stats[11]
        self.TP = stats[12]
        self.TPA = stats[13]
        self.TPM = 0.0 if (stats[14] == "") else stats[14]
        self.FT = stats[15]
        self.FTA = stats[16]
        self.FTM = 0.0 if (stats[17] == "") else stats[17]
        self.ORB = stats[18]
        self.DRB = stats[19]
        self.TRB = stats[20]
        self.AST = stats[21]
        self.STL = stats[22]
        self.BLK = stats[23]
        self.TOV = stats[24]
        self.PF = stats[25]
        self.PTS = stats[26]
        if float(self.TOV) == 0.0:
            self.AT = "0.0"
        else:
            self.AT = str(float(self.AST) / float(self.TOV))

    def toQuote(self, value):
        return "\"{value}\"".format(value=value)

    def toSql(self):
        values = [
            str(getattr(self, each)) for each in self.__dict__
            if not callable(getattr(self, each))
        ]

        stats = "({values})".format(values=", ".join(values))
        sql = "REPLACE INTO gamelogs VALUES {values};".format(values=stats)

        return sql

    def toString(self):

        attributes = [
            ":".join([each, str(getattr(self, each))])
            for each in self.__dict__ if not callable(getattr(self, each))
        ]

        return " | ".join(attributes)