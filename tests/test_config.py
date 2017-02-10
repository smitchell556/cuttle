# -*- coding: utf-8 -*-
"""

Tests for configuring Cuttle.

"""
import pytest

import cuttle.home


def test_config_values():
    db = cuttle.home.Cuttle('mysql|test_db|localhost|test_user|test_pw')
    expected = {
        'DB': 'test_db',
        'HOST': 'localhost',
        'USER': 'test_user',
        'PASSWD': 'test_pw'
    }
    assert expected['DB'] == db.Model._config['DB']
    assert expected['HOST'] == db.Model._config['HOST']
    assert expected['USER'] == db.Model._config['USER']
    assert expected['PASSWD'] == db.Model._config['PASSWD']

def test_short_config():
    with pytest.raises(ValueError):
        db = cuttle.home.Cuttle('sql|test_db|localhost|test_user')

def test_long_config():
    with pytest.raises(ValueError):
        db = cuttle.home.Cuttle('sql|test_db|localhost|test_user|test_pw|idk')

def test_invalid_sql():
    with pytest.raises(ValueError):
        db = cuttle.home.Cuttle('sqlame|test_db|localhost|test_user|test_pw')
