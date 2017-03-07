################
Cuttle Changelog
################

Here are the changes made to Cuttle for each release.

Version 0.3.0
-------------

- Changed parameters accepted by Cuttle object from one long configuration string
  to multiple parameters.
- Column names input to query methods can be checked for validity.
- Switched from mysql-connector-python to PyMySQL.
- Query methods generate strings instead of performing a query.
- :func:`~cuttle.model.Model.where` must be called explicitly to add WHERE
  clause on Model subclass objects.
- :func:`~cuttle.model.Model.execute_query` executes the generated query and returns
  the results, if any from Model subclass objects.
- Basic helper functions :func:`~cuttle.model.Model.append_query`,
  :func:`~cuttle.model.Model.extend_values`, and :func:`~cuttle.model.Model.columns_lower`
  for manipulating query strings, values, and column name inputs.

Version 0.2.1
-------------

- Added instructions for installation to include non PyPi dependencies.
- Fix setup.py to properly upload all packages under cuttle.
- Added mock to docs to fix build errors on ImportError.
