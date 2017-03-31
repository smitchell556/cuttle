# -*- coding: utf-8
"""
Tests related to creating databases.
"""
import pymysql

from cuttle.columns import Column

from base_class import DbObject, DB, DB2


class CuttleInstanceTestCase(DbObject):

    def test_create_db_no_table(self):
        self.db.create_db()

        cur = self.con.cursor()
        cur.execute('SHOW DATABASES')
        rv = cur.fetchall()
        cur.close()

        self.assertIn((DB,), rv)

    def test_create_db_table(self):
        class TestTable(self.db.Model):
            columns = [Column('c1', 'INT')]

        self.db.create_db()

        cur = self.con.cursor()
        cur.execute('DESCRIBE {}.testtable'.format(DB))
        rv = cur.fetchall()
        cur.close()

        self.assertEqual((('c1', 'int(11)', 'YES', '', None, ''),), rv)

    def test_create_db_improper_table(self):
        class ImproperTestTable(self.db.Model):
            columns = [Column('c1', 'kwyjibo')]

        with self.assertRaises(pymysql.err.ProgrammingError):
            self.db.create_db()

    def test_create_db_multiple(self):
        class TestTable(self.db.Model):
            columns = [Column('c1', 'INT')]

        class TestTable2(self.db2.Model):
            columns = [Column('c2', 'INT')]

        self.db.create_db()
        self.db2.create_db()

        cur = self.con.cursor()
        cur.execute('SHOW DATABASES')
        rv = cur.fetchall()
        cur.close()

        self.assertIn((DB,), rv)
        self.assertIn((DB2,), rv)

        self.con.select_db(DB)

        cur = self.con.cursor()
        cur.execute('SHOW TABLES')
        rv = cur.fetchall()
        cur.close()

        self.assertIn(('testtable',), rv)
        self.assertNotIn(('testtable2',), rv)

        self.con.select_db(DB2)

        cur = self.con.cursor()
        cur.execute('SHOW TABLES')
        rv = cur.fetchall()
        cur.close()

        self.assertIn(('testtable2',), rv)
        self.assertNotIn(('testtable',), rv)

    def test_create_db_nested_models(self):
        class TestTable(self.db.Model):
            columns = [Column('c1', 'INT')]

        class NonTable(TestTable):
            pass

        class TestTable2(NonTable):
            columns = [Column('c2', 'INT')]

        self.db.create_db()

        self.con.select_db(DB)

        cur = self.con.cursor()
        cur.execute('SHOW TABLES')
        rv = cur.fetchall()
        cur.close()

        self.assertIn(('testtable',), rv)
        self.assertIn(('testtable2',), rv)
        self.assertNotIn(('NonTable',), rv)
