# -*- coding: utf-8 -*-
"""

Tests for running mysql queries.

"""
import pytest

import _helpers


def test_mysql_select(db_and_model, mysql_config):
    db, t_class = db_and_model

    exp_select = ((7, 'Goku'),)
    exp_select_all = ((1, 'Vegeta'), (7, 'Goku'))

    db.create_db()
    t_obj = t_class()
    t_obj.connect()

    _helpers._mysql_insert(
        mysql_config,
        "INSERT INTO {} (test_varchar_col) VALUES ('Vegeta')".format(
            t_obj.name))
    _helpers._mysql_insert(
        mysql_config,
        "INSERT INTO {} (test_int_col, test_varchar_col) VALUES (7, 'Goku')".format(
            t_obj.name))

    res_select = t_obj.select(test_varchar_col='Goku')
    res_select_all = t_obj.select()

    t_obj.close()

    assert res_select == exp_select
    assert res_select_all == exp_select_all

def test_mysql_insert(db_and_model, mysql_config):
    db, t_class = db_and_model
    db.create_db()

    exp_insert = [(1, 'Vegeta'), (7, 'Goku')]

    t_obj = t_class()
    t_obj.connect()
    t_obj.insert(('test_int_col', 'test_varchar_col'),
                 ((None, 'Vegeta'), (7, 'Goku')))
    t_obj.close()

    res = _helpers._mysql_query(
        mysql_config,
        "SELECT * FROM {}".format(t_obj.name)
    )

    assert res == exp_insert

def test_mysql_update(db_and_model, mysql_config):
    db, t_class = db_and_model
    db.create_db()
    t_obj = t_class()

    exp_update1 = [(1, 'Frieza'), (7, 'Frieza')]
    exp_update2 = [(1, 'Frieza'), (7, 'Master Roshi')]

    _helpers._mysql_insert(
        mysql_config,
        "INSERT INTO {} (test_varchar_col) VALUES ('Vegeta')".format(
            t_obj.name))
    _helpers._mysql_insert(
        mysql_config,
        "INSERT INTO {} (test_int_col, test_varchar_col) VALUES (7, 'Goku')".format(
            t_obj.name))

    t_obj.connect()
    t_obj.update({'test_varchar_col': 'Frieza'})

    res = _helpers._mysql_query(
        mysql_config,
        "SELECT * FROM {}".format(t_obj.name)
    )

    assert res == exp_update1

    t_obj.update({'test_varchar_col': 'Master Roshi'}, {'test_int_col': 7})

    res = _helpers._mysql_query(
        mysql_config,
        "SELECT * FROM {}".format(t_obj.name)
    )

    assert res == exp_update2

    t_obj.close()

def test_mysql_delete(db_and_model, mysql_config):
    db, t_class = db_and_model

    exp_delete = [(7, 'Goku')]

    db.create_db()
    t_obj = t_class()
    t_obj.connect()

    _helpers._mysql_insert(
        mysql_config,
        "INSERT INTO {} (test_varchar_col) VALUES ('Vegeta')".format(
            t_obj.name))
    _helpers._mysql_insert(
        mysql_config,
        "INSERT INTO {} (test_int_col, test_varchar_col) VALUES (7, 'Goku')".format(
            t_obj.name))

    res_select = t_obj.delete(test_varchar_col='Vegeta')

    t_obj.close()

    res = _helpers._mysql_query(
        mysql_config,
        "SELECT * FROM {}".format(t_obj.name)
    )

    assert res == exp_delete
