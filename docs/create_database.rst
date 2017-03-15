Creating a Database
===================

The first thing you will do is create a database. This requires a Cuttle object
and Model subclasses which represent tables.

In order to make these objects, you need to import Cuttle and any Column objects
that will be used. Create a file ``cuttle_tutorial.py`` and add the following
import statements::

  from cuttle.reef import Cuttle
  from cuttle.columns import IntColumn, TextColumn

The Column classes here are extensions of the base Column class. The only thing
they do is specify the data type. All other responsibilities are taken care of
by the base class. It's not necessary to use the Column subclasses, but they
provide convenience for selecting column data types.

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
          IntColumn('fish_id', primary_key=True),
          TextColumn('fish_type', required=True),
          TextColumn('fish_name', required=True),
          IntColumn('age', required=True),
          TextColumn('personality')
      ]

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
