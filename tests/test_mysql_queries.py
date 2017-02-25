# -*- coding: utf-8 -*-
"""

Tests for running mysql queries.

"""
import pytest

import _helpers


def test_mysql_select(db_and_model, mysql_config):
    db, t_class = db_and_model

    exp_select = ['SELECT test_varchar_col FROM testtable']
    exp_select_all = ['SELECT * FROM testtable']

    t_obj = t_class()
    res_select = t_obj.select('test_varchar_col').query
    t_obj.reset_query()
    res_select_all = t_obj.select().query

    assert res_select == exp_select
    assert res_select_all == exp_select_all


def test_mysql_insert(db_and_model, mysql_config):
    db, t_class = db_and_model

    exp_insert = [
        'INSERT INTO testtable (test_int_col, test_varchar_col) VALUES (%s, %s)']
    exp_values = [(None, 'Vegeta'), (7, 'Goku')]

    t_obj = t_class()
    t_obj.insert(('test_int_col', 'test_varchar_col'),
                 ((None, 'Vegeta'), (7, 'Goku')))

    assert t_obj.query == exp_insert
    assert t_obj.values == exp_values


def test_mysql_update(db_and_model, mysql_config):
    db, t_class = db_and_model
    t_obj = t_class()

    exp_update = ['UPDATE testtable SET test_varchar_col=%s']
    exp_values = [('Frieza',)]

    t_obj.update(**{'test_varchar_col': 'Frieza'})

    assert t_obj.query == exp_update
    assert t_obj.values == exp_values


def test_mysql_delete(db_and_model, mysql_config):
    db, t_class = db_and_model

    exp_delete = ['DELETE FROM testtable']

    t_obj = t_class()
    t_obj.delete()

    assert t_obj.query == exp_delete
