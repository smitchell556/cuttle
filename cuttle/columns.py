# -*- coding: utf-8 -*-
"""
This module contains the Column class for specifying table columns.

:license: MIT, see LICENSE for details.
"""


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

    :raises TypeError: If either ``name``, ``column_type``, and ``schema`` is
                       ``None`` *or* ``schema`` is ``None`` and ``name`` or
                       ``column_type`` is ``None``.
    """

    def __init__(self, name, column_type, maximum=None, precision=None,
                 required=False, unique=False, auto_increment=False,
                 default=None, update=None, primary_key=False):
        try:
            #: Contains values specifying column parameters.
            self.attributes = dict(
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

        except:
            self._schema_to_column(schema)

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

    def _format_default(self, column_type, default):
        """
        Formats ``default`` input if string type.
        """
        if default and column_type in STRING_TYPES:
            default = "'{}'".format(default)

        return default

    def _schema_to_column(self, schema):
        """
        Converts column schema to ``Column`` object.

        :param tuple schema: Column schema in the form of a tuple.
        """
        column_type = re.findall('.[^\(]*', schema[1])
        maximum = decimal = None
        try:
            decimal = tuple(int(x)
                            for x in re.sub('[\(\)]', '', column_type[1])
                            .split(','))
        except:
            try:
                maximum = int(re.sub('[\(\)]', '', column_type[1]))
            except:
                pass

        self.attributes = dict(
            name=schema[0].lower,
            column_type=column_type[0],
            maximum=maximum,
            decimal=decimal,
            required=True if schema[2].upper() == 'NO' else False,
            unique=True if schema[3].upper() == 'UNI' else False,
            auto_increment=True if 'auto_increment' in schema[5] else False,
            default=None
        )

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
