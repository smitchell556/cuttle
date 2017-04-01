# -*- coding: utf-8
"""
Tests related to the Model class.
"""
import unittest

import pymysql.connections
import pymysql.cursors

from cuttle.columns import Column

from base_class import DbAndSubclassObject, ModelObject, DB


class ModelConnectionTestCase(ModelObject):

    def test_connection_property(self):
        # Test connection object created
        self.assertTrue(isinstance(self.model.connection,
                                   pymysql.connections.Connection))
        self.assertTrue(self.model.connection.open)

        # Close connection
        self.model._connection.close()
        self.assertFalse(self.model._connection.open)

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
