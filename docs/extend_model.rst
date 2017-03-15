Custom Query Methods
====================

Now that your touch pool is populated with fish, you realize that Xerxes is
older than Hermes and should be returned first from a SELECT query. Cuttle
can't help you with this directly, but using some helper methods, you can make
the ``TouchPool`` class order results from a SELECT query by writing a custom
query method.

In ``cuttle_tutorial.py`` you created the following class::

  class TouchPool(db.Model):
      columns = [
          IntColumn('fish_id', primary_key=True),
          TextColumn('fish_type', required=True),
          TextColumn('fish_name', required=True),
          IntColumn('age', required=True),
          TextColumn('personality')
      ]

Now add the following method to that class so that it looks like this::

  class TouchPool(db.Model):
      columns = [
          IntColumn('fish_id', primary_key=True),
          TextColumn('fish_type', required=True),
          TextColumn('fish_name', required=True),
          IntColumn('age', required=True),
          TextColumn('personality')
      ]

      def order_by(self, column, order='ASC'):
          """Creates an ORDER BY clause"""
          # Make sure order is an appropriate keyword to prevent SQL injection.
          order = order.upper()
          if order not in ['ASC', 'DESC']:
              raise ValueError('{} is not a proper keyword'.format(order))

          # Convert column names in kwargs to lowercase since the columns in
          # the table are converted to lowercase when the database is created.
          column = self.columns_lower(column)[0]

          # Check columns are valid to prevent SQL injection.
          if self.check_columns(column):
              # Create the ORDER BY statement.
              q = 'ORDER BY {} {}'.format(column, order)

              # Append the ORDER BY statement to the query property.
              self.append_query(q)

          return self

Breaking the ``order_by()`` method down part by part, you see that the ``order``
parameter is checked for validity. This is necessary to prevent SQL injection
on the off chance that a user's input is passed to the function. Never assume
that a user's input won't be passed to the function. Always, always validate.
This doesn't apply to values (it still applies to the columns passed to it
though) such as those passed in the :func:`~cuttle.model.Model.insert`
method since those are checked by the underlying SQL connector, but those
should also be handled per the specifications of the underlying connector.

Next, the :func:`~cuttle.model.Model.columns_lower` method returns a tuple
of the arguments passed to it in lowercase. Since only one argument was passed
to it, that argument is selected from the tuple and the tuple is discarded.
The column name must be converted to lowercase because the column names on the
table are converted to lowercase when the database is created with the
:func:`~cuttle.reef.Cuttle.create_db` method.

Then the column is checked with the :func:`~cuttle.model.Model.check_columns`
method to ensure that the column is in fact in the table. Again, to prevent
SQL injection.

Finally the ORDER BY statement is created and appended to the ``query`` property
using :func:`~cuttle.model.Model.append_query`. The instance is returned to
continue chaining query methods.

Back in the python interpreter, try using the custom query method you just made.

::

  >>> touch_pool = TouchPool()
  >>> touch_pool.select().order_by('age', 'DESC').execute()
  >>> for fish in touch_pool:
  ...     print fish
  (2, 'catfish', 'Xerxes', 4, 'aloof')
  (1, 'catfish', 'Hermes', 3, 'cuddly')

Now you can customize Cuttle to create more specific statements based on your
needs. If you would like custom query methods available on all your models, you
can create a subclass of ``Model`` that contains all the custom query methods
you would like, then set ``db.Model`` to that subclass and use that to create
your table models. If there are any Model subclasses that you do not want to be
made into tables by :func:`~cuttle.reef.Cuttle.create_db`, just omit the
``columns`` property from that class and a table will not be made in the
database for it.

I highly encourage you to look through the API for the :class:`~cuttle.model.Model`
class to understand the helper functions available and to get ideas from the
built in query methods for formatting your own.
