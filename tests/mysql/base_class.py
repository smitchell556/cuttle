# -*- coding: utf-8
"""
This module contains a TestCase subclass to build fixtures off of.
"""
import unittest

import pymysql.cursors
from cuttle.reef import Cuttle

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