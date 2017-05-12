# -*- coding: utf-8
"""
Tests related to the Model class.
"""
import sys
import unittest
import warnings

from cuttle.reef import Model

from test_cuttle_class import BaseDbTestCase, DB


class ModelTestCase(BaseDbTestCase):

    def setUp(self):
        super(ModelTestCase, self).setUp()
        self.db.create_db()

        self.pool = self.Pool(db=DB, **self.credentials)


class ModelStatementsTestCase(ModelTestCase):

    def setUp(self):
        super(ModelStatementsTestCase, self).setUp()

        self.con = self.pool.get_connection()
        self.cur = self.con.cursor()

        self.cur.executemany(
            ('INSERT INTO {} (hero_name) '
             'VALUES (%s)').format(self.testtable1().name),
            [('Goku',), ('Piccolo',)])
        self.con.commit()


class ModelNameTestCase(unittest.TestCase):

    def test_name_property(self):
        class Lower(Model):
            pass

        self.assertEqual(Lower().name, 'lower')


class ModelConnectionTestCase(ModelTestCase):

    def test_connection_property(self):
        with self.testtable1() as heros:
            self.assertIsInstance(heros.connection, self.Connection)

    def test_cursor_property(self):
        with self.testtable1() as heros:
            self.assertIsInstance(heros.cursor, self.Cursor)

    def test_connection_arguments_property(self):
        with self.testtable1() as heros:
            test_outp = {k: v for k, v in self.credentials.items()}
            test_outp.update(db=DB)

            for k in test_outp.keys():
                self.assertEqual(heros.connection_arguments[k], test_outp[k])


class ModelQueryValuesTestCase(unittest.TestCase):

    def setUp(self):
        class TestModel(Model):
            pass

        self.Model = TestModel

    def test_query_property(self):
        with self.Model() as model:
            query = 'this is a query'
            model._query = query.split(' ')
            self.assertEqual(model.query, query)

    def test_values_property(self):
        with self.Model() as model:
            values = ['these', 'are', 'values']
            model._values = values
            self.assertEqual(model.values, tuple(values))

    def test_seq_of_values_property(self):
        with self.Model() as model:
            seq_of_values = [['these', 'are', 'values'],
                             ['so', 'are', 'these']]
            model._values = seq_of_values
            self.assertEqual(model.seq_of_values,
                             [tuple(v) for v in seq_of_values])


class ModelSelectTestCase(ModelStatementsTestCase):

    def test_select_all(self):
        with self.testtable1() as heros:
            self.cur.execute('SELECT * FROM {}'.format(heros.name))
            self.con.commit()
            exp = self.cur.fetchall()

            heros.select().execute()
            self.assertEqual(heros.fetchall(), exp)

    def test_select_parameter(self):
        with self.testtable1() as heros:
            self.cur.execute('SELECT hero_name FROM {}'.format(heros.name))
            self.con.commit()
            exp = self.cur.fetchall()

            heros.select('hero_name').execute()
            self.assertEqual(heros.fetchall(), exp)

    def test_select_failure(self):
        with self.assertRaises(ValueError):
            with self.testtable1() as heros:
                heros.select('wrong')


class ModelInsertTestCase(ModelStatementsTestCase):

    def test_insert(self):
        with self.testtable1() as heros:
            hero = 'Yajirobe'
            heros.insert(['hero_name'], [hero]).execute(commit=True)

            self.cur.execute('SELECT hero_name FROM {}'.format(heros.name))
            self.con.commit()
            exp = self.cur.fetchall()
            self.assertIn((hero,), exp)

    def test_insert_many(self):
        with self.testtable1() as heros:
            hero1 = 'Yajirobe'
            hero2 = 'Master Roshi'
            heros.insert(['hero_name'], [[hero1], [hero2]])\
                 .executemany(commit=True)

            self.cur.execute('SELECT hero_name FROM {}'.format(heros.name))
            self.con.commit()
            exp = self.cur.fetchall()
            self.assertIn((hero1,), exp)
            self.assertIn((hero2,), exp)

    def test_insert_failure(self):
        with self.assertRaises(ValueError):
            with self.testtable1() as heros:
                heros.insert(['wrong'], ['Freeze'])


class ModelUpdateTestCase(ModelStatementsTestCase):

    def test_update(self):
        with self.testtable1() as heros:
            hero = 'Gohan'
            heros.update(hero_name=hero).execute(commit=True)

            self.cur.execute('SELECT hero_name FROM {}'.format(heros.name))
            self.con.commit()
            exp = self.cur.fetchall()

            self.assertTrue(all(map(lambda x: x == (hero,), exp)))

    def test_update_no_args(self):
        with self.assertRaises(ValueError):
            with self.testtable1() as heros:
                heros.update()

    def test_update_failure(self):
        with self.assertRaises(ValueError):
            with self.testtable1() as heros:
                heros.update(wrong='Freeze')


class ModelDeleteTestCase(ModelStatementsTestCase):

    def test_delete(self):
        with self.testtable1() as heros:
            heros.delete().execute(commit=True)

            self.cur.execute('SELECT hero_name FROM {}'.format(heros.name))
            self.con.commit()
            exp = self.cur.fetchall()

            self.assertEqual(tuple(), exp)


