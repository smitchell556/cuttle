# -*- coding: utf-8 -*-
"""

Test fixtures.

"""
import gc

import mysql.connector
import pytest

import cuttle.home
import cuttle.model
import cuttle.columns

import _helpers
import sql_db_config


# configuration values
# --------------------
@pytest.fixture()
def mysql_config():
    return sql_db_config.mysql_config


# object fixtures
# ---------------
@pytest.fixture()
def mysql_db_obj(mysql_config):
    db = cuttle.home.Cuttle(mysql_config['SQL_TYPE'],
                            mysql_config['DB'],
                            mysql_config['HOST'],
                            mysql_config['USER'],
                            mysql_config['PASSWD'])
    yield db
    del db
    _helpers._mysql_query(
        mysql_config,
        "DROP DATABASE IF EXISTS {}".format(mysql_config['DB']))


@pytest.fixture()
def db_and_model(mysql_db_obj):
    del_models(mysql_db_obj.Model.__subclasses__())
    gc.collect()

    class TestTable(mysql_db_obj.Model):
        columns = [
            cuttle.columns.Column('test_int_col',
                                  'INT',
                                  auto_increment=True,
                                  primary_key=True),
            cuttle.columns.Column('test_varchar_col', 'VARCHAR', maximum=16)
        ]
    yield mysql_db_obj, TestTable


@pytest.fixture()
def db_and_subclass(mysql_db_obj):
    del_models(mysql_db_obj.Model.__subclasses__())
    gc.collect()

    class EmptyModel(mysql_db_obj.Model):

        def __init__(self):
            super(EmptyModel, self).__init__()

        def foo(self):
            return 'foo'

    class NonEmptyModel(EmptyModel):

        def __init__(self):
            super(NonEmptyModel, self).__init__()

        columns = [
            cuttle.columns.IntColumn('test_int',
                                     auto_increment=True,
                                     primary_key=True)
        ]

    yield mysql_db_obj, NonEmptyModel


def del_models(models):
    for model in models:
        del_models(model.__subclasses__())
        del model
