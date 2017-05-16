######
Cuttle
######
The simple, extendable ORM
**************************

Cuttle is a small, open source ORM that allows developers to create custom
queries. It does not aim to do everything, but instead abstracts away much of
the basic steps involved in database interactions. Read the docs at
https://cuttle.readthedocs.io. Cuttle is licensed under the MIT license.

Why is it called Cuttle?
------------------------

It's called Cuttle after the cuttlefish.

Why make another ORM?
---------------------

This project started as a way to make database interactions as simple and easy
as possible. As work began, it became apparent that requirements for being easy
to use and flexible enough to handle unknown needs were at odds with each other.
This lead to the design of encouraging custom query statement creation methods
with Cuttle providing the infrastructure for making and executing custom methods
as easy as possible.

Installing Cuttle
-----------------

Install Cuttle with the command ``pip install cuttle``.

Is Cuttle usable?
-----------------

If you're only using MySQL, then kind of. It's still in the early stages of
development and things are likely to change quickly. If you decide to use it
keep in mind that the API can (and probably will) change frequently until a
1.0 release.

Why use Cuttle?
---------------

For simplicity. Cuttle was originally developed at a small business to be used on
low volume systems. As a result, it was designed to be easy to use and quick to
extend. It's goal is to cut down on development time for solo developers or
small teams with a simple API and extendable interface.

When will it be stable?
-----------------------

Maybe never. Features/bug fixes are added on an as needed basis and Cuttle is
still trying to find it's identity, so many things can change in the future.

What SQL implementations does Cuttle support?
---------------------------------------------

As of right now Cuttle only supports MySQL, but SQLite and PostgreSQL support is
planned for the future.

What Cuttle can do
------------------

Cuttle can create databases and perform basic SELECT, INSERT, UPDATE, and DELETE
queries. What makes Cuttle different is the ability to write custom queries on
models. Cuttle also uses connection pooling through `Cuttle Pool
<https://github.com/smitchell556/cuttlepool>`_

What features are planned?
--------------------------

Besides including support for SQLite and PostgreSQL, the future includes
support for modifying database schema. Work on supporting SQLite and PostgreSQL
will begin once the API becomes stable for MySQL.

The intent is to extend Cuttle to support every SQL implementation, but for the
near future the above mentioned implementations will be the focus of attention.

Contributing
------------

It's highly recommended to develop in a virtualenv.

Clone the repository::

  git clone https://github.com/smitchell556/cuttle.git

Install the package in editable mode::

  cd cuttle
  pip install -e .

Now you're set. See the next section for running tests.

Running the tests
-----------------

To run the tests, tox will need to be installed with ``pip install tox``.

First set the environment variable ``TEST_CUTTLE`` to the implementation you
want to test. For example ``export TEST_CUTTLE="mysql"`` will ensure the tests
are run using MySQL. Tests can be run using tox with the command ``tox``. If
the tests require user credentials, create a file ``<sql>_credentials.py`` with
the appropriate variables in the test directory, where ``<sql>`` is the specific
implementation desired for testing.

.. TODO:
   Include what credentials are needed to run tests using mysql.

Where can I get help?
---------------------
If you're having trouble, check the
`issue tracker <https://github.com/smitchell556/cuttle/issues>`_ to see if it's
being worked on (or solved). The mailing list can be found
`here <https://groups.google.com/forum/#!forum/cuttle>`_. If you have a question
that you can't find the answer to, it may have already been asked there,
otherwise please ask. Odds are somebody else has the same question to.
