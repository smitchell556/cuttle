# -*- coding: utf-8 -*-
"""

This module contains the Cuttle class which is the central unit for working
with Cuttle.

"""
import model


class Cuttle(object):
    """
    Cuttle represents the database. It is used to create the database and
    models. The argument can be passed to Cuttle as an environment variable or
    as a variable from another module/file that is not tracked by your
    repository if you do not want to hardcode the db credentials.

    :param str sql_type: Determines what sql implementation to use (MySQL,
                         SQLite, etc).
    :param \**kwargs: Arguments to be passed to the connection object when
                      connections are made.

    :raise ValueError: If not database name is provided.

    :example: Instantiating Cuttle is as simple as:

              >>> from cuttle.home import Cuttle
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

        self.Model = type(kwargs['db'], (model.Model,), {})
        self.Model._configure_model(sql_type, **kwargs)

    def create_db(self):
        """
        Creates database.
        """
        self.Model._create_db()
