# -*- coding: utf-8 -*-
"""

Tests the check_columns method.

"""
import pytest


def test_check_columns(db_and_model):
    t_class = db_and_model[1]

    t_obj1 = t_class()

    assert t_obj1.check_columns('test_int_col')

    with pytest.raises(ValueError):
        t_obj1.check_columns('test_int_col', 'test_wrong_col')

    t_obj2 = t_class(validate_columns=True, raise_error_on_validation=False)
    assert not t_obj2.check_columns('test_int_col', 'test_wrong_col')

    t_obj3 = t_class(False)
    assert t_obj3.check_columns('test_int_col', 'test_wrong_col')
