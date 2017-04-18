# -*- coding: utf-8 -*-
"""
This module contains the Column class for specifying table columns.

:license: MIT, see LICENSE for details.
"""


class Column(object):
    """
    The Column class is the base class for representing a column in a table.

    :param name: Name of column.
    :param column_type: Data type of column.
    :param maximum: Maximum character count. Defaults to
                    ``None``.
    :param precision: Sets precision of decimal in form (M, D) where M is the
                      number of significant digits and D represents the number
                      of digits after the decimal point. Expects a tuple.
                      Defaults to ``None``.
    :param required: Ensures column must contain a value. Defaults to ``False``.
    :param default: Sets default value of column on INSERT queries. Defaults to
                    ``None``. If default is supposed to be a string in the
                    database, the quotes must be included like "'default'".
    :param update: Sets default value of column on UPDATE queries. Defaults to
                   ``None``. If update is supposed to be a string in the
                   database, the quotes must be included like "'update'".
    :param unique: Requires values entered into column are unique. Defaults to
                   ``False``.
    :param auto_increment: Auto increments value of column on INSERT queries.
                           Defaults to ``False``.
    :param primary_key: Signifies column as primary key of table. Defaults to
                        ``False``.

    :note: If an attribute is not specified, then the default of the SQL
           implementation will be used.
    """

    def __init__(self, name, column_type, maximum=None, precision=None,
                 required=False, unique=False, auto_increment=False,
                 default=None, update=None, primary_key=False):

        #: Contains values specifying column parameters.
        self.attributes = dict(
            name=name.lower(),
            column_type=column_type.upper(),
            maximum=maximum,
            precision=precision,
            required=required,
            unique=unique,
            auto_increment=auto_increment,
            default=default,
            update=update,
            primary_key=primary_key
        )

    @property
    def name(self):
        """
        Returns the name of the column in lower case.
        """
        return self.attributes['name']

    @property
    def primary_key(self):
        """
        Returns a bool indicating if column is a primary key.
        """
        return self.attributes['primary_key']

    def column_schema(self):
        """
        Generates column schema.
        """
        create_col = [self.name]

        # add attributes
        if self.attributes['maximum'] is not None:
            create_col.append('{}({})'.format(
                self.attributes['column_type'],
                self.attributes['maximum']))
        elif self.attributes['precision'] is not None:
            create_col.append('{}{}'.format(
                self.attributes['column_type'],
                self.attributes['precision']))
        else:
            create_col.append(self.attributes['column_type'])
        if self.attributes['required']:
            create_col.append('NOT NULL')
        if self.attributes['unique']:
            create_col.append('UNIQUE')
        if self.attributes['auto_increment']:
            create_col.append('AUTO_INCREMENT')
        if self.attributes['default'] is not None:
            create_col.append(
                'DEFAULT {}'.format(self.attributes['default']))
        if self.attributes['update'] is not None:
            create_col.append(
                'ON UPDATE {}'.format(self.attributes['update']))
        if self.primary_key:
            create_col.append('PRIMARY KEY')
        create_col[-1] += ',\n'

        return ' '.join(create_col)
