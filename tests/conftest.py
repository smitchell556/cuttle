# -*- coding: utf-8 -*-
"""

Test fixtures.

"""
import gc

import pytest

import cuttle.home
import cuttle.model
import cuttle.columns


# object fixtures
# ---------------
@pytest.fixture()
def mysql_db_obj():
    db = cuttle.home.Cuttle('mysql',
                            db='fake_db',
                            host='localhost',
                            user='Ash',
                            passwd='squirtle_squad')
    yield db
    del db


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
            cuttle.columns.Column('test_varchar_col', 'VARCHAR', maximum=16),
            cuttle.columns.Column('test_varchar_col2', 'VARCHAR', maximum=32)
        ]
    yield mysql_db_obj, TestTable


@pytest.fixture()
def db_and_subclass(mysql_db_obj):
    del_models(mysql_db_obj.Model.__subclasses__())
    gc.collect()

    class EmptyModel(mysql_db_obj.Model):

        def foo(self):
            return 'foo'

    class NonEmptyModel(EmptyModel):
        columns = [
            cuttle.columns.IntColumn('test_int',
                                     auto_increment=True,
                                     primary_key=True)
        ]

    yield mysql_db_obj, EmptyModel, NonEmptyModel


def del_models(models):
    for model in models:
        del_models(model.__subclasses__())
        del model
