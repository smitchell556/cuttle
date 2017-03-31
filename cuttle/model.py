# -*- coding: utf-8 -*-
"""

This module contains the Model class which is used to make querys on the
database.

"""
import warnings

import pymysql.cursors


LEGAL_COMPARISONS = [
    '=',
    '<=>',
    '>',
    '>=',
    '<',
    '<=',
    '!=',
    '<>',
]

LEGAL_CONDITIONS = [
    'AND',
    '&&',
    'OR',
    '||',
    'XOR'
]


class Model(object):
    """
    Model represents a table. It is used for querying the database. It is meant
    to be subclassed to create tables.

    :param bool validate_columns: Requires a validation check on all query
                                  methods that pass columns as parameters. If 
                                  raise_error_on_validation is false, no error
                                  will be raised, but the query method will not
                                  modify ``query`` or ``values`` on the object.
                                  Defaults to ``True``.
    :param bool raise_error_on_validation: Requires that an error is raised when
                                           a column fails validation. Defaults
                                           to ``True``. If validate_columns is
                                           false, no error will be raised.

    :raises TypeError: Error caused by instantiating Model.

    :example: Model is used as a subclass like so:

              >>> from cuttle.home import Cuttle
              >>> db = Cuttle('mysql', 'test_db', 'localhost', 'squirtle', 'test_pw')
              >>> ExampleTable(db.Model):
              ...     columns = [IntField(name='example_column', serial=True),
              ...                TextField(name='example_text')]

              The `ExampleTable` can now be used for making queries (assuming
              the database has been created manually or with
              :func:`~cuttle.home.Cuttle.create_db`).

    :note: Model should not be instantiated. Treat it like an abstract base
           class.
    """

    def __init__(self, validate_columns=True, raise_error_on_validation=True):
        #: Holds the connection to the database.
        self._connection = None
        #: Holds a cursor to the database.
        self._cursor = None
        #: Holds query to be executed as a list of strings.
        self._query = []
        #: Holds values to be inserted into query when executed.
        self._values = []
        self.validate_columns = validate_columns
        self.raise_error_on_validation = raise_error_on_validation
        # Copy connection_arguments dict to prevent changes made on this
        # instance from affecting all instances.
        self._connection_arguments = {
            k: v for k, v in self.connection_arguments.items()
        }

    def __del__(self):
        self.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def __iter__(self):
        return self.cursor.__iter__()

    @property
    def name(self):
        """
        Returns the table name which can be used for writing queries.
        """
        return type(self).__name__.lower()

    @property
    def connection_arguments(self):
        """
        Returns the connection arguments that are passed to the connection
        object.
        """
        return self._connection_arguments

    @property
    def connection(self):
        """
        Returns a connection to the database. Creates a connection if one hasn't
        already been made.

        Use :func:`~cuttle.home.Model.close` to close the connection.
        """
        try:
            self._connection.ping()
        except:
            self._connection = pymysql.connect(**self.connection_arguments)
        return self._connection

    @property
    def cursor(self):
        """
        Returns a cursor to the database. The cursor must be closed explicitly
        before a new one will be made.

        :note: A connection will automatically be made to the database before
               creating a cursor.
        """
        if self._cursor is None or self._cursor.connection is None:
            self._cursor = self.connection.cursor()
        return self._cursor

    @property
    def query(self):
        """
        Returns the current query string.
        """
        return ' '.join(self._query)

    @property
    def values(self):
        """
        Returns the values as a tuple.
        """
        return tuple(self._values)

    @property
    def seq_of_values(self):
        """
        Returns a sequence of values as tuples.
        """
        return [tuple(v) for v in self._values]

    @classmethod
    def _configure_model(cls, sql_type, **kwargs):
        """Configures the Model class to connect to the database."""
        cls._sql_type = sql_type.lower()
        if cls._sql_type == 'mysql':
            cls._connection_arguments = kwargs
        else:
            msg = "Please choose a valid sql extension"
            raise ValueError(msg)

    def _create_db(self):
        """
        Creates database and tables.
        """
        db_name = self.connection_arguments.pop('db')

        # Create database
        self._generate_db(db_name).execute()

        self.connection_arguments['db'] = db_name
        self.connection.select_db(db_name)

        # Create tables
        for tbl in _nested_subclasses(type(self)):
            if tbl.__dict__.get('columns', False):
                self._generate_table(tbl).execute()

        self.close()

    def _generate_db(self, db):
        """
        Genreates the create database statement.

        :param str db: The name of the database to create.
        """
        self.append_query('CREATE DATABASE IF NOT EXISTS {}'.format(db))
        return self

    def _generate_table(self, tbl):
        """
        Generates table schema.

        :param class tbl: A subclass of Model.
        """
        create_tbl = []
        # table names will be all lower case based on the name of the model
        tbl_name = tbl.__name__.lower()

        tbl_columns = tbl.columns

        create_tbl.append(
            'CREATE TABLE IF NOT EXISTS {} ('.format(tbl_name))

        p_key = None

        for column in tbl_columns:
            create_tbl.extend(self._generate_column(column))
            if column.attributes['primary_key']:
                p_key = column.attributes['name']

        if p_key is not None:
            create_tbl.append('PRIMARY KEY ({})'.format(p_key))
        if create_tbl[-1][-1] == ',':
            create_tbl[-1] = create_tbl[-1][:-1]

        create_tbl.append(')')

        self.append_query(' '.join(create_tbl))
        return self

    def _generate_column(self, column):
        """
        Generates column schema.

        :param obj column: A :class:`~cuttle.columns.Column` object.
        """
        attr = column.attributes

        create_col = [
            attr['name'].lower()
        ]

        # add attributes
        if attr['maximum'] is not None:
            create_col.append('{}({})'.format(
                attr['column_type'],
                attr['maximum']))
        elif attr['precision'] is not None:
            create_col.append('{}{}'.format(
                attr['column_type'],
                attr['precision']))
        else:
            create_col.append(attr['column_type'])
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

    def select(self, *args):
        """
        Adds a SELECT query on the table associated with the model. If no
        arguments are supplied, all rows will be returned.

        :param \*args: Columns to select for as strings. If no columns provided,
                       all columns will be selected.
        """
        if args:
            args = self.columns_lower(*args)
        if self.check_columns(*args):
            q = ['SELECT']
            if args:
                q.append(', '.join([c for c in args]))
            else:
                q.append('*')
            q.append('FROM {}'.format(self.name))
            self.append_query(' '.join(q))
        return self

    def insert(self, columns=[], values=[]):
        """
        Adds an INSERT query on the table associated with the model.

        :param list columns: The columns to insert values into.
        :param list values: Values to be inserted into the table. They must be
                            in the same order as the columns. Also accepts a
                            list of lists/tuples which would be used with
                            :func:`~cuttle.model.Model.executemany`.
        """
        if columns:
            columns = self.columns_lower(*tuple(columns))
        if self.check_columns(*columns):
            q = ['INSERT INTO {}'.format(self.name)]

            c = '({})'.format(', '.join(columns))
            q.append(c)
            q.append('VALUES')

            holder = '({})'.format(
                ', '.join(['%s' for __ in range(len(columns))]))
            q.append(holder)
            self.append_query(' '.join(q))
            self.extend_values(values)
        return self

    def update(self, **kwargs):
        """
        Adds an UPDATE query on the table associated with the model.

        :param dict \**kwargs: The values to be updated in the table where the
                               key is the column.

        """
        if not kwargs:
            raise ValueError('arguments required to update table')

        kwargs = self.columns_lower(**kwargs)
        if self.check_columns(*tuple(key for key in kwargs.keys())):
            columns, values = [], []
            for key, value in kwargs.items():
                columns.append(key)
                values.append(value)

            q = ['UPDATE {} SET'.format(self.name)]
            q.append(', '.join(['{}=%s'.format(column) for column in columns]))
            self.append_query(' '.join(q))
            self.extend_values(values)
        return self

    def delete(self):
        """
        Adds a DELETE query on the table associated with the model.
        """
        self.append_query('DELETE FROM {}'.format(self.name))
        return self

    def where(self, condition='AND', comparison='=', **kwargs):
        """
        Adds a WHERE clause to the query. The WHERE clause checks for equality.

        :param str condition: The conditional operator to use in the WHERE clause.
        :param str comparison: The comparison operator to use in the WHERE clause.
        :param \**kwargs: Key value pairs where the keys are the columns of the
                          table.

        :raises ValueError: If condition or comparison operator is invalid.
        """
        condition = condition.upper()
        comparison = comparison.upper()
        if condition not in LEGAL_CONDITIONS or comparison not in LEGAL_COMPARISONS:
            raise ValueError(
                'The conditional or comparison operator is not legal.')

        kwargs = self.columns_lower(**kwargs)
        if self.check_columns(*tuple(key for key in kwargs.keys())):
            columns, values = [], []
            for key, value in kwargs.iteritems():
                columns.append(key)
                values.append(value)

            q = []
            if 'WHERE' in self.query:
                q.append(condition)
            else:
                q.append('WHERE')

            q.append(' {} '.format(condition).join(['{}{}%s'.format(column, comparison)
                                                    for column in columns]))

            self.append_query(' '.join(q))
            self.extend_values(values)
        return self

    def execute(self, dict_cursor=False, unbuffered_cursor=False, commit=True):
        """
        Executes the query and returns the results (if any).

        :param bool dict_cursor: If true, results will be in a dict instead of
                                 a tuple. Defaults to ``False``.
        :param bool unbuffered_cursor: If true, uses an unbuffered cursor for
                                       queries. Defaults to ``False``.
        :param bool commit: Will commit the executed statement if ``True``.
                            Defaults to ``True``.

        :returns: The result of ``cursor.execute()``.

        :note: If both ``dict_cursor`` and ``unbuffered_cursor`` are ``True``,
               An unbuffered cursor will be used, and the results returned will
               be formatted as dictionaries.
        """
        if dict_cursor and unbuffered_cursor:
            self.connection.cursorclass = pymysql.cursors.SSDictCursor
        elif unbuffered_cursor:
            self.connection.cursorclass = pymysql.cursors.SSCursor
        elif dict_cursor:
            self.connection.cursorclass = pymysql.cursors.DictCursor
        else:
            self.connection.cursorclass = pymysql.cursors.Cursor

        result = self.cursor.execute(self.query, self.values)

        self.reset_query()

        if commit:
            self.commit()

        return result

    def executemany(self, dict_cursor=False, unbuffered_cursor=False, commit=True):
        """
        Executes the query with multiple values and returns the results (if any).

        :param bool dict_cursor: If true, results will be in a dict instead of
                                 a tuple. Defaults to ``False``.
        :param bool unbuffered_cursor: If true, uses an unbuffered cursor for
                                       queries. Defaults to ``False``.
        :param bool commit: Will commit the executed statement if ``True``.
                            Defaults to ``True``.

        :returns: The result of ``cursor.execute()``.

        :note: If both ``dict_cursor`` and ``unbuffered_cursor`` are ``True``,
               An unbuffered cursor will be used, and the results returned will
               be formatted as dictionaries.
        """
        if dict_cursor and unbuffered_cursor:
            self.connection.cursorclass = pymysql.cursors.SSDictCursor
        elif unbuffered_cursor:
            self.connection.cursorclass = pymysql.cursors.SSCursor
        elif dict_cursor:
            self.connection.cursorclass = pymysql.cursors.DictCursor
        else:
            self.connection.cursorclass = pymysql.cursors.Cursor

        result = self.cursor.executemany(self.query, self.seq_of_values)

        self.reset_query()

        if commit:
            self.commit()

        return result

    def fetchone(self):
        """
        Fetches the next row.
        """
        return self.cursor.fetchone()

    def fetchmany(self, size=None):
        """
        Fetches ``size`` number of rows or all if ``size`` is ``None``.

        :param int size: The number of rows to fetch. Defaults to ``None``.
        """
        return self.cursor.fetchmany(size)

    def fetchall(self):
        """
        Fetches all the rows in the cursor.

        :note: If the underlying cursor is unbuffered, PyMySQL's
               ``fetchall_unbuffered()`` is called.
        """
        if isinstance(self.cursor, pymysql.cursors.SSCursor):
            return self.cursor.fetchall_unbuffered()
        return self.cursor.fetchall()

    def commit(self):
        """
        Commits changes.
        """
        self.connection.commit()

    def rollback(self):
        """
        Rolls back the current transaction.
        """
        self.connection.rollback()

    def append_query(self, query):
        """
        Appends query string to current _query attribute.

        :param str query: A SQL query string.
        """
        self._query.append(query)

    def extend_values(self, values):
        """
        Extends _values with input values.

        :param list values: Values to be inserted into the query.
        """
        self._values.extend(values)

    def columns_lower(self, *args, **kwargs):
        """
        Converts columns to lowercase. Accepts both args and kwargs, but args
        take precedence for conversion. If both are passed as arguments, only
        converted args will be returned.

        :param \*args: Column names.
        :param \**kwargs: Pairs where the key is the column name.

        :raises ValueError: If no argument(s) are passed to the function.
        """
        if args:
            return tuple(arg.lower() for arg in args)
        elif kwargs:
            return {key.lower(): value for key, value in kwargs.items()}
        else:
            raise ValueError("columns_lower must receive input of either args "
                             "or kwargs")

    def check_columns(self, *args):
        """
        Ensures columns exist on model before creating query string. Failing to
        check columns can result in sql injection.

        :param \*args: Columns to be checked against model.

        :raises ValueError: If parameters are not columns on model.
        """
        column_names = set(col.attributes['name'].lower()
                           for col in self.columns)
        failed_columns = set(arg.lower() for arg in args) - column_names

        if self.validate_columns and failed_columns:
            msg = ('Columns {} were not found on the Model. Be wary of SQL '
                   'injection.').format(failed_columns)
            if self.raise_error_on_validation:
                raise ValueError(msg)
            else:
                warnings.warn(msg)
                return False
        return True

    def reset_query(self):
        """
        Resets query and values property on model.
        """
        self._query = []
        self._values = []

    def close(self):
        """
        Closes the database connection and cursor, if any.

        :note: If model is instantiated outside of a with block, it is recommended
               to explicitly call ``close()``.
        """
        self._close_cursor()
        self._close_connection()

    def _close_cursor(self):
        """
        Close the cursor, if any.
        """
        try:
            self._cursor.close()
        except:
            pass
        finally:
            self._cursor = None

    def _close_connection(self):
        """
        Close the connection, if any.
        """
        try:
            self._connection.close()
        except:
            pass


def _nested_subclasses(cls):
    """
    Creates a list of all nested subclasses.
    """
    return cls.__subclasses__() + [s for sc in cls.__subclasses__()
                                   for s in _nested_subclasses(sc)]
