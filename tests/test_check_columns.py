# -*- coding: utf-8 -*-
"""

Tests the check_columns method.

"""
import pytest


def test_check_columns(db_and_model):
    t_class = db_and_model[1]

    t_obj = t_class()

    assert t_obj.check_columns('test_int_col')

    with pytest.raises(ValueError):
        t_obj.check_columns('test_int_col', 'test_wrong_col')
