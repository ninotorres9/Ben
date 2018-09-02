# -*- coding: utf-8 -*

from app import db


class IP(db.Model):
    __tablename__ = "iplist"
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(64), unique=True)


class Gamelog(db.Model):  # (db.Model):
    __tablename__ = "gamelogs"
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(64))
    Date = db.Column(db.DateTime)
    Team = db.Column(db.String(64))
    Home = db.Column(db.Boolean)
    Opp = db.Column(db.String(64))
    Win = db.Column(db.Boolean)
    MIN = db.Column(db.Integer)
    FG = db.Column(db.Float)
    FGA = db.Column(db.Float)
    FGM = db.Column(db.Float)
    TP = db.Column(db.Float)
    TPA = db.Column(db.Float)
    TPM = db.Column(db.Float)
    FT = db.Column(db.Float)
    FTA = db.Column(db.Float)
    FTM = db.Column(db.Float)
    ORB = db.Column(db.Float)
    DRB = db.Column(db.Float)
    TRB = db.Column(db.Float)
    AST = db.Column(db.Float)
    STL = db.Column(db.Float)
    BLK = db.Column(db.Float)
    TOV = db.Column(db.Float)
    PF = db.Column(db.Float)
    PTS = db.Column(db.Float)
    AT = db.Column(db.Float)

    def __init__(self, name, stats):
        self.Name = name
        self.Date = stats[1]
        self.Team = stats[3]
        self.Home = 0 if stats[4] == "@" else 1
        self.Opp = stats[5]
        self.Win = 1 if "W" in stats[6] else 0
        self.MIN = self.toSecond(stats[8])
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

    def toSecond(self, time):
        minute, second = time.split(":")
        return int(minute) * 60 + int(second)

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