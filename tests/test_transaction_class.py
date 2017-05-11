# -*- coding: utf-8
"""
Tests related to the Transaction class.
"""
from cuttle.transaction import Transaction

from test_model_class import ModelTestCase


class TransactionTestCase(ModelTestCase):

    def setUp(self):
        super(TransactionTestCase, self).setUp()

        self.con = self.pool.get_connection()
        self.cur = self.con.cursor()


class TransactionCloseTestCase(TransactionTestCase):

    def test_close(self):
        t = Transaction(self.pool.get_connection())
        self.assertIsInstance(t._connection, self.Connection)

        t.end()
        self.assertIsNone(t._connection)
