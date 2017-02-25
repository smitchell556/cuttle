# -*- coding: utf-8 -*-
"""

This module contains the Model class which is used to make querys on the
database.

"""
import _mysql_methods


class Model(object):
    """
    Model represents a table. It is used for querying the database. It is meant
    to be subclassed to create tables.

    :raises TypeError: Error caused by instantiating Model.

    :example: Model is used as a subclass like so:

              >>> from cuttle.home import Cuttle
              >>> db = Cuttle('mysql', 'test_db', 'localhost', 'squirtle', 'test_pw')
              >>> ExampleTable(db.Model):
              ...     columns = [IntField(name='example_column', serial=True),
              ...               TextField(name='example_text')]

              The `ExampleTable` can now be used for making queries (assuming
              the database has been created manually or with
              :func:`~cuttle.home.Cuttle.create_db`).

    :note: Model should not be instantiated. Treat it like an abstract base
           class.
    """
    #: Holds configuration values for database.
    _config = {}

    def __init__(self):
        if self.__class__.__name__ == 'Model':
            err_msg = 'Do not make an instance of Model, make a subclass.'
            raise TypeError(err_msg)
        self.query = []
        self.values = []

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
        Performs a SELECT query on the table associated with the model. If no
        arguments are supplied, all rows will be returned.

        :param \*args: Columns to select for as strings. If no columns provided,
                       all columns will be selected.

        :return: A list of tuples where each tuple is a row in the table.
        """
        self.check_columns(*args)
        self.query.append(self._sql_m()._select(self.name, *args))
        return self

    def insert(self, columns, values):
        """
        Performs an INSERT query on the table associated with the model.

        :param list columns: The columns to insert values into.
        :param list values: Values to be inserted into the table. They must be
                            in the same order as the columns. Expects a list
                            of tuples

        :note: If values are not ordered in the same sequence as columns, they
               wont be in the proper column in the database.
        """
        self.check_columns(*tuple(columns))
        q, vals = self._sql_m()._insert(self.name, columns, values)
        self.query.append(q)
        self.values.extend(vals)
        return self

    def update(self, **kwargs):
        """
        Performs an UPDATE query on the table associated with the model.

        :param dict \**kwargs: The values to be updated in the table where the
                               key is the column.

        :note: All key value pairs will be checked for *equality* in the WHERE
               clause.
        """
        self.check_columns(*tuple(key for key in kwargs.keys()))
        q, vals = self._sql_m()._update(self.name, **kwargs)
        self.query.append(q)
        self.values.append(vals)
        return self

    def delete(self):
        """
        Performs a DELETE query on the table associated with the model.
        """
        self.query.append(self._sql_m()._delete(self.name))
        return self

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

    def reset_query(self):
        """
        Resets query and values property on model.
        """
        self.query = []
        self.values = []

    def check_columns(self, *args):
        """
        Ensures columns exist on model before creating query string. Failing to
        check columns can result in sql injection.

        :param \*args: Columns to be checked against model.

        :raises ValueError: If parameters are not columns on model.
        """
        column_names = set(col.attributes['name']
                           for col in self._get_columns())
        input_columns = set(args)

        if not input_columns.issubset(column_names):
            miss_cols = ', '.join(list(input_columns - column_names))
            msg = ('Columns {} were not found on the Model. Be wary of SQL '
                   'injection.').format(miss_cols)
            raise ValueError(msg)

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
