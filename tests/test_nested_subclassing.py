# -*- coding: utf-8 -*-
"""

Tests for configuring Cuttle.

"""
import pytest

import cuttle.columns

import _helpers


def test_nested_subclass_table_generation(db_and_subclass, mysql_config):
    db, s_class = db_and_subclass
    db.create_db()

    exp_db = [('nonemptymodel',)]
    exp_schema = [
        ('test_int', 'int(11)', 'NO', 'PRI', None, 'auto_increment')]
    db.create_db()

    res_db = _helpers._mysql_query(
        mysql_config,
        "SHOW TABLES")

    res_schema = _helpers._mysql_query(
        mysql_config,
        "DESCRIBE nonemptymodel")

    assert res_db == exp_db
    assert res_schema == exp_schema
