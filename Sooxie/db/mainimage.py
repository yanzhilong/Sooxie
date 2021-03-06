# -*- coding: utf-8 -*-
from base import Base
from Sooxie import db
from Sooxie.db import MainImageTable
from Sooxie.domain.Shoe import Shoe as ShoeDomain
from Sooxie.domain.Shoe import MainImage as MainImageDomain

from sqlalchemy.sql import select


class MainImage(Base):

    def __init__(self):
        pass

    def addentry(self, entry):
        ins = MainImageTable.insert().values(Id=entry.Id, Url=entry.Url, Sort=entry.Sort, ShoeId=entry.ShoeId)
        conn = db.engine.connect()
        conn.execute(ins)

    def addentrys(self, entrys):
        connection = db.engine.connect()
        trans = connection.begin()
        try:
            for entry in entrys:
                ins = MainImageTable.insert().values(Id=entry.Id, Url=entry.Url, Sort=entry.Sort, ShoeId=entry.ShoeId)
                connection.execute(ins)
            trans.commit()
        except Exception,e:
            print(u"添加mainimage异常" + e.message)
            trans.rollback()

    def updateentry(self, entry):
        connection = db.engine.connect()
        stmt = MainImageTable.update(). \
            where(MainImageTable.c.Id == entry.Id). \
            values(Url=entry.Url, Sort=entry.Sort, ShoeId=entry.ShoeId)
        connection.execute(stmt)

    def updateentrys(self, entrys):
        connection = db.engine.connect()
        trans = connection.begin()
        try:
            for entry in entrys:
                stmt = MainImageTable.update(). \
                    where(MainImageTable.c.Id == entry.Id). \
                    values(Url=entry.Url, Sort=entry.Sort, ShoeId=entry.ShoeId)
                connection.execute(stmt)
            trans.commit()
        except Exception, e:
            trans.rollback()

    def deleteentry(self, entry):
        connection = db.engine.connect()
        connection.execute(MainImageTable.delete().where(MainImageTable.c.Id == entry.Id))

    def deleteentrys(self, entrys):
        connection = db.engine.connect()
        trans = connection.begin()
        try:
            for entry in entrys:
                connection.execute(MainImageTable.delete().where(MainImageTable.c.Id == entry.Id))
            trans.commit()
        except Exception, e:
            trans.rollback()

    def getbyid(self, entry):
        connection = db.engine.connect()
        s = select([MainImageTable]).where(MainImageTable.c.Id == entry.Id)
        row = connection.execute(s).fetchone()
        shoe = ShoeDomain()
        shoe.Id = row['Id']
        shoe.Url = row['Url']
        shoe.Sort = row['Sort']
        shoe.ShoeId = row['ShoeId']
        return shoe

    def getentrys(self):
        connection = db.engine.connect()
        s = select([MainImageTable])
        imageslist = []
        for row in connection.execute(s):
            image = MainImageDomain()
            image.Id = row['Id']
            image.Url = row['Url']
            image.Sort = row['Sort']
            image.ShoeId = row['ShoeId']
            imageslist.append(image)
        return imageslist

    def deleteall(self):
        connection = db.engine.connect()
        connection.execute(MainImageTable.delete())