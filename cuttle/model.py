# -*- coding: utf-8 -*-
"""
This module contains the Model class which is used to make querys on the
database.

:license: MIT, see LICENSE for details.
"""
import warnings

from cuttlepool import CuttlePool


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
    ``Model`` represents a table. It is used for querying the database. It is
    meant to be subclassed to create tables.

    :param obj transaction: A ``Transaction`` object which will bundle all
                            executed SQL statements into one transaction.
    :param bool validate_columns: Requires a validation check on all query
                                  methods that pass columns as parameters.
                                  If raise_error_on_validation is false, no
                                  error will be raised, but the query method
                                  will not modify ``query`` or ``values`` on
                                  the object. Defaults to ``True``.
    :param bool raise_error_on_validation: Requires that an error is raised
                                           when a column fails validation.
                                           Defaults to ``True``. If
                                           validate_columns is false, no error
                                           will be raised.

    :raises TypeError: Error caused by instantiating Model.
    """

    def __init__(self, transaction=None, validate_columns=True, raise_error_on_validation=True):
        #: Holds the connection to the database.
        self._connection = None
        #: Holds a cursor to the database.
        self._cursor = None
        #: Holds query to be executed as a list of strings.
        self._query = []
        #: Holds values to be inserted into query when executed.
        self._values = []

        self._transaction = transaction
        self.validate_columns = validate_columns
        self.raise_error_on_validation = raise_error_on_validation

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
        Returns the connection arguments used by the underlying connection
        driver.
        """
        return self._pool.connection_arguments

    @property
    def connection(self):
        """
        Returns a connection to the database. Gets a connection from the
        connection pool if it doesn't already have one.

        :note: Use :func:`~cuttle.home.Model.close` to close the connection.
               :func:`~cuttle.home.Model.close` is not necessary if using the
               ``Model`` object as a context manager.
        """
        try:
            self._connection.ping()
        except:
            self._connection = self._pool.get_connection()
        return self._connection

    @property
    def cursor(self):
        """
        Returns a cursor to the database. The cursor must be closed explicitly
        before a new one will be made.

        :note: A connection will automatically be made to the database before
               creating a cursor.
        """
        if self._transaction is not None:
            return self._transaction._cursor

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
    def _configure(cls, sql_type, **kwargs):
        """
        Configures the Model class to connect to the database.

        :param str sql_type: The SQL implementation to use.
        :param \**kwargs: Connection arguments to be used by the underlying
                          connection object.

        :raises ValueError: If improper sql_type parameter.
        """
        cls._sql_type = sql_type.lower()
        if cls._sql_type == 'mysql':
            from pymysql import connect

            # add ping method to pool
            class Pool(CuttlePool):

                def ping(self, connection):
                    try:
                        connection.ping()
                    except Exception:
                        pass
                    return connection.open

        else:
            msg = "Please choose a valid sql extension"
            raise ValueError(msg)

        cls._pool = Pool(connect, **kwargs)

    def _create_table(self):
        """
        Generates table schema.

        :raises AttributeError: If table has multiple primary keys.
        """
        create_tbl = []

        create_tbl.append(
            'CREATE TABLE IF NOT EXISTS {} (\n'.format(self.name))

        for column in self.columns:
            create_tbl.append(column._column_schema())

        create_tbl[-1] = create_tbl[-1].replace(',', '')

        create_tbl.append(')')

        self.append_query(''.join(create_tbl))
        return self

    def select(self, *args):
        """
        Adds a SELECT query on the table associated with the model. If no
        arguments are supplied, all rows will be returned.

        :param \*args: Columns to select for as strings. If no columns
                       provided, all columns will be selected.
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

        :raises ValueError: If no column value pairs passed in.
        """
        if not kwargs:
            raise ValueError('column value pairs required to update table')

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

        :param str condition: The conditional operator to use in the WHERE
                              clause.
        :param str comparison: The comparison operator to use in the WHERE
                               clause.
        :param \**kwargs: Key value pairs where the keys are the columns of the
                          table.

        :raises ValueError: If condition or comparison operator is invalid. If
                            no column value pairs passed in.
        """
        if not kwargs:
            raise ValueError('column value pairs required for WHERE clause')

        condition = condition.upper()
        comparison = comparison.upper()
        if condition not in LEGAL_CONDITIONS or comparison not in LEGAL_COMPARISONS:
            raise ValueError(
                'The conditional or comparison operator is not legal.')

        kwargs = self.columns_lower(**kwargs)
        if self.check_columns(*tuple(key for key in kwargs.keys())):
            columns, values = [], []
            for key, value in kwargs.items():
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

    def execute(self, commit=False):
        """
        Executes the query and returns the results (if any). If a

        :param bool commit: Will commit the executed statement if ``True``.
                            Defaults to ``False``.

        :returns: The result of ``cursor.execute()``.
        """
        result = self.cursor.execute(self.query, self.values)

        self.reset_query()

        if commit:
            self.commit()

        return result

    def executemany(self, commit=False):
        """
        Executes the query with multiple values and returns the results (if any).

        :param bool commit: Will commit the executed statement if ``True``.
                            Defaults to ``False``.

        :returns: The result of ``cursor.execute()``.
        """
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
        """
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
        column_names = set(col._attributes['name'].lower()
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

        :note: If model is instantiated outside of a with block, it is
               recommended to explicitly call ``close()``.
        """
        self._close_connection()

    def _close_cursor(self):
        """
        Close the cursor, if any.
        """
        try:
            self._cursor.close()
        except Exception:
            pass
        finally:
            self._cursor = None

    def _close_connection(self):
        """
        Close the connection, if any.
        """
        self._close_cursor()

        try:
            self._connection.close()
        except Exception:
            pass
        finally:
            self._connection = None
