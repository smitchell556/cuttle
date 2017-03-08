# -*- coding: utf-8 -*-
"""

This module contains the Model class which is used to make querys on the
database.

"""
import warnings

import _mysql_methods


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
    #: Holds configuration values for database.
    _config = {}

    def __init__(self, validate_columns=True, raise_error_on_validation=True):
        if self.__class__.__name__ == 'Model':
            err_msg = 'Do not make an instance of Model, make a subclass.'
            raise TypeError(err_msg)
        #: Holds query to be executed as a list of strings.
        self._query = []
        #: Holds values to be inserted into query when executed.
        self._values = []
        self.validate_columns = validate_columns
        self.raise_error_on_validation = raise_error_on_validation

    def __del__(self):
        self.close()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    @classmethod
    def _configure_model(cls, sql_type, db, host, user, passwd):
        """Configures the Model class to connect to the database."""
        if sql_type.lower() == 'mysql':
            cls._config['SQL_METHODS'] = _mysql_methods
            cls._config['DB'] = db
            cls._config['HOST'] = host
            cls._config['USER'] = user
            cls._config['PASSWD'] = passwd
        else:
            msg = "Please choose a valid sql extension"
            raise ValueError(msg)

    @classmethod
    def _get_config(cls):
        """
        Gets config dict.
        """
        return cls._config

    @classmethod
    def _get_columns(cls):
        """
        Gets Column objects of class.
        """
        return cls.columns

    @classmethod
    def _sql_m(cls):
        """
        Gets methods for specified sql implementation.
        """
        return cls._config['SQL_METHODS']

    @classmethod
    def _create_db(cls):
        """
        Creates database for specified sql implementation.
        """
        cls._sql_m()._create_db(cls)

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
            self.append_query(self._sql_m()._select(self.name, *args))
        return self

    def insert(self, columns, values):
        """
        Adds an INSERT query on the table associated with the model.

        :param list columns: The columns to insert values into.
        :param list values: Values to be inserted into the table. They must be
                            in the same order as the columns.

        :note: This only inserts a single entry into the database.
        """
        columns = self.columns_lower(*tuple(columns))
        if self.check_columns(*columns):
            q, vals = self._sql_m()._insert(self.name, columns, values)
            self.append_query(q)
            self.extend_values(vals)
        return self

    def update(self, **kwargs):
        """
        Adds an UPDATE query on the table associated with the model.

        :param dict \**kwargs: The values to be updated in the table where the
                               key is the column.

        """
        kwargs = self.columns_lower(**kwargs)
        if self.check_columns(*tuple(key for key in kwargs.keys())):
            q, vals = self._sql_m()._update(self.name, **kwargs)
            self.append_query(q)
            self.extend_values(vals)
        return self

    def delete(self):
        """
        Adds a DELETE query on the table associated with the model.
        """
        self.append_query(self._sql_m()._delete(self.name))
        return self

    def where(self, **kwargs):
        """
        Adds a WHERE clause to the query. The WHERE clause checks for equality.

        :param \**kwargs: Key value pairs where the keys are the columns of the
                          table.
        """
        kwargs = self.columns_lower(**kwargs)
        if self.check_columns(*tuple(key for key in kwargs.keys())):
            q, vals = self._sql_m()._where(self.name, **kwargs)
            self.append_query(q)
            self.extend_values(vals)
        return self

    def execute(self):
        """
        Executes the query and returns the results (if any).

        :returns: A tuple of tuples. Where each inner tuple represents a
                  column.
        """
        result = self._sql_m()._execute(self)
        self.reset_query()
        return result

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
            return {key.lower(): value for key, value in kwargs.iteritems()}
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
                           for col in self._get_columns())
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

    def connect(self):
        """
        Connects the model to the database.

        :note: If model is instantiated outside of a with block, the
               ``connect()`` method must be explicitly called before
               performing any queries.
        """
        self.close()
        self._connection = self._sql_m()._make_con(self._get_config())

    def close(self):
        """
        Closes the database connection.

        :note: If model is instantiated outside of a with block, the ``close()``
               method must be explicitly called.
        """
        try:
            self.connection.close()
        except:
            pass
        finally:
            self._connection = None

    def cursor(self, **kwargs):
        """
        Returns a cursor. Requires instance to be connected to the database
        first.

        :param \**kwargs: Type(s) of cursor to use as boolean values.

        :note: It is the caller's responsibility to close the cursor.
        """
        if kwargs:
            return self.connection.cursor(**kwargs)
        try:
            return self.connection.cursor(**self._cursor_properties)
        except:
            return self.connection.cursor()

    def cursor_properties(self, **kwargs):
        """
        Sets type of cursor to use.

        :param \**kwargs: Type(s) of cursor to use as boolean values.
        """
        self._cursor_properties = kwargs

    @property
    def name(self):
        """
        Returns the table name which can be used for writing queries.
        """
        return type(self).__name__.lower()

    @property
    def connection(self):
        """
        Returns a connection to the database.
        """
        try:
            return self._connection
        except:
            self._connection = None
        return self._connection

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