class ModelWhereTestCase(ModelStatementsTestCase):

    def test_where(self):
        with self.testtable1() as heros:
            heros.select('hero_name').where(hero_id=1).execute()

            self.assertEqual(heros.fetchone(), ('Goku',))

    def test_multiple_args(self):
        with self.testtable1() as heros:
            heros.select('hero_name').where(hero_id=1, hero_name='Goku')\
                                     .execute()

            self.assertEqual(heros.fetchone(), ('Goku',))

    def test_chained_where(self):
        with self.testtable1() as heros:
            heros.select('hero_name').where(comparison='>', hero_id=1)\
                                     .where(condition='or', hero_name='Goku')\
                                     .execute()
            rv = heros.fetchall()

            self.cur.execute('SELECT hero_name FROM {}'.format(heros.name))
            self.con.commit()
            exp = self.cur.fetchall()

            self.assertTrue(all(map(lambda x: x in rv, exp)))

    def test_where_no_args(self):
        with self.assertRaises(ValueError):
            with self.testtable1() as heros:
                heros.where()

    def test_where_failure(self):
        with self.assertRaises(ValueError):
            with self.testtable1() as heros:
                heros.where(wrong='Freeze')

    def test_where_wrong_condition(self):
        with self.assertRaises(ValueError):
            with self.testtable1() as heros:
                heros.where(condition='wrong', hero_id=1)

    def test_where_wrong_comparison(self):
        with self.assertRaises(ValueError):
            with self.testtable1() as heros:
                heros.where(comparison='wrong', hero_id=1)


class ModelTransactionTestCase(ModelTestCase):

    def setUp(self):
        super(ModelTransactionTestCase, self).setUp()

        self.con = self.pool.get_connection()
        self.cur = self.con.cursor()

    def test_explicit_commit(self):
        t = self.db.transaction()

        hero1 = 'Yajirobe'
        hero2 = 'Master Roshi'

        heros1 = self.testtable1(t)
        heros2 = self.testtable1(t)

        heros1.insert(['hero_name'], [hero1]).execute()
        heros2.insert(['hero_name'], [hero2]).execute()

        self.cur.execute('SELECT hero_name FROM {}'.format(heros1.name))
        self.con.commit()
        rv = self.cur.fetchall()

        self.assertNotIn((hero1,), rv)
        self.assertNotIn((hero2,), rv)

        t.commit()

        self.cur.execute('SELECT hero_name FROM {}'.format(heros1.name))
        self.con.commit()
        rv = self.cur.fetchall()

        self.assertIn((hero1,), rv)
        self.assertIn((hero2,), rv)

    def test_explicit_rollback(self):
        t = self.db.transaction()

        hero1 = 'Yajirobe'
        hero2 = 'Master Roshi'

        heros1 = self.testtable1(t)
        heros2 = self.testtable1(t)

        heros1.insert(['hero_name'], [hero1]).execute()
        heros2.insert(['hero_name'], [hero2]).execute()

        t.rollback()

        self.cur.execute('SELECT hero_name FROM {}'.format(heros1.name))
        self.con.commit()
        rv = self.cur.fetchall()

        self.assertNotIn((hero1,), rv)
        self.assertNotIn((hero2,), rv)

    def test_contextmanager_commit(self):

        hero1 = 'Yajirobe'
        hero2 = 'Master Roshi'

        with self.db.transaction() as t:
            heros1 = self.testtable1(t)
            heros2 = self.testtable1(t)

            heros1.insert(['hero_name'], [hero1]).execute()
            heros2.insert(['hero_name'], [hero2]).execute()

            self.cur.execute('SELECT hero_name FROM {}'.format(heros1.name))
            self.con.commit()
            rv = self.cur.fetchall()

            self.assertNotIn((hero1,), rv)
            self.assertNotIn((hero2,), rv)

        self.cur.execute('SELECT hero_name FROM {}'.format(heros1.name))
        self.con.commit()
        rv = self.cur.fetchall()

        self.assertIn((hero1,), rv)
        self.assertIn((hero2,), rv)


class ModelLowercaseColumnsTestCase(unittest.TestCase):

    def test_columns_lower_arg(self):
        with Model() as model:
            self.assertEqual(model.columns_lower('COL'), ('col',))

    def test_columns_lower_kwarg(self):
        with Model() as model:
            self.assertEqual(model.columns_lower(COL=1), dict(col=1))

    def test_columns_lower_both(self):
        with Model() as model:
            self.assertEqual(model.columns_lower('COL', COL=1),
                             ('col',))

    def test_columns_lower_no_args(self):
        with self.assertRaises(ValueError):
            with Model() as model:
                model.columns_lower()


class ModelCheckColumnsTestCase(ModelTestCase):

    def test_true_rv(self):
        with self.testtable1() as heros:
            self.assertTrue(heros.check_columns('hero_name'))

    def test_error_raised(self):
        with self.assertRaises(ValueError):
            with self.testtable1() as heros:
                heros.check_columns('villain_name')

    @unittest.skipIf(sys.version_info < (3, 3), 'test for warning skipped')
    def test_warning(self):
        with self.assertWarns(UserWarning):
            with self.testtable1(raise_error_on_validation=False) as heros:
                heros.check_columns('villain_name')

    def test_false_rv(self):
        warnings.filterwarnings('ignore')
        with self.testtable1(raise_error_on_validation=False) as heros:
            self.assertFalse(heros.check_columns('villain_name'))

    def test_true_rv_bad_input(self):
        with self.testtable1(validate_columns=False) as heros:
            self.assertTrue(heros.check_columns('villain_name'))


class ModelResetQueryTestCase(ModelTestCase):

    def test_reset_query(self):
        heros = self.testtable1()

        heros.select().where(hero_id=1)

        self.assertNotEqual(heros.query, '')
        self.assertNotEqual(heros.values, ())

        heros.reset_query()

        self.assertEqual(heros.query, '')
        self.assertEqual(heros.values, ())


class ModelCloseConnectionTestCase(ModelTestCase):

    def test_close(self):
        heros = self.testtable1()
        heros.cursor

        self.assertIsNotNone(heros._connection)
        self.assertIsNotNone(heros._cursor)

        heros.close()

        self.assertIsNone(heros._connection)
        self.assertIsNone(heros._cursor)
