# -*- coding: utf-8 -*-
"""

This module contains database methods for performing queries in MySQL.

"""
import pymysql.cursors

import _db_helpers


def _create_db(cls):
    """
    Creates database and tables.

    :param cls: Expects the Model class.
    """
    db_config = cls._get_config()
    tbl_classes = _db_helpers._nested_subclasses(cls)

    # Generate sql statements
    create_db = _create_db(db_config['DB'])
    create_tbls = _generate_table_schema(db_config['DB'], tbl_classes)

    con = pymysql.connect(host=db_config['HOST'],
                          user=db_config['USER'],
                          passwd=db_config['PASSWD'])
    cur = con.cursor()
    cur.execute(create_db)
    cur.execute(create_tbls)
    cur.close()
    con.close()


def _generate_db(db):
    """
    Genreates the create database statement.
    """
    create_db = 'CREATE DATABASE IF NOT EXISTS {}'.format(db)
    return create_db


def _generate_table_schema(db, tbl_classes):
    """
    Generates table schema.
    """
    create_tbls = ['USE {};'.format(db)]

    # construct table schema from tbl_classes columns list
    for tbl in tbl_classes:
        # table names will be all lower case based on the name of the model
        tbl_name = tbl.__name__.lower()

        if not hasattr(tbl, 'columns'):
            continue

        tbl_columns = tbl._get_columns()

        create_tbls.append('CREATE TABLE IF NOT EXISTS {} ('.format(tbl_name))
        p_key = None

        for column in tbl_columns:
            create_tbls.extend(_generate_column_schema(column))
            if column.attributes['primary_key']:
                p_key = column.attributes['name']

        if p_key is not None:
            create_tbls.append('PRIMARY KEY ({})'.format(p_key))
        if create_tbls[-1][-1] == ',':
            create_tbls[-1] = create_tbls[-1][:-1]

        create_tbls.append(');')

    create_tbls = ' '.join(create_tbls)

    return create_tbls


def _generate_column_schema(column):
    """
    Generates column schema.
    """
    attr = column.attributes

    create_col = [
        attr['name'].lower()
    ]

    # add attributes
    if attr['maximum'] is not None:
        create_col.append('{}({})'.format(
            attr['data_type'],
            attr['maximum']))
    elif attr['precision'] is not None:
        create_col.append('{}{}'.format(
            attr['data_type'],
            attr['precision']))
    else:
        create_col.append(attr['data_type'])
    if attr['required']:
        create_col.append('NOT NULL')
    if attr['unique']:
        create_col.append('UNIQUE')
    if attr['auto_increment']:
        create_col.append('AUTO_INCREMENT')
    if attr['default'] is not None:
        create_col.append(
            'DEFAULT {}'.format(attr['default']))
    if attr['update'] is not None:
        create_col.append(
            'ON UPDATE {}'.format(attr['update']))
    create_col[-1] += ','

    return create_col


def _make_con(db_config):
    """
    Creates connection to db.
    """
    return pymysql.connect(host=db_config['HOST'],
                           user=db_config['USER'],
                           passwd=db_config['PASSWD'],
                           db=db_config['DB'])


def _select(model, *args):
    """
    Generates SELECT statement.
    """
    q = ['SELECT']
    if args:
        q.append(', '.join([c for c in args]))
    else:
        q.append('*')
    q.append('FROM {}'.format(model.name))
    return ' '.join(q)


def _insert(model, columns, values):
    """
    Generates INSERT statement.
    """
    q = ['INSERT INTO {}'.format(model.name)]

    c = '({})'.format(', '.join(columns))
    q.append(c)
    q.append('VALUES')

    holder = '({})'.format(
        ', '.join(['%s' for __ in range(len(values))]))
    q.append(holder)
    return ' '.join(q), values


def _update(model, **kwargs):
    """
    Generates UPDATE statement.
    """
    columns, values = [], []
    for key, value in kwargs.iteritems():
        columns.append(key)
        values.append(value)

    q = ['UPDATE {} SET'.format(model.name)]
    q.append(', '.join(['{}=%s'.format(column) for column in columns]))
    return ' '.join(q), values


def _delete(model):
    """
    Generates DELETE statement.
    """
    return 'DELETE FROM {}'.format(model.name)


def _where(model, condition, comparison, **kwargs):
    """
    Generates WHERE statement.
    """
    columns, values = [], []
    for key, value in kwargs.iteritems():
        columns.append(key)
        values.append(value)

    q = []
    if 'WHERE' in model.query:
        q.append(condition)
    else:
        q.append('WHERE')

    q.append(' {} '.format(condition).join(['{}{}%s'.format(column, comparison)
                                            for column in columns]))
    return ' '.join(q), values


def _execute(model):
    """
    Executes a query and returns the results (if any).
    """
    cursor = model.cursor()
    cursor.execute(model.query, model.values)
    result = cursor.fetchall()
    model.connection.commit()
    cursor.close()
    return result
