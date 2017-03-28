Creating a Database
===================

The first thing you will do is create a database. This requires a Cuttle object
and Model subclasses which represent tables.

In order to make these objects, you need to import Cuttle and the Column class.
Create a file ``cuttle_tutorial.py`` and add the following import statements::

  from cuttle.reef import Cuttle
  from cuttle.columns import Column

The next line creates a Cuttle object, which we will use to create subclasses
of the Model class. These subclasses will reflect the tables that Cuttle will
create in a database. ::

  db = Cuttle(sql_type='mysql',
              user='<user>',
              passwd='<passwd>',
              host='localhost',
              db='aquarium')

.. note:: Replace `'<user>'` and `'<passwd>'` with the user and password of a MySQL
          user on your computer.

The Cuttle object accepts any keyword arguments that the connection object of
the underlying python SQL connector accepts. Just beware that if you want to
pass a cursor class (such as a DictCursor) as an argument to Cuttle, it must be
imported first. That goes for any object that can be accepted by the underlying
``Connection`` object.

Great, the next step is creating table schema using our Cuttle object.

Subclassing Model
-----------------

Under the Cuttle object, create a Model subclass as follows::

  class TouchPool(db.Model):
      columns = [
          Column('fish_id', 'INT', primary_key=True),
          Column('fish_type', 'VARCHAR', required=True),
          Column('fish_name', 'VARCHAR', required=True),
          Column('age', 'INT', required=True),
          Column('personality', 'VARCHAR')
      ]

:class:`~cuttle.columns.Column` requires a name and column type.

That's all you need to setup a database. The only thing left is actually creating
it which you can do from the command line.

Run create_db()
---------------

Open up a python interpreter in the same directory as ``cuttle_tutorial.py`` and
run the following commands::

  >>> from cuttle_tutorial import db
  >>> db.create_db()

If you check the available MySQL databases, you should see ``aquarium`` there
and a table based on the ``TouchPool`` class in that database.

Continue with :doc:`queries`.
