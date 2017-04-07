# -*- coding: utf-8
"""
Tests related to the Model class.
"""
import pymysql.connections
import pymysql.cursors
from cuttlepool.cuttlepool import PoolConnection

from base_class import DbAndSubclassObject, ModelObject, DB


class ModelConnectionTestCase(ModelObject):

    def test_connection_property(self):
        # Test connection object created
        self.assertTrue(isinstance(self.model.connection,
                                   PoolConnection))
        self.assertTrue(self.model.connection.open)

        # Close connection
        self.model._connection.close()
        with self.assertRaises(AttributeError):
            self.model._connection.open

        # Test connection is reopened when connection property is accessed
        self.assertTrue(self.model.connection.open)

    def test_cursor_property(self):
        # Test cursor object created
        self.assertTrue(isinstance(self.model.cursor,
                                   pymysql.cursors.Cursor))

        # Close cursor
        self.model._cursor.close()
        self.assertIsNone(self.model._cursor.connection)

        # Test open cursor is made when cursor property is accessed
        self.assertTrue(isinstance(self.model.cursor.connection,
                                   pymysql.connections.Connection))

    def test_close(self):
        # Test connection object created
        self.assertTrue(isinstance(self.model.connection,
                                   PoolConnection))
        self.assertTrue(self.model.connection.open)

        # Test cursor object created
        self.assertTrue(isinstance(self.model.cursor,
                                   pymysql.cursors.Cursor))

        # Call close method
        self.model.close()
        with self.assertRaises(AttributeError):
            self.model._connection.open
        self.assertIsNone(self.model._cursor)

    def test_close_cursor(self):
        # Test cursor object created
        self.assertTrue(isinstance(self.model.cursor,
                                   pymysql.cursors.Cursor))

        # Close cursor
        self.model._close_cursor()
        self.assertIsNone(self.model._cursor)

    def test_close_connection(self):
        # Test connection object created
        self.assertTrue(isinstance(self.model.connection,
                                   PoolConnection))
        self.assertTrue(self.model.connection.open)

        # Close connection
        self.model._close_connection()
        with self.assertRaises(AttributeError):
            self.model._connection.open


class ModelExecuteTestCase(DbAndSubclassObject):

    def test_execute(self):
        with self.TestTable() as testtable:
            testtable.append_query('SELECT DATABASE()')
            testtable.execute()
            self.assertEqual((DB,), testtable.cursor.fetchone())

    def test_select_execute(self):
        cur = self.con.cursor()
        cur.execute('INSERT INTO {} (c1, c2) VALUES (%s, %s)'.format(
            self.TestTable.__name__.lower()), (1, 'val'))
        self.con.commit()
        cur.close()

        with self.TestTable() as testtable:
            testtable.select().execute()
            self.assertEqual((1, 'val'), testtable.cursor.fetchone())

            testtable.select('c1').execute()
            self.assertEqual((1,), testtable.cursor.fetchone())

    def test_insert_execute(self):
        with self.TestTable() as testtable:
            testtable.insert().execute()
            testtable.insert(['c1', 'c2'], [1, 'val']).execute()

        cur = self.con.cursor()
        cur.execute('SELECT * FROM testtable')
        rv = cur.fetchall()
        cur.close()

        self.assertIn((None, None), rv)
        self.assertIn((1, 'val'), rv)

    def test_update_execute(self):
        cur = self.con.cursor()
        cur.execute('INSERT INTO testtable (c1, c2) VALUES (%s, %s)',
                    (1, 'val'))
        self.con.commit()

        with self.TestTable() as testtable:
            testtable.update(c1=2).execute()

        cur.execute('SELECT * FROM testtable')
        rv = cur.fetchall()
        cur.close()

        self.assertEqual(((2, 'val'),), rv)

    def test_delete_execute(self):
        cur = self.con.cursor()
        cur.execute('INSERT INTO testtable (c1, c2) VALUES (%s, %s)',
                    (1, 'val'))
        self.con.commit()

        with self.TestTable() as testtable:
            testtable.delete().execute()

        cur.execute('SELECT * FROM testtable')
        rv = cur.fetchall()
        cur.close()

        self.assertEqual(tuple(), rv)

    def test_where_execute(self):
        cur = self.con.cursor()
        cur.executemany('INSERT INTO testtable (c1, c2) VALUES (%s, %s)',
                        [(1, 'val'), (2, 'val2')])
        self.con.commit()
        cur.close()

        with self.TestTable() as testtable:
            testtable.select().where(c1=1).execute()
            self.assertEqual(((1, 'val'),), testtable.cursor.fetchall())


class ModelExecuteManyTestCase(DbAndSubclassObject):

    def test_insert_executemany(self):
        with self.TestTable() as testtable:
            testtable.insert(
                ['c1', 'c2'],
                [[1, 'val'], [2, 'val2']]
            ).executemany()

        cur = self.con.cursor()
        cur.execute('SELECT * FROM testtable')
        rv = cur.fetchall()
        cur.close()

        self.assertEqual(((1, 'val'), (2, 'val2')), rv)


class ModelFetchTestCase(DbAndSubclassObject):

    def setUp(self):
        super(ModelFetchTestCase, self).setUp()

        cur = self.con.cursor()
        cur.executemany('INSERT INTO testtable (c1, c2) VALUES (%s, %s)',
                        [(1, 'val'), (2, 'val2'), (3, 'val3')])
        self.con.commit()
        cur.close()

    def test_fetchone(self):
        with self.TestTable() as testtable:
            testtable.select().execute()
            self.assertEqual((1, 'val'), testtable.fetchone())

    def test_fetchmany(self):
        with self.TestTable() as testtable:
            testtable.select().execute()
            self.assertEqual(((1, 'val'), (2, 'val2')), testtable.fetchmany(2))
            self.assertEqual(((3, 'val3'),), testtable.fetchmany())

            testtable.select().execute()
            self.assertEqual(((1, 'val'),), testtable.fetchmany())

            testtable.select().execute()
            self.assertEqual(((1, 'val'), (2, 'val2'), (3, 'val3')),
                             testtable.fetchmany(4))

    def test_fetchall(self):
        with self.TestTable() as testtable:
            testtable.select().execute()
            self.assertEqual(((1, 'val'), (2, 'val2'), (3, 'val3')),
                             testtable.fetchall())

    def test_fetch_iter(self):
        with self.TestTable() as testtable:
            testtable.select().execute()
            for row in testtable:
                self.assertIn(row, ((1, 'val'), (2, 'val2'), (3, 'val3')))
