# -*- coding: utf-8
"""
This module contains TestCase subclasses to build fixtures off of.
"""
import unittest

import pymysql.cursors
from cuttle.reef import Cuttle
from cuttle.columns import Column
from cuttle.model import Model

from mysql_credentials import USER, PASSWD


DB = '_cuttle_test_db'
DB2 = '{}2'.format(DB)
HOST = 'localhost'


class DbObject(unittest.TestCase):

    def setUp(self):
        self.con = pymysql.connect(host=HOST, user=USER, passwd=PASSWD)

        cur = self.con.cursor()
        cur.execute('DROP DATABASE IF EXISTS {}'.format(DB))
        cur.execute('DROP DATABASE IF EXISTS {}'.format(DB2))
        cur.close()

        self.db = Cuttle('mysql', db=DB, user=USER,
                         passwd=PASSWD, host=HOST)
        self.db2 = Cuttle('mysql', db=DB2, user=USER,
                          passwd=PASSWD, host=HOST)

    def tearDown(self):
        del self.db
        del self.db2
        self.db = None
        self.db2 = None

        cur = self.con.cursor()
        cur.execute('DROP DATABASE IF EXISTS {}'.format(DB))
        cur.execute('DROP DATABASE IF EXISTS {}'.format(DB2))
        cur.close()

        self.con.close()


class ModelObject(unittest.TestCase):

    def setUp(self):
        self.Model = Model
        self.Model._configure_model(
            'mysql', user=USER, passwd=PASSWD, host=HOST)
        self.model = Model()

    def tearDown(self):
        del self.model
        self.Model = None


class DbAndSubclassObject(DbObject):

    def setUp(self):
        super(DbAndSubclassObject, self).setUp()

        class TestTable(self.db.Model):
            columns = [Column('c1', 'INT'),
                       Column('c2', 'VARCHAR', maximum=16)]

        self.TestTable = TestTable

        self.db.create_db()

        self.con.select_db(self.db.Model._connection_arguments['db'])

    def tearDown(self):
        del self.TestTable

        super(DbAndSubclassObject, self).tearDown()
