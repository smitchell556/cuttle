# -*- coding: utf-8 -*-
"""

Tests for creating database(s).

"""
import pytest

import _helpers


def test_mysql_create_db(db_and_model, mysql_config):
    db = db_and_model[0]

    exp_db = [('testtable',)]
    exp_schema = [
        ('test_int_col', 'int(11)', 'NO', 'PRI', None, 'auto_increment'),
        ('test_varchar_col', 'varchar(16)', 'YES', '', None, '')]

    db.create_db()

    res_db = _helpers._mysql_query(
        mysql_config,
        "SHOW TABLES")

    res_schema = _helpers._mysql_query(
        mysql_config,
        "DESCRIBE testtable")

    assert res_db == exp_db
    assert res_schema == exp_schema
