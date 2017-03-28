# -*- coding: utf-8 -*-
"""

Tests for creating database(s).

"""
from cuttle.reef import Cuttle
from cuttle.columns import Column


def test_mysql_create_db(db_and_model):
    db = db_and_model[0]

    db2 = Cuttle('mysql',
                 db='fake_db2',
                 host='localhost',
                 user='Ash',
                 passwd='squirtle_squad')

    class TestTable2(db2.Model):
        columns = [
            Column('test_int_col2',
                   'INT',
                   auto_increment=True,
                   primary_key=True),
            Column('test_varchar_col2', 'VARCHAR', maximum=16)
        ]

    exp_db = 'CREATE DATABASE IF NOT EXISTS fake_db'
    exp_schema = ('USE fake_db; CREATE TABLE IF NOT EXISTS testtable ( '
                  'test_int_col INT AUTO_INCREMENT, '
                  'test_varchar_col VARCHAR(16), '
                  'test_varchar_col2 VARCHAR(32), '
                  'PRIMARY KEY (test_int_col) );')

    exp_db2 = 'CREATE DATABASE IF NOT EXISTS fake_db2'
    exp_schema2 = ('USE fake_db2; CREATE TABLE IF NOT EXISTS testtable2 ( '
                   'test_int_col2 INT AUTO_INCREMENT, '
                   'test_varchar_col2 VARCHAR(16), '
                   'PRIMARY KEY (test_int_col2) );')

    db_name = db.Model._get_config()['connection_arguments']['db']

    res_db = db.Model._generate_db(db_name)
    res_schema = db.Model._generate_table_schema(db_name)

    db_name = db2.Model._get_config()['connection_arguments']['db']

    res_db2 = db2.Model._generate_db(db_name)
    res_schema2 = db2.Model._generate_table_schema(db_name)

    assert res_db == exp_db
    assert res_schema == exp_schema

    assert res_db2 == exp_db2
    assert res_schema2 == exp_schema2
