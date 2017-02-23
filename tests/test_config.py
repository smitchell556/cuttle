# -*- coding: utf-8 -*-
"""

Tests for configuring Cuttle.

"""
import time

import pytest

import cuttle.home
import cuttle._mysql_methods


def test_config_values():
    db_name = '_test_db_{}'.format(str(time.time()).split('.')[0])
    db = cuttle.home.Cuttle(
        'mysql', db_name, 'localhost', 'test_user', 'test_pw')
    expected = {
        'DB': db_name,
        'HOST': 'localhost',
        'USER': 'test_user',
        'PASSWD': 'test_pw'
    }
    assert expected['DB'] == db.Model._config['DB']
    assert expected['HOST'] == db.Model._config['HOST']
    assert expected['USER'] == db.Model._config['USER']
    assert expected['PASSWD'] == db.Model._config['PASSWD']


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
        'DB': db_name,
        'HOST': 'localhost',
        'USER': 'test_user',
        'PASSWD': 'test_pw'
    }
    assert cuttle._mysql_methods == db.Model._config['SQL_METHODS']
    assert expected['DB'] == db.Model._config['DB']
    assert expected['HOST'] == db.Model._config['HOST']
    assert expected['USER'] == db.Model._config['USER']
    assert expected['PASSWD'] == db.Model._config['PASSWD']
