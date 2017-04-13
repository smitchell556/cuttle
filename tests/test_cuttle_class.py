# -*- coding: utf-8
"""
Tests related to the Cuttle class.
"""
import unittest

from cuttle.reef import Cuttle


class CuttleInstanceTestCase(unittest.TestCase):

    def test_cuttle_instantiate_mysql(self):
        db = Cuttle('mysql', db='test_db')
        self.assertEqual('mysql', db.Model._sql_type)

    def test_cuttle_instantiate_improper_sql(self):
        with self.assertRaises(ValueError):
            Cuttle('toxicsql', db='test_db')
