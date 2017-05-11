Making Queries
==============

Now that the database has been created, you can interact with it through
the ``TouchPool`` class.

INSERT
------

In the python interpreter, import the ``TouchPool`` class and instantiate an
instance::

  >>> from cuttle_tutorial import TouchPool
  >>> touch_pool = TouchPool()

Data can be inserted with the :func:`~cuttle.model.Model.insert` method by
passing a list of table columns and list of values like so::

  >>> cols = ['fish_type', 'fish_name', 'age', 'personality']
  >>> vals = ['catfish', 'Hermes', 3, 'cuddly']
  >>> touch_pool.insert(cols, vals).execute()
  >>> touch_pool.commit()

A new row has been added to the database with the values inserted. In order for
changes to be written to the database, the have to be committed. Instead of
explicitely calling ``commit()``, ``True`` can be passed as an argument to
``execute()`` like so::

  >>> touch_pool.insert(cols, vals).execute(commit=True)

SELECT
------

Selecting data from the database is very similar, using the
:func:`~cuttle.model.Model.select` method. Try selecting every row in the
database. ::

  >>> touch_pool.select().execute(commit=True)

The results can be fetched using a fetch method like that of any SQL connector.
Cuttle supports :func:`~cuttle.model.Model.fetchone`, :func:`~cuttle.model.Model.fetchmany`,
and :func:`~cuttle.model.Model.fetchall`, as well as using the instance itself as
an iterator.

Using a fetch method::

  >>> print touch_pool.fetchone()
  (1, 'catfish', 'Hermes', 3, 'cuddly')

Using the instance as an iterator::

  >>> for fish in touch_pool:
  ...     print fish
  ...
  (1, 'catfish', 'Hermes', 3, 'cuddly')

Specific columns can also be selected for using the :func:`~cuttle.model.Model.select`
method by passing the column names to select as arguments like::

  >>> touch_pool.select('fish_name', 'fish_type').execute(commit=True)
  >>> print touch_pool.fetchone()
  ('Hermes', 'catfish')

UPDATE
------

Updating data is done in the same vein using the :func:`~cuttle.model.Model.update`
method. Whatever data you would like to be updated is passed as keyword arguments
to the method where the key is the column name, like so::

  >>> touch_pool.update(personality='cranky').execute(commit=True)

The lonely row in the table should be updated to reflect this change. ::

  >>> touch_pool.select().execute(commit=True)
  >>> print touch_pool.fetchone()
  (1, 'catfish', 'Hermes', 3, 'cranky')

WHERE
-----

Being able to update values is great, but not very useful without a WHERE
clause. Likewise, sometimes you will want to select rows based on certain
conditions. The above methods can be chained with the
:func:`~cuttle.model.Model.where` method to accomplish this task.

Before using :func:`~cuttle.model.Model.where`, insert another catfish to the
table. ::

  >>> cols = ['fish_type', 'fish_name', 'age', 'personality']
  >>> vals = ['catfish', 'Xerxes', 4, 'aloof']
  >>> touch_pool.insert(cols, vals).execute(commit=True)

Now update the table since Hermes was fed and is no longer cranky::

  >>> touch_pool.update(personality='cuddly')\
                .where(fish_name='Hermes')\
                .execute(commit=True)

Checking the rows in the table, you'll see the row containing Hermes was
updated, but the other row wasn't. ::

  >>> touch_pool.select().execute(commit=True)
  >>> for fish in touch_pool:
  ...     print fish
  ...
  (1, 'catfish', 'Hermes', 3, 'cuddly')
  (2, 'catfish', 'Xerxes', 4, 'aloof')

Now you have a lot more flexibility to interact with your table.

DELETE
------

Next is deleting entries. Let's insert a third catfish to demonstrate. ::

  >>> cols = ['fish_type', 'fish_name', 'age', 'personality']
  >>> vals = ['catfish', 'Rascal', 7, 'moody']
  >>> touch_pool.insert(cols, vals).execute(commit=True)
  >>> touch_pool.select().execute(commit=True)
  >>> for fish in touch_pool:
  ...     print fish
  ...
  (1, 'catfish', 'Hermes', 3, 'cuddly')
  (2, 'catfish', 'Xerxes', 4, 'aloof')
  (3, 'catfish', 'Rascal', 7, 'moody')

Rascal's owner just dropped him off for a visit and is back to pick him up, so
it's time to delete Rascal from the table::

  >> touch_pool.delete().where(fish_name='Rascal').execute(commit=True)

If you check the rows, you'll see Rascal's no longer there. ::

  >>> touch_pool.select().execute(commit=True)
  >>> for fish in touch_pool:
  ...     print fish
  ...
  (1, 'catfish', 'Hermes', 3, 'cuddly')
  (2, 'catfish', 'Xerxes', 4, 'aloof')

Closing the Connection
----------------------

It is a good idea to close the connection on the object when you're done with
it. The connection property of the table holds the connection object and can
be closed directly by calling the :func:`~cuttle.model.Model.close` method.
Continuing with the above example in the interpreter::

  >>> touch_pool.close()

It is not mandatory to close the connection, since the
:func:`~cuttle.model.Model.close` method will be called if the instance is
garbage collected. The key word being `if`; it's better not to assume all
references to the instance are deleted and just close the connection explicitly.

Another option is to use the object as a context manager, which will
automatically close the connection on exit. Just instantiate an object in a
``with`` statement. ::

  >>> with TouchPool() as touch_pool:
  ...     # do whatever you want with touch_pool

It's recommended to use the context manager to handle closing connections.

Combining Transactions
----------------------

At some point, you may find yourself interacting with multiple tables at once.
The problem with executing statements on multiple ``Model`` objects is that
each object has it's own connection to the database, resulting in multiple
transactions. If something goes wrong and you want to roll back all the
statements from each object, it has to be done on each object seperately.
It can be even hairier if some of those transactions have already been
committed.

To get around this, ``Cuttle`` has a ``Transaction`` object that can be passed
to a ``Model`` on instantiation. Every executed statement made on a ``Model``
holding a ``Transaction`` object will be executed by the ``Transaction`` object
instead and those statements can be committed as one transaction or rolled back
together.

A very simple example using our ``TouchPool``::

  >>> t = db.transaction()
  >>> touch_pool1 = TouchPool(t)
  >>> touch_pool2 = TouchPool(t)
  >>> # execute statements with the TouchPool objects as you normally would
  >>> t.commit()  # or t.rollback() if the statements shouldn't be committed
  >>> t.end()

The transaction is made and passed to both ``TouchPool`` objects and the
``TouchPool`` objects can be used as normal. All statements executed by each
``TouchPool`` object will go through the underlying ``Transaction`` object so
they'll all be bundled together. Although the ``Transaction`` object was only
passed to differenct instances of ``TouchPool``, it can be passed to every
subclass of ``Model`` and isn't restricted to a single subclass at any given
time.

``Transaction`` objects can also be used in a ``with`` statement. ::

  >>> with db.transaction() as t:
  ...     # use t as you would above
  ...     # there's no need to call t.commit() or t.end()

Using the context manager approach will automatically commit the transaction
when execution leaves the ``with`` block, or the transaction will be rolled
back if an exception is raised. The ``end()`` method will also be called
effectively killing the transaction.

.. note::
   Once ``end()`` is called, the ``Transaction`` object becomes useless. It no
   longer contains a connection to the database, so any attempts to execute
   statements will fail.
  
You've got the basics down, now check out :doc:`extend_model`
