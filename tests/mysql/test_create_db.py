# -*- coding: utf-8
"""
Tests related to creating databases.
"""
from base_class import DbObject, DB


class CuttleInstanceTestCase(DbObject):

    def test_create_db(self):
        self.db.create_db()

        cur = self.con.cursor()
        cur.execute('SHOW DATABASES')
        rv = cur.fetchall()
        cur.close()

        self.assertIn(DB, rv)
