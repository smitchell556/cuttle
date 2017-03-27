# -*- coding: utf-8 -*-
"""

Tests abstract base class implementation of Model.

"""
import pytest


def test_check_columns(db_and_model):
    db = db_and_model[0]

    with pytest.raises(TypeError):
        model = db.Model()
