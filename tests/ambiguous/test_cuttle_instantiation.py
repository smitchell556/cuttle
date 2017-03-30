# -*- coding: utf-8
"""
Tests related to instantiating the Cuttle class.
"""
import unittest

from cuttle.reef import Cuttle


class CuttleInstanceTestCase(unittest.TestCase):

    def test_cuttle_instantiate_improper_sql(self):
        with self.assertRaises(ValueError):
            Cuttle('toxicsql', db='test_db')
