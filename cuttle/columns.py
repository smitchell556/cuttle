# -*- coding: utf-8 -*-
"""
This module contains the Column class for specifying table columns.

:license: MIT, see LICENSE for details.
"""
import decimal


INTEGER_TYPES = [
    'INTEGER',
    'INT',
    'SMALLINT',
    'TINYINT',
    'MEDIUMINT',
    'BIGINT'
]

FIXED_POINT_TYPES = [
    'DECIMAL',
    'NUMERIC'
]

FLOATING_POINT_TYPES = [
    'FLOAT',
    'DOUBLE'
]

STRING_TYPES = [
    'CHAR',
    'VARCHAR',
    'BINARY',
    'VARBINARY',
    'BLOB',
    'TEXT',
    'ENUM',
    'SET'
]


class Column(object):
    """
    The Column class is the base class for representing a column in a table.

    :param name: Name of column.
    :param column_type: Data type of column.
    :param maximum: Maximum character count. Defaults to
                    ``None``.
    :param tuple precision: Sets precision of decimal in form (M, D) where M
                            is the number of significant digits and D
                            represents the number of digits after the decimal
                            point. Expects a tuple. Defaults to ``None``.
    :param bool required: Ensures column must contain a value. Defaults to
                          ``False``.
    :param default: Sets default value of column on INSERT queries.
                    Defaults to ``None``.
    :param update: Sets default value of column on UPDATE queries.
                   Defaults to ``None``.
    :param bool unique: Requires values entered into column are unique.
                        Defaults to ``False``.
    :param bool auto_increment: Auto increments value of column on INSERT
                                queries. Defaults to ``False``.
    :param bool primary_key: Signifies column as primary key of table.
                             Defaults to ``False``.
    """

    def __init__(self, name, column_type, maximum=None, precision=None,
                 required=False, unique=False, auto_increment=False,
                 default=None, update=None, primary_key=False):
        #: Contains values specifying column parameters.
        self._attributes = dict(
            name=name.lower(),
            column_type=column_type.upper(),
            maximum=maximum,
            precision=precision,
            required=required,
            unique=unique,
            auto_increment=auto_increment,
            default=self._format_default(column_type, default),
            update=update,
            primary_key=primary_key
        )

    @property
    def name(self):
        """
        Returns the name of the column in lower case.
        """
        return self._attributes['name']

    def _format_default(self, column_type, default):
        """
        Formats ``default`` input if string type.
        """
        if default is not None:
            if column_type in INTEGER_TYPES:
                default = int(default)
            elif column_type in FIXED_POINT_TYPES:
                default = decimal.Decimal(str(default))
            elif column_type in FLOATING_POINT_TYPES:
                default = float(default)
            elif column_type in STRING_TYPES:
                default = "'{}'".format(default)

        return default

    def _column_schema(self):
        """
        Generates column schema.
        """
        create_col = [self.name]

        # add attributes
        if self._attributes['maximum'] is not None:
            create_col.append('{}({})'.format(
                self._attributes['column_type'],
                self._attributes['maximum']))
        elif self._attributes['precision'] is not None:
            create_col.append('{}{}'.format(
                self._attributes['column_type'],
                self._attributes['precision']))
        else:
            create_col.append(self._attributes['column_type'])

        if self._attributes['required']:
            create_col.append('NOT NULL')
        if self._attributes['unique']:
            create_col.append('UNIQUE')
        if self._attributes['auto_increment']:
            create_col.append('AUTO_INCREMENT')
        if self._attributes['default'] is not None:
            create_col.append(
                'DEFAULT {}'.format(self._attributes['default']))
        if self._attributes['update'] is not None:
            create_col.append(
                'ON UPDATE {}'.format(self._attributes['update']))
        if self._attributes['primary_key']:
            create_col.append('PRIMARY KEY')

        create_col[-1] += ',\n'

        return ' '.join(create_col)
