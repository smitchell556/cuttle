# -*- coding: utf-8
"""
Tests related to the Column class.
"""
import unittest

from cuttle.reef import Column


class ColumnNamePropertyTestCase(unittest.TestCase):

    def test_name_property(self):
        name = 'test'
        column = Column(name, 'INT')
        self.assertEqual(column.name, name)

    def test_name_property_is_lowercase(self):
        name = 'TEST'
        column = Column(name, 'INT')
        self.assertEqual(column.name, name.lower())


class ColumnPrimaryKeyPropertyTestCase(unittest.TestCase):

    def test_true_primary_key(self):
        column = Column('test', 'INT', primary_key=True)
        self.assertTrue(column.primary_key)

    def test_false_primary_key(self):
        column = Column('test', 'INT', primary_key=False)
        self.assertFalse(column.primary_key)


class ColumnSchemaTestCase(unittest.TestCase):

    def test_column_basic(self):
        column = Column('test', 'INT')
        column_schema = 'test INT,\n'
        self.assertEqual(column.column_schema(), column_schema)

    def test_column_maximum(self):
        column = Column('test', 'INT', maximum=16)
        column_schema = 'test INT(16),\n'
        self.assertEqual(column.column_schema(), column_schema)

    def test_column_precision(self):
        column = Column('test', 'INT', precision=(8, 2))
        column_schema = 'test INT(8, 2),\n'
        self.assertEqual(column.column_schema(), column_schema)

    def test_column_required(self):
        column = Column('test', 'INT', required=True)
        column_schema = 'test INT NOT NULL,\n'
        self.assertEqual(column.column_schema(), column_schema)

    def test_column_unique(self):
        column = Column('test', 'INT', unique=True)
        column_schema = 'test INT UNIQUE,\n'
        self.assertEqual(column.column_schema(), column_schema)

    def test_column_auto_increment(self):
        column = Column('test', 'INT', auto_increment=True)
        column_schema = 'test INT AUTO_INCREMENT,\n'
        self.assertEqual(column.column_schema(), column_schema)

    def test_column_default_number_type(self):
        column = Column('test', 'INT', default=6)
        column_schema = 'test INT DEFAULT 6,\n'
        self.assertEqual(column.column_schema(), column_schema)

    def test_column_default_string_type(self):
        column = Column('test', 'VARCHAR', maximum=16, default='test')
        column_schema = 'test VARCHAR(16) DEFAULT \'test\',\n'
        self.assertEqual(column.column_schema(), column_schema)

    def test_column_update(self):
        column = Column('test', 'INT', update=6)
        column_schema = 'test INT ON UPDATE 6,\n'
        self.assertEqual(column.column_schema(), column_schema)
