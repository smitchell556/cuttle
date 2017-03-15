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

Column Objects
--------------

.. module:: cuttle.columns

Column objects are used to in Model subclasses.

The Column class is used to build all Column subclasses.

.. autoclass:: Column
   :members:
   :inherited-members:

.. autoclass:: IntColumn
   :members:
   :inherited-members:

.. autoclass:: DecimalColumn
   :members:
   :inherited-members:

.. autoclass:: TextColumn
   :members:
   :inherited-members:

.. autoclass:: DateColumn
   :members:
   :inherited-members:

.. autoclass:: DateTimeColumn
   :members:
   :inherited-members:
