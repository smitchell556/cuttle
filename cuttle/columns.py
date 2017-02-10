# -*- coding: utf-8 -*-
"""

This module contains the Column base class and subsequent derived classes
for specifying table columns.

"""
import datetime
import sys


class Column(object):
    """
    The Column class is the base class for representing a column in a table.

    :param name: Name of column.
    :param data_type: Data type of column.
    :param maximum: Maximum character count. Defaults to
                    ``None``.
    :param precision: Sets precision of decimal in form (M, D) where M is the
                      number of significant digits and D represents the number
                      of digits after the decimal point. Expects a tuple. M is
                      required, but D is optional.
                      Defaults to ``None``.
    :param required: Ensures column must contain a value. Defaults to ``False``.
    :param default: Sets default value of column on INSERT queries. Defaults to
                    ``None``.
    :param update: Sets default value of column on UPDATE queries. Defaults to
                   ``None``.
    :param unique: Requires values entered into column are unique. Defaults to
                   ``False``.
    :param auto_increment: Auto increments value of column on INSERT queries.
                           Defaults to ``False``.

    :raises: ValueError: If both maximum and precision is set. If value at index
                         1 of precision is greater than value at index 0.

    :note: If an attribute is not specified, then the default of the SQL
           implementation will be used. 
    """
    def __init__(self, name, data_type, maximum=None, precision=None,
                 decimal_precision=None, required=False, unique=False,
                 auto_increment=False, default=None, update=None, 
                 primary_key=False):
        # ensure maximum and precision are not set at the same time.
        # the column can have a max character count or precision (if decimal),
        # but it cannot have both.
        if maximum is not None and precision is not None:
            err_msg = 'maximum and precision cannot be set at the same time'
            raise ValueError(err_msg)

        # ensure proper precision values. D cannot be greater than M.
        if precision is not None and precision[1] > precision[0]:
            err_msg = 'precision must be formatted (M, D) where M >= D'
            raise ValueError(err_msg)

        #: Contains values specifying column parameters.
        self.attributes = {
            'name': name,
            'data_type': data_type,
            'maximum': maximum,
            'precision': precision,
            'required': required,
            'unique': unique,
            'auto_increment': auto_increment,
            'default': default,
            'update': update,
            'primary_key': primary_key
        }


class IntColumn(Column):
    """
    Represents an int column in database.

    :param name: Name of column.
    :param \**kwargs: Column parameters. Check :class:`~cuttle.columns.Column`
                      for acceptable arguments.
    """
    def __init__(self, name, **kwargs):
        super(IntColumn, self).__init__(name, 'INT', **kwargs)


class DecimalColumn(Column):
    """
    Represents a decimal column in database.

    :param name: Name of column.
    :param \**kwargs: Column parameters. Check :class:`~cuttle.columns.Column`
                      for acceptable arguments.
    """
    def __init__(self, name, **kwargs):
        super(DecimalColumn, self).__init__(name, 'DECIMAL', **kwargs)


class TextColumn(Column):
    """
    Represents a text column in database.

    :param name: Name of column.
    :param \**kwargs: Column parameters. Check :class:`~cuttle.columns.Column`
                      for acceptable arguments.
    """
    def __init__(self, name, **kwargs):
        super(TextColumn, self).__init__(name, 'VARCHAR', **kwargs)


class DateColumn(Column):
    """
    Represents a date column in database.

    :param name: Name of column.
    :param \**kwargs: Column parameters. Check :class:`~cuttle.columns.Column`
                      for acceptable arguments.
    """
    def __init__(self, name, **kwargs):
        super(DateColumn, self).__init__(name, 'DATE', **kwargs)


class DateTimeColumn(Column):
    """
    Represents a datetime column in database.

    :param name: Name of column.
    :param \**kwargs: Column parameters. Check :class:`~cuttle.columns.Column`
                      for acceptable arguments.
    """
    def __init__(self, name, **kwargs):
        super(DateTimeColumn, self).__init__(name, 'DATETIME', **kwargs)
