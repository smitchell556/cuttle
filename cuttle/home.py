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
    :param str db: The database to be used.
    :param str host: The host to be used. Defaults to None.
    :param str user: The user of the database to login under. Defaults to None.
    :param str passwd: The passwd for the user of the database. Defaults to
                       None.

    :example: Instantiating Cuttle is as simple as:

              >>> from cuttle.home import Cuttle
              >>> db = Cuttle('mysql', 'test_db', 'localhost', 'squirtle', 'my_passwd')
    """

    def __init__(self, sql_type, db,
                 host=None, user=None, passwd=None):
        #: Holds Model class.
        self.Model = model.Model
        self.Model._configure_model(sql_type, db, host, user, passwd)

    def create_db(self):
        """
        Creates database.
        """
        self.Model._create_db()
