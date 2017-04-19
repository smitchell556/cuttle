# -*- coding: utf-8 -*-
"""
This module contains the Cuttle class which is the central unit for working
with Cuttle.

:license: MIT, see LICENSE for details.
"""
from cuttle.columns import Column
from cuttle.model import CuttlePool, Model


class Cuttle(object):
    """
    Cuttle represents the database. It is used to create the database and
    models.

    :param str sql_type: Determines what sql implementation to use (MySQL,
                         SQLite, etc).
    :param \**kwargs: Arguments to be passed to the connection object when
                      connections are made.

    :raise ValueError: If no database name is provided.

    :example: Instantiating Cuttle is as simple as:

              >>> from cuttle.reef import Cuttle
              >>> db = Cuttle('mysql', 'test_db', 'localhost', 'squirtle', 'my_passwd')
    """

    def __init__(self, sql_type, **kwargs):
        #: Holds Model class.
        kwargs['db'] = kwargs.get('db', None) or kwargs.get('database', None)
        if kwargs['db'] is None:
            raise ValueError('A database must be specified')

        try:
            del kwargs['database']
        except:
            pass

        self.Model = type(kwargs['db'], (Model,), {})
        self.Model.configure(sql_type, **kwargs)

    def _create_tables(self):
        """
        Creates tables.
        """
        for tbl in set(self._nested_subclasses(self.Model)):
            if tbl.__dict__.get('columns', False):
                with tbl() as tbl:
                    tbl.create_table().execute()

    def _nested_subclasses(self, cls):
        """
        Creates a list of all nested subclasses.
        """
        return cls.__subclasses__() + [s for sc in cls.__subclasses__()
                                       for s in self._nested_subclasses(sc)]

    def create_db(self, drop_existing=False):
        """
        Creates database.

        :param bool drop_existing: If ``True`` drops database if exists.
                                   Defaults to ``False``.
        """
        if drop_existing:
            self.drop_db()

        connection_arguments = self.Model().connection_arguments
        db_name = connection_arguments.pop('db')

        db_stmnt = 'CREATE DATABASE {}'.format(db_name)

        tmp_pool = CuttlePool(**connection_arguments)

        con = tmp_pool.get_connection()
        cur = con.cursor()

        cur.execute(db_stmnt)
        con.commit()

        cur.close()
        con.close()

        self._create_tables()

    def drop_db(self):
        """
        Drops the database.
        """
        with self.Model() as model:
            db_name = model.connection_arguments['db']
            drop_db = 'DROP DATABASE IF EXISTS {}'.format(db_name)
            model.append_query(drop_db)
            model.execute()
