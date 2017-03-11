# -*- coding: utf-8 -*-
"""

Tests for creating database(s).

"""
from cuttle.model import _nested_subclasses


def test_mysql_create_db(db_and_model):
    db = db_and_model[0]

    exp_db = 'CREATE DATABASE IF NOT EXISTS fake_db'
    exp_schema = ('USE fake_db; CREATE TABLE IF NOT EXISTS testtable ( '
                  'test_int_col INT AUTO_INCREMENT, '
                  'test_varchar_col VARCHAR(16), '
                  'test_varchar_col2 VARCHAR(32), '
                  'PRIMARY KEY (test_int_col) );')

    db_name = db.Model._get_config()['db']
    model_subclasses = _nested_subclasses(db.Model)

    res_db = db.Model._generate_db()
    res_schema = db.Model._generate_table_schema()

    assert res_db == exp_db
    assert res_schema == exp_schema
