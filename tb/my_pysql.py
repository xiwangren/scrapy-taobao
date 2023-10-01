#! /usr/bin/python
# coding:utf-8
import logging
import time
import pymysql.cursors  # by chandler
import pymysql.err

from . import settings


class PyMySql:
    _conn = None
    _cursor = None

    def __init__(self):
        config = {}
        config['host'] = settings.MYSQL_HOST
        config['port'] = settings.MYSQL_PORT
        config['user'] = settings.MYSQL_USER
        config['password'] = settings.MYSQL_PASSWORD
        config['database'] = settings.MYSQL_DB
        try:
            self._conn = pymysql.connect(**config)
            self._conn.autocommit(True)
            self._cursor = self._conn.cursor()
        except Exception as ex:
            print('("ERROR!!!!,connect db error!")', ex, config)



    # 批量写入
    def insert_batch(self, sql, parm):
        try:
            return self._cursor.executemany(sql, parm)
        except Exception as ex:
            self.close()
            return -1

    # 单条插入
    def insert(self, sql, parm):
        try:
                return self._cursor.execute(sql, parm)
        except Exception as  ex:
            logging.error(ex)
            print(ex)
            return -1
    #
    # # 重写了一个update语句 by chandler 其实和insert语句一样的，都是执行
    # def py_update_chandler(self, sql, parm):
    #     if self.conn is None:
    #         self.conn=self.getConnection_chandler()
    #     try:
    #         with self.conn._cursor() as self._cursor:
    #             self._cursor.execute(sql, parm)
    #     except Exception as ex:
    #         print ('py_update_chandler: ',ex,sql,parm)
    #
    #
    # # 重写了一个select语句 by chandler
    # def py_select_chandler(self,sql,parm):
    #     result=-1
    #     if self.conn is None:
    #         self.conn=self.getConnection_chandler()
    #     try:
    #         with self.conn._cursor() as self._cursor:
    #             self._cursor.execute(sql,parm)
    #             result=self._cursor.fetchone()
    #         return result
    #     except Exception as ex:
    #         print ('py_select_chandler: ',ex)
    #
    # # 重写了一个select语句 给罗林提供旧程序select接口
    # def py_select_tuple(self,sql,parm):
    #     if self.conn is None:
    #         self.conn=self.getConnection_chandler()
    #     try:
    #         with self.conn._cursor() as self._cursor:
    #             self._cursor.execute(sql,parm)
    #             result=self._cursor.fetchall()
    #         return (result)
    #     except pymysql.err.OperationalError as ex:
    #         print ('pymysql.err: ',ex)
    #         self.py_close_chandler()
    #         # self.conn=None
    #         self.conn=self.getConnection_chandler()
    #         return []
    #     except Exception as ex:
    #         print ('py_select_tuple: ',ex)

    def close(self):
        try:
            self._conn.close()
        except pymysql.Error as e:
            pass



