# -*- coding: utf-8
"""
This module contains TestCase subclasses to build fixtures off of.
"""
import unittest

from cuttle.columns import Column
from cuttle.model import Model


class ModelObject(unittest.TestCase):

    def setUp(self):
        self.Model = Model
        self.Model._configure_model('mysql')
        self.model = Model()

    def tearDown(self):
        del self.model
        self.Model = None


class ModelSubclassObject(unittest.TestCase):

    def setUp(self):
        self.Model = Model
        self.Model._configure_model('mysql')

        class TestTable(self.Model):
            columns = [Column('c1', 'INT'),
                       Column('c2', 'INT')]

        self.TestTable = TestTable

        self.testtable = self.TestTable()

    def tearDown(self):
        del self.testtable
        del self.TestTable
        self.Model = None
