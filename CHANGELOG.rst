################
Cuttle Changelog
################

Here are the changes made to Cuttle for each release.

Version 0.3.0
-------------

Minor release, unreleased

- Changed parameters accepted by Cuttle object from one long configuration string
  to multiple parameters.
- Column names input to query methods can be checked for validity.
- Switched from mysql-connector-python to PyMySQL.

Version 0.2.1
-------------

- Added instructions for installation to include non PyPi dependencies.
- Fix setup.py to properly upload all packages under cuttle.
- Added mock to docs to fix build errors on ImportError.
