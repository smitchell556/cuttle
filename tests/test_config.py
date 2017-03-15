# -*- coding: utf-8 -*-
"""

Tests for configuring Cuttle.

"""
import time

import pytest

import cuttle.reef


def test_config_values():
    expected = {
        'db': '_test_db',
        'host': 'localhost',
        'user': 'test_user',
        'passwd': 'test_pw'
    }
    db = cuttle.reef.Cuttle(
        'mysql', **expected)
    assert expected == db.Model._config['connection_arguments']


def test_invalid_sql():
    con_kwargs = {
        'db': '_test_db',
        'host': 'localhost',
        'user': 'test_user',
        'passwd': 'test_pw'
    }
    with pytest.raises(ValueError):
        db = cuttle.reef.Cuttle(
            'sqlame', **con_kwargs)


def test_case_insensitive_sql_type():
    expected = {
        'db': '_test_db',
        'host': 'localhost',
        'user': 'test_user',
        'passwd': 'test_pw'
    }
    db = cuttle.reef.Cuttle(
        'MYSQL', **expected)
    assert expected == db.Model._config['connection_arguments']


def test_no_db_arg():
    con_kwargs = {
        'host': 'localhost',
        'user': 'test_user',
        'passwd': 'test_pw'
    }
    with pytest.raises(ValueError):
        db = cuttle.reef.Cuttle(
            'mysql', **con_kwargs)
