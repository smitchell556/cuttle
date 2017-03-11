# -*- coding: utf-8 -*-
"""

Tests for configuring Cuttle.

"""
import time

import pytest

import cuttle.home


def test_config_values():
    db_name = '_test_db_{}'.format(str(time.time()).split('.')[0])
    db = cuttle.home.Cuttle(
        'mysql', db_name, 'localhost', 'test_user', 'test_pw')
    expected = {
        'db': db_name,
        'host': 'localhost',
        'user': 'test_user',
        'passwd': 'test_pw'
    }
    assert expected['db'] == db.Model._config['db']
    assert expected['host'] == db.Model._config['host']
    assert expected['user'] == db.Model._config['user']
    assert expected['passwd'] == db.Model._config['passwd']


def test_invalid_sql():
    db_name = '_test_db_{}'.format(str(time.time()).split('.')[0])
    with pytest.raises(ValueError):
        db = cuttle.home.Cuttle(
            'sqlame', db_name, 'localhost', 'test_user', 'test_pw')


def test_case_insensitive_sql_type():
    db_name = '_test_db_{}'.format(str(time.time()).split('.')[0])
    db = cuttle.home.Cuttle(
        'MYSQL', db_name, 'localhost', 'test_user', 'test_pw')
    expected = {
        'db': db_name,
        'host': 'localhost',
        'user': 'test_user',
        'passwd': 'test_pw'
    }
    assert expected['db'] == db.Model._config['db']
    assert expected['host'] == db.Model._config['host']
    assert expected['user'] == db.Model._config['user']
    assert expected['passwd'] == db.Model._config['passwd']
