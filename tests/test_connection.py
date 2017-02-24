# -*- coding: utf-8 -*-
"""

Tests that Model makes connection.

"""
import pymysql
import pytest


def test_explicit_connect(db_and_model):
    db, t_class = db_and_model
    db.create_db()

    t_obj = t_class()
    t_obj.connect()
    assert type(t_obj.connection) == pymysql.connections.Connection

    t_obj.close()
    assert t_obj.connection is None


def test_with_connect(db_and_model):
    db, t_class = db_and_model
    db.create_db()

    with t_class() as t_obj:
        assert type(t_obj.connection) == pymysql.connections.Connection
