# -*- coding: utf-8 -*-
"""

Tests that Model makes connection.

"""
import pytest

import _helpers


def test_explicit_connect(db_and_model):
    db, t_class = db_and_model
    db.create_db()

    t_obj = t_class()
    t_obj.connect()
    assert t_obj.con.is_connected()

    t_obj.close()
    assert t_obj.con == None

def test_with_connect(db_and_model):
    db, t_class = db_and_model
    db.create_db()

    with t_class() as t_obj:
        assert t_obj.con.is_connected()

def test_connect_twice_exception(db_and_model):
    db, t_class = db_and_model
    db.create_db()

    t_obj = t_class()
    t_obj.connect()
    with pytest.raises(RuntimeError):
        t_obj.connect()

    t_obj.close()

    with t_class() as t_obj:
        with pytest.raises(RuntimeError):
            t_obj.connect()

def test_set_con_error(db_and_model):
    db, t_class = db_and_model
    db.create_db()

    t_obj = t_class()

    with pytest.raises(AttributeError):
        t_obj.con = 'Please work'
