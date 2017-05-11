API
===

Cuttle Object
-------------

The Cuttle object connects all the tables and is used to create the database

.. module:: cuttle.reef

.. autoclass:: Cuttle
   :members:
   :inherited-members:

Model Object
------------

.. module:: cuttle.model

Model subclasses represent tables.

.. autoclass:: Model
   :members:
   :inherited-members:

Column Object
-------------

.. module:: cuttle.columns

Column objects are used to represent columns in Model subclasses.

.. autoclass:: Column
   :members:
   :inherited-members:

Transaction object
------------------

.. module:: cuttle.transaction

Transaction objects are used to bundle multiple executions across Models into
one transaction.

.. autoclass:: Transaction
   :members:
   :inherited-members:
