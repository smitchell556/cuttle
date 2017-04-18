API
===

Cuttle Object
-------------

The Cuttle object connects all the tables and is used to create the database

.. module:: cuttle.reef

.. autoclass:: Cuttle
   :members:
   :inherited-members:

Model Objects
-------------

.. module:: cuttle.model

Model subclasses represent tables.

.. autoclass:: Model
   :members:
   :inherited-members:
   :exclude-members: create_table

Column Objects
--------------

.. module:: cuttle.columns

Column objects are used to represent columns in Model subclasses.

.. autoclass:: Column
   :members:
   :inherited-members:
   :exclude-members: attributes, name, primary_key, column_schema
