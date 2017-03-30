# -*- coding: utf-8
"""
This module contains a TestCase subclass to build fixtures off of.
"""
import unittest

import pymysql.cursors
from cuttle.reef import Cuttle

from ..db_credentials.mysql_credentials import USER, PASSWD


DB = '_cuttle_test_db'
HOST = 'localhost'


class DbObject(unittest.TestCase):

    def setUp(self):
        self.db = Cuttle('mysql', db=DB, user=USER,
                         passwd=PASSWD, host=HOST)
        self.con = pymysql.connect(host=HOST, user=USER, passwd=PASSWD)

    def tearDown(self):
        del self.db

        cur = self.con.cursor()
        cur.execute('DROP DATABASE IF EXISTS {}'.format(DB))

        cur.close()
        self.con.close()

        self.db = None
