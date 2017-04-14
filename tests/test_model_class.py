# -*- coding: utf-8
"""
Tests related to the Model class.
"""
import unittest

from cuttle.reef import Cuttle, Model
from pymysql.cursors import Cursor

from test_cuttle_class import BaseDbTestCase, PoolConnection


class ModelTestCase(BaseDbTestCase):

    def setUp(self):
        super(ModelTestCase, self).setUp()
        self.db.create_db()

        self.Connection = PoolConnection
        self.Cursor = Cursor


class ModelNameTestCase(unittest.TestCase):

    def test_name_property(self):
        class Lower(Model):
            pass

        self.assertEqual(Lower().name, 'lower')


class ModelConnectionTestCase(ModelTestCase):

    def test_connection_property(self):
        with self.testtable1() as heros:
            self.assertIsInstance(heros.connection, self.Connection)

    def test_cursor_property(self):
        with self.testtable1() as heros:
            self.assertIsInstance(heros.cursor, self.Cursor)


class ModelQueryValuesTestCase(unittest.TestCase):

    def setUp(self):
        class TestModel(Model):
            pass

        self.Model = TestModel

    def test_query_property(self):
        with self.Model() as model:
            query = 'this is a query'
            model._query = query.split(' ')
            self.assertEqual(model.query, query)

    def test_values_property(self):
        with self.Model() as model:
            values = ['these', 'are', 'values']
            model._values = values
            self.assertEqual(model.values, tuple(values))

    def test_seq_of_values_property(self):
        with self.Model() as model:
            seq_of_values = [['these', 'are', 'values'],
                             ['so', 'are', 'these']]
            model._values = seq_of_values
            self.assertEqual(model.seq_of_values,
                             [tuple(v) for v in seq_of_values])
