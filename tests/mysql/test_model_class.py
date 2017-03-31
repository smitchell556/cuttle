# -*- coding: utf-8
"""
Tests related to the Model class.
"""
import unittest

from pymysql.connections import Connection
from pymysql.cursors import Cursor, DictCursor, SSCursor, SSDictCursor

from cuttle.columns import Column

from base_class import ModelObject, DB


class ModelConnectionTestCase(ModelObject):

    def test_connection_property(self):
        # Test connection object created
        self.assertTrue(isinstance(self.model.connection, Connection))
        self.assertTrue(self.model.connection.open)

        # Close connection
        self.model._connection.close()
        self.assertFalse(self.model._connection.open)

        # Test connection is reopened when connection property is accessed
        self.assertTrue(self.model.connection.open)

    def test_cursor_property(self):
        # Test cursor object created
        self.assertTrue(isinstance(self.model.cursor, Cursor))

        # Close cursor
        self.model._cursor.close()
        self.assertIsNone(self.model._cursor.connection)

        # Test open cursor is made when cursor property is accessed
        self.assertTrue(isinstance(self.model.cursor.connection, Connection))
