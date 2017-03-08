# -*- coding: utf-8 -*-
"""

Tests for creating database(s).

"""
from cuttle._db_helpers import _nested_subclasses
from cuttle._mysql_methods import _generate_db, _generate_table_schema


def test_mysql_create_db(db_and_model):
    db = db_and_model[0]

    exp_db = 'CREATE DATABASE IF NOT EXISTS fake_db'
    exp_schema = ('USE fake_db; CREATE TABLE IF NOT EXISTS testtable ( '
                  'test_int_col INT AUTO_INCREMENT, '
                  'test_varchar_col VARCHAR(16), '
                  'PRIMARY KEY (test_int_col) );')

    db_name = db.Model._get_config()['DB']
    model_subclasses = _nested_subclasses(db.Model)

    res_db = _generate_db(db_name)
    res_schema = _generate_table_schema(db_name, model_subclasses)

    assert res_db == exp_db
    assert res_schema == exp_schema
