# -*- coding: utf-8 -*-
"""
This module contains the Transaction class which is used to make querys as a
single transaction.

:license: MIT, see LICENSE for details.
"""


class Transaction(object):
    """
    ``Transaction`` objects are used to bundle SQL statement executions made
    across multiple tables into one transaction. A single ``Transaction``
    object can be passed to multiple ``Model`` objects.

    :param obj connection: A connection to the database.
    """

    def __init__(self, connection):
        self._connection = connection
        self._cursor = self._connection.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            self.rollback()
        else:
            self.commit()

        self._close()

    def _close(self):
        """Closes the connection to the database."""
        self._connection.close()
        self._connection = None

    def _execute(self, query, values):
        """Executes the SQL statement."""
        self._cursor.execute(query, values)

    def _executemany(self, query, values):
        """Executes the SQL statement."""
        self._cursor.executemany(query, values)

    def commit(self):
        """Commits the transaction."""
        self._connection.commit()

    def end(self):
        """Ends the transaction."""
        self._close()

    def rollback(self):
        """Rolls back the transaction."""
        self._connection.rollback()
