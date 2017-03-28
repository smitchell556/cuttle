################
Cuttle Changelog
################

Here are the changes made to Cuttle for each release.

Version 0.5.0
-------------

Minor release, unreleased

- Close pre-existing cursor (if exists) in ``execute()``.
- Add internal methods to close connection and close cursor.
- Add ``executemany()`` method and update ``insert()``
  to accept a sequence of values.
- Cut down the list of acceptable comparison/conditional operators used by the
  ``where()`` method.
- Remove ``Column`` subclasses.
- Multiple Cuttle objects connected to different databases can be created.

Version 0.4.0
-------------

- ``where()`` accepts conditional and comparison operators.
- ``execute_query()`` is replace by ``execute()``.
- Removed ``cursor_properties()`` from ``Model`` since choosing to use a
  dict cursor is selected in the ``execute()`` method now.
- Moved all methods in ``_mysql_methods`` and ``_db_helpers`` modules to
  ``model``.
- Moved fetching of rows from ``execute()`` to various
  fetch methods.
- Created ``fetchone()``, ``fetchmany()``, and ``fetchall()`` methods to fetch rows.
- Added an ``__iter__()`` method to ``Model`` for returning
  rows from fetch operations.
- Made database connection instantiation lazy. A connection won't be made until it's
  needed. Removed the ``connect()`` method as a result since it's unneeded.
- Change ``Cuttle`` parameters to kwargs for more flexibility
  when creating connection objects.
- Check comparison/conditional operators for validity in ``where()``.
- Changed name of ``home`` module to ``reef``.
- Created a tutorial.

Version 0.3.0
-------------

- Changed parameters accepted by Cuttle object from one long configuration string
  to multiple parameters.
- Column names input to query methods can be checked for validity.
- Switched from mysql-connector-python to PyMySQL.
- Query methods generate strings instead of performing a query.
- ``where()`` must be called explicitly to add WHERE
  clause on Model subclass objects.
- ``execute_query()`` executes the generated query and returns
  the results, if any from Model subclass objects.
- Basic helper functions ``append_query()``, ``extend_values()``, and
  ``columns_lower()`` for manipulating query strings, values, and column name
  inputs.

Version 0.2.1
-------------

- Added instructions for installation to include non PyPi dependencies.
- Fix setup.py to properly upload all packages under cuttle.
- Added mock to docs to fix build errors on ImportError.

Version 0.2.0
-------------

First public release.
