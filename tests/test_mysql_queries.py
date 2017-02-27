# -*- coding: utf-8 -*-
"""

Tests for running mysql queries.

"""
import pytest

import _helpers


def test_mysql_select(db_and_model):
    t_class = db_and_model[1]

    exp_select = ['SELECT test_varchar_col FROM testtable']
    exp_select_all = ['SELECT * FROM testtable']

    t_obj = t_class()
    res_select = t_obj.select('test_varchar_col').query
    t_obj.reset_query()
    res_select_all = t_obj.select().query

    assert res_select == exp_select
    assert res_select_all == exp_select_all


def test_mysql_insert(db_and_model):
    t_class = db_and_model[1]

    exp_insert = [
        'INSERT INTO testtable (test_int_col, test_varchar_col) VALUES (%s, %s)']
    exp_values = [(None, 'Vegeta'), (7, 'Goku')]

    t_obj = t_class()
    t_obj.insert(('test_int_col', 'test_varchar_col'),
                 ((None, 'Vegeta'), (7, 'Goku')))

    assert t_obj.query == exp_insert
    assert t_obj.values == exp_values


def test_mysql_update(db_and_model):
    t_class = db_and_model[1]
    t_obj = t_class()

    exp_update = ['UPDATE testtable SET test_varchar_col=%s']
    exp_values = [['Frieza']]

    t_obj.update(**{'test_varchar_col': 'Frieza'})

    assert t_obj.query == exp_update
    assert t_obj.values == exp_values


def test_mysql_delete(db_and_model):
    t_class = db_and_model[1]

    exp_delete = ['DELETE FROM testtable']

    t_obj = t_class()
    t_obj.delete()

    assert t_obj.query == exp_delete


def test_mysql_where(db_and_model):
    t_class = db_and_model[1]

    exp_where1 = ['WHERE test_int_col=%s']
    exp_values1 = [[1]]
    exp_where2 = ['WHERE test_int_col=%s AND test_varchar_col=%s']
    exp_values2 = [[7, 'Goku']]

    t_obj = t_class()

    t_obj.where(test_int_col=1)
    assert t_obj.query == exp_where1
    assert t_obj.values == exp_values1

    t_obj.reset_query()

    t_obj.where(test_int_col=7, test_varchar_col='Goku')
    assert t_obj.query == exp_where2
    assert t_obj.values == exp_values2


def test_mysql_generate_statement(db_and_model):
    t_class = db_and_model[1]

    exp_clause1 = 'SELECT * FROM testtable WHERE test_int_col=%s'
    exp_values1 = (1,)
    exp_clause2 = 'INSERT INTO testtable (test_varchar_col) VALUES (%s)'
    exp_values2 = [('Tien',), ('Yamcha',)]

    t_obj = t_class()

    t_obj.select().where(test_int_col=1)
    assert t_obj._generate_statement() == (exp_clause1, exp_values1)

    t_obj.reset_query()

    t_obj.insert(['test_varchar_col'], [('Tien',), ('Yamcha',)])
    assert t_obj._generate_statement() == (exp_clause2, exp_values2)
