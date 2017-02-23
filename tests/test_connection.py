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
    assert t_obj.connection.is_connected()

    t_obj.close()
    assert t_obj.connection is None


def test_with_connect(db_and_model):
    db, t_class = db_and_model
    db.create_db()

    with t_class() as t_obj:
        assert t_obj.connection.is_connected()
