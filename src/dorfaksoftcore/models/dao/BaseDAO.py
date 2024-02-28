import pymysql

from dorfaksoftcore.domain.Entity import Entity
from dorfaksoftcore.infrastructure.DBHelper import DBHelper


class BaseDAO(Entity):
    tableName = ""

    def find(self, condition=None, data=None, order="id ASC", tableName=None):
        if condition is None:
            condition = "1=%s"

        if data is None:
            data = (1)

        if tableName is None:
            tableName = self.tableName

        db = DBHelper().getConnection()
        db: pymysql.Connection
        cur = db.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT * FROM " + tableName + " WHERE " + condition + "  order by " + order
        cur.execute(sql, data)
        from pymysql.cursors import Cursor
        cur: Cursor
        row = cur.fetchone()
        if row == None:
            return None
        entity = self.fillData(row)
        cur.close()
        db.close()
        return entity

    def findCustom(self, sql, data=None):

        if data is None:
            data = ()

        db = DBHelper().getConnection()
        cur = db.cursor(pymysql.cursors.DictCursor)
        cur.execute(sql, data)
        row = cur.fetchone()
        if row == None:
            return None
        entity = self.fillData(row)
        cur.close()
        db.close()
        return entity

    def getRow(self, sql, data=None):
        if data is None:
            data = ()

        db = DBHelper().getConnection()
        cur = db.cursor(pymysql.cursors.DictCursor)
        cur.execute(sql, data)
        row = cur.fetchone()

        cur.close()
        db.close()
        return row

    def execQuery(self, sql, data=None):
        if data is None:
            data = ()

        db = DBHelper().getConnection()
        cur = db.cursor(pymysql.cursors.DictCursor)
        cur.execute(sql, data)
        db.commit()
        cur.close()
        db.close()

    def getList(self, condition=None, data=None, page=1, rowCount=1000, order="id ASC", tableName=None):
        if condition is None:
            condition = "1=%s"

        if data is None:
            data = (1)

        if tableName is None:
            tableName = self.tableName

        start = (page - 1) * rowCount
        db = DBHelper().getConnection()
        sql = "SELECT * FROM " + tableName + " WHERE " + condition + " order by " + order + " LIMIT " + str(
            start) + "," + str(rowCount)
        cur = db.cursor(pymysql.cursors.DictCursor)
        cur.execute(sql, data)
        rows = cur.fetchall()
        lst = []
        for row in rows:
            entity = self.fillData(row)
            lst.append(entity)
        cur.close()
        db.close()
        return lst

    def getListCustom(self, sql, data=None, page=1, rowCount=1000, order="id ASC"):

        if data is None:
            data = ()
        start = (page - 1) * rowCount
        db = DBHelper().getConnection()
        if "limit" not in sql:
            sql = sql + " order by " + order + " LIMIT " + str(start) + "," + str(rowCount)
        cur = db.cursor(pymysql.cursors.DictCursor)
        cur.execute(sql, data)
        rows = cur.fetchall()
        lst = []
        for row in rows:
            entity = self.fillData(row)
            lst.append(entity)
        cur.close()
        db.close()
        return lst

    def delete(self, condition, data):
        db = DBHelper().getConnection()
        sql = "DELETE FROM " + self.tableName + " WHERE " + condition
        cur = db.cursor()
        cur.execute(sql, data)
        db.commit()
        cur.close()
        db.close()

    def findProc(self, procedureName, args):
        db = DBHelper().getConnection()
        cur = db.cursor(pymysql.cursors.DictCursor)
        cur.callproc(procedureName, args)
        row = cur.fetchone()
        if row == None:
            return None
        entity = self.fillData(row)
        db.commit()
        cur.close()
        db.close()
        return entity

    def getCount(self, condition=None, data=None, tableName=None):
        if condition is None:
            condition = "1=%s"

        if data is None:
            data = (1)

        if tableName is None:
            tableName = self.tableName

        db = DBHelper().getConnection()
        cur = db.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT count(*) c FROM " + tableName + " WHERE " + condition
        cur.execute(sql, data)
        row = cur.fetchone()
        if row == None:
            return None
        count = row["c"]
        cur.close()
        db.close()
        return count

    def getListProc(self, procedureName, args):
        db = DBHelper().getConnection()
        cur = db.cursor(pymysql.cursors.DictCursor)
        cur.callproc(procedureName, args)
        rows = cur.fetchall()
        lst = []
        for row in rows:
            entity = self.fillData(row)
            lst.append(entity)
        db.commit()
        cur.close()
        db.close()
        return lst

    def fillData(self, row):
        pass
