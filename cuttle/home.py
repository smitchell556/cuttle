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

    :param str config: Sets configuration for Cuttle to connect to database.
                       expected in the form:
                       ``"<sql_type>|<database>|<host>|<user>|<password>"``

    :example: Instantiating Cuttle is as simple as:

              >>> from cuttle.home import Cuttle
              >>> db = Cuttle("mysql|test_db|localhost|spencer|my_passwd")
    """

    def __init__(self, config):
        #: Holds Model class.
        self.Model = model.Model
        self.Model._configure_model(config)

    def create_db(self):
        """
        Creates database.

        :note: In order for Cuttle to create the database you want, subclasses
               of Model must be made otherwise the database will be empty.
        """
        self.Model._create_db()
