################
Cuttle Changelog
################

Here are the changes made to Cuttle for each release.

Version 0.4.0
-------------

Minor release, unreleased

- :func:`~cuttle.model.Model.where` accepts conditional and comparison operators.
- ``execute_query()`` is replace by
  :func:`~cuttle.model.Model.execute`.
- Removed :func:`~cuttle.model.Model.cursor_properties` since choosing to use a
  dict cursor is selected in the :func:`~cuttle.model.Model.execute` method now.
- Moved all methods in ``_mysql_methods`` and ``_db_helpers`` modules to
  :module:`~cuttle.model`.
- Moved fetching of rows from :func:`~cuttle.model.Model.execute` to various
  fetch methods.
- Created :func:`~cuttle.model.Model.fetchone`, :func:`~cuttle.model.Model.fetchmany`,
  and :func:`~cuttle.model.Model.fetchall` methods to fetch rows.
- Made database connection instantiation lazy. A connection won't be made until it's
  needed. Removed the ``connect()`` method as a result since it's unneeded.

Version 0.3.0
-------------

- Changed parameters accepted by Cuttle object from one long configuration string
  to multiple parameters.
- Column names input to query methods can be checked for validity.
- Switched from mysql-connector-python to PyMySQL.
- Query methods generate strings instead of performing a query.
- :func:`~cuttle.model.Model.where` must be called explicitly to add WHERE
  clause on Model subclass objects.
- ``execute_query()`` executes the generated query and returns
  the results, if any from Model subclass objects.
- Basic helper functions :func:`~cuttle.model.Model.append_query`,
  :func:`~cuttle.model.Model.extend_values`, and :func:`~cuttle.model.Model.columns_lower`
  for manipulating query strings, values, and column name inputs.

Version 0.2.1
-------------

- Added instructions for installation to include non PyPi dependencies.
- Fix setup.py to properly upload all packages under cuttle.
- Added mock to docs to fix build errors on ImportError.
