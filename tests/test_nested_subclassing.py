# -*- coding: utf-8 -*-
"""

Tests for configuring Cuttle.

"""
from cuttle.model import _nested_subclasses


def test_nested_subclass_table_generation(db_and_subclass):
    db, e_class, ne_class = db_and_subclass

    exp_models = [e_class, ne_class]

    res_models = _nested_subclasses(db.Model)

    assert res_models == exp_models
