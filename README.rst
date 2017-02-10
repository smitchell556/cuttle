######
Cuttle
######
The simple, extendable ORM
**************************

Cuttle is a small ORM that allows developers to create custom queries. It does
not aim to do everything, but instead abstracts away much of the basic steps
involved in database interactions.

How do I install Cuttle?
------------------------
Installation is as simple as ``pip install cuttle``.

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

What features does it have?
---------------------------
Cuttle can create databases and perform basic SELECT, INSERT, UPDATE, and DELETE
queries. What makes Cuttle different is the ability to write custom queries on
models.

What features are planned?
--------------------------
Besides including support for SQLite and PostgreSQL, the future includes
connection pooling, support for modifying database schema, and connecting to
multiple databases. Work on supporting SQLite and PostgreSQL will begin once the
API becomes stable for MySQL.

The intent is to extend Cuttle to support every SQL implementation, but for the
near future the above mentioned implementations will be the focus of attention.

How can I contribute?
---------------------
For the time being, this project won't be accepting outside contributions. It's
very much in it's infancy and the API can change drastically at any time. Once
the project has become more stable, contributions from the community will be
more than welcome. Just hold tight while Cuttle finds it's identity.

Where can I get help?
---------------------
The mailing list is on it's way!
