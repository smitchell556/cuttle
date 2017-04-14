# -*- coding: utf-8
"""
Tests related to the Cuttle class.
"""
import os
import unittest

from cuttle.reef import Cuttle, Column
from cuttlepool import CuttlePool
from cuttlepool.cuttlepool import PoolConnection


DB = '_cuttle_test_db'
DB2 = '_cuttle_test_db2'
HOST = 'localhost'


class BaseDbTestCase(unittest.TestCase):

    def setUp(self):
        self.credentials = dict(host=HOST)

        self.sql_type = os.environ['CUTTLE_SQL'].lower()

        if self.sql_type == 'mysql':
            from mysql_credentials import USER, PASSWD

            self.credentials.update(dict(user=USER, passwd=PASSWD))

        self.db = Cuttle(self.sql_type, db=DB, **self.credentials)

        class Heros(self.db.Model):
            columns = [
                Column('hero_id', 'INT'),
                Column('hero_name', 'VARCHAR', maximum=16)
            ]
        self.testtable1 = Heros

        self.create_heros_statement = (
            'CREATE TABLE IF NOT EXISTS {} (\n'
            'hero_id INT,\n'
            'hero_name VARCHAR(16)\n'
            ')').format(self.testtable1().name)
        self.heros_schema = (('hero_id', 'int(11)', 'YES', '', None, ''),
                             ('hero_name', 'varchar(16)', 'YES', '', None, ''))

    def tearDown(self):
        with self.db.Model() as drop_db:
            drop_db.append_query('DROP DATABASE IF EXISTS {}'.format(DB))
            drop_db.execute()

    def createPool(self, **kwargs):
        return CuttlePool(**kwargs)


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

        self.villains_schema = (('villain_id', 'int(11)', 'YES', '', None, ''),
                                ('villain_name', 'varchar(16)', 'YES', '', None, ''))


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

        with self.db2.Model() as drop_db:
            drop_db.append_query('DROP DATABASE IF EXISTS {}'.format(DB2))
            drop_db.execute()


class CuttleInstanceTestCase(unittest.TestCase):

    def test_improper_sql_type(self):
        with self.assertRaises(ValueError):
            db = Cuttle('wrongsql', db='db')

    def test_no_db(self):
        with self.assertRaises(ValueError):
            db = Cuttle('mysql')


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

        self.assertEqual(((self.testtable1().name,),), tbls1)
        self.assertEqual(((self.testtable2().name,),), tbls2)


class CuttleCreateDbNestedModels(DbNestedModelTestCase):

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

        # get table schema
        cur.execute('DESCRIBE {}'.format(self.testtable2().name))
        tblschma = cur.fetchall()

        self.assertEqual(self.villains_schema, tblschma)
