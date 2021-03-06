# -*- coding: utf-8
"""
Tests related to the Cuttle class.
"""
import os
import unittest
import warnings
import time

from cuttle.reef import Cuttle, Column
from cuttlepool import CuttlePool
from cuttlepool.cuttlepool import PoolConnection


DB = '_cuttle_test_db'
DB2 = '_cuttle_test_db2'
HOST = 'localhost'


class BaseDbTestCase(unittest.TestCase):

    def setUp(self):
        self.Pool = CuttlePool
        self.Connection = PoolConnection

        self.credentials = dict(host=HOST)

        self.sql_type = os.environ['TEST_CUTTLE'].lower()

        if self.sql_type == 'mysql':
            import pymysql
            from mysql_credentials import USER, PASSWD

            self.Cursor = pymysql.cursors.Cursor
            self.connect = pymysql.connect

            self.credentials.update(dict(user=USER, passwd=PASSWD))

        self.db = Cuttle(self.sql_type, db=DB, **self.credentials)

        class Heros(self.db.Model):
            columns = [
                Column('hero_id', 'INT', auto_increment=True, primary_key=True),
                Column('hero_name', 'VARCHAR', maximum=16)
            ]
        self.testtable1 = Heros

        self.create_heros_statement = (
            'CREATE TABLE IF NOT EXISTS {} (\n'
            'hero_id INT AUTO_INCREMENT PRIMARY KEY,\n'
            'hero_name VARCHAR(16)\n'
            ')').format(self.testtable1().name)
        self.heros_schema = (('hero_id', 'int(11)', 'NO', 'PRI', None, 'auto_increment'),
                             ('hero_name', 'varchar(16)', 'YES', '', None, ''))

    def tearDown(self):
        warnings.filterwarnings('ignore')
        self.db.drop_db()

    def createPool(self, **kwargs):
        warnings.filterwarnings('ignore')
        return CuttlePool(self.connect, **kwargs)


class DbNestedModelTestCase(BaseDbTestCase):

    def setUp(self):
        super(DbNestedModelTestCase, self).setUp()

        class UselessTable(self.db.Model):
            pass
        self.uselesstable = UselessTable

        class Villains(UselessTable):
            columns = [
                Column('villain_id', 'INT'),
                Column('villain_name', 'VARCHAR', maximum=16)
            ]
        self.testtable2 = Villains


class TwoDbTestCase(BaseDbTestCase):

    def setUp(self):
        super(TwoDbTestCase, self).setUp()

        self.db2 = Cuttle(self.sql_type, db=DB2, **self.credentials)

        class ThrowAway(self.db2.Model):
            columns = [
                Column('throwaway', 'INT')
            ]
        self.testtable2 = ThrowAway

    def tearDown(self):
        super(TwoDbTestCase, self).tearDown()

        self.db2.drop_db()


class CuttleInstanceTestCase(unittest.TestCase):

    def test_improper_sql_type(self):
        with self.assertRaises(ValueError):
            db = Cuttle('wrongsql', db='db')

    def test_no_db(self):
        with self.assertRaises(ValueError):
            db = Cuttle('mysql')

    def test_name_property(self):
        db_name = 'get_schwifty'
        db = Cuttle('mysql', db=db_name)
        self.assertEqual(db.name, db_name)


class CuttleCreateDbTestCase(BaseDbTestCase):

    def test_create_db(self):
        self.db.create_db()

        pool = self.createPool(db=DB, **self.credentials)
        con = pool.get_connection()
        cur = con.cursor()

        # get databases
        cur.execute('SHOW DATABASES')
        dbs = cur.fetchall()

        self.assertIn((DB,), dbs)

    def test_table_schema(self):
        self.db.create_db()

        pool = self.createPool(db=DB, **self.credentials)
        con = pool.get_connection()
        cur = con.cursor()

        # get tables
        cur.execute('SHOW TABLES')
        tbls = cur.fetchall()

        self.assertEqual(((self.testtable1().name,),), tbls)

        # get table schema
        cur.execute('DESCRIBE {}'.format(self.testtable1().name))
        tblschma = cur.fetchall()

        self.assertEqual(self.heros_schema, tblschma)


class CuttleCreateMultiDbTestCase(TwoDbTestCase):

    def test_create_two_dbs(self):
        self.db.create_db()
        self.db2.create_db()

        pool1 = self.createPool(db=DB, **self.credentials)
        pool2 = self.createPool(db=DB2, **self.credentials)

        con1 = pool1.get_connection()
        cur1 = con1.cursor()
        con2 = pool2.get_connection()
        cur2 = con2.cursor()

        # get databases
        cur1.execute('SHOW DATABASES')
        dbs = cur1.fetchall()

        self.assertIn((DB,), dbs)
        self.assertIn((DB2,), dbs)

        # get tables
        cur1.execute('SHOW TABLES')
        tbls1 = cur1.fetchall()
        cur2.execute('SHOW TABLES')
        tbls2 = cur2.fetchall()

        self.assertIn((self.testtable1().name,), tbls1)
        self.assertNotIn((self.testtable2().name,), tbls1)

        self.assertIn((self.testtable2().name,), tbls2)
        self.assertNotIn((self.testtable1().name,), tbls2)


class CuttleCreateDbNestedModelsTestCase(DbNestedModelTestCase):

    def test_correct_tables_made(self):
        self.db.create_db()

        pool = self.createPool(db=DB, **self.credentials)
        con = pool.get_connection()
        cur = con.cursor()

        # get tables
        cur.execute('SHOW TABLES')
        tbls = cur.fetchall()

        self.assertIn((self.testtable1().name,), tbls)
        self.assertIn((self.testtable2().name,), tbls)
        self.assertNotIn((self.uselesstable().name,), tbls)


class CuttleDropDbTestCase(BaseDbTestCase):

    def setUp(self):
        super(CuttleDropDbTestCase, self).setUp()
        self.db.create_db()

    def test_drop_db(self):
        pool = self.createPool(**self.credentials)
        con = pool.get_connection()
        cur = con.cursor()

        # get databases
        cur.execute('SHOW DATABASES')
        dbs = cur.fetchall()

        # make sure database actually exists
        self.assertIn((DB,), dbs)

        # drop the database
        self.db.drop_db()

        # get databases
        cur.execute('SHOW DATABASES')
        dbs = cur.fetchall()

        # make sure database no longer exists
        self.assertNotIn((DB,), dbs)
