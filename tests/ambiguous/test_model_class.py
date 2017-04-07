# -*- coding: utf-8
"""
Tests related to the Model class.
"""
import unittest

from cuttle.columns import Column
from cuttle.model import Model

from base_class import ModelObject, ModelSubclassObject


class ModelNamePropertyTestCase(unittest.TestCase):

    def test_model_name_lower(self):
        model = Model()

        self.assertEqual('model', model.name)


class ModelQueryTestCase(ModelObject):

    def test_query_property(self):
        self.model._query = ['test', 'query']
        self.assertEqual('test query', self.model.query)


class ModelValuesTestCase(ModelObject):

    def test_values_property(self):
        self.model._values = ['test', 'values']
        self.assertEqual(('test', 'values'), self.model.values)

    def test_seq_of_values_peroperty(self):
        self.model._values = [['test'], ['values']]
        self.assertEqual([('test',), ('values',)], self.model.seq_of_values)


class ModelConfigurationTestCase(unittest.TestCase):

    def test_configure_model_mysql(self):
        Model._configure_model('MySQL', db='db')

        self.assertEqual(Model._sql_type, 'mysql')

    def test_configure_model_improper_sql(self):
        with self.assertRaises(ValueError):
            Model._configure_model('toxicsql', db='db')


class ModelGenerateDbTestCase(ModelObject):

    def test_generate_db(self):
        self.model._generate_db('db')
        self.assertEqual(self.model._query, [
                         'CREATE DATABASE IF NOT EXISTS db'])

    def test_generate_table(self):
        class TestTable(self.Model):
            columns = [Column('c1', 'INT')]

        self.model._generate_table(TestTable)
        self.assertEqual(self.model._query,
                         ['CREATE TABLE IF NOT EXISTS testtable ( c1 INT )'])

    def test_generate_column(self):
        self.assertEqual(self.model._generate_column(Column('c1', 'INT')),
                         ['c1', 'INT,'])


class ModelSelectTestCase(ModelSubclassObject):

    def test_select_no_args(self):
        self.testtable.select()
        self.assertEqual(['SELECT * FROM testtable'],
                         self.testtable._query)

    def test_select_args(self):
        self.testtable.select('c1')
        self.assertEqual(['SELECT c1 FROM testtable'],
                         self.testtable._query)


class ModelInsertTestCase(ModelSubclassObject):

    def test_insert_no_args(self):
        self.testtable.insert()
        self.assertEqual(['INSERT INTO testtable () VALUES ()'],
                         self.testtable._query)
        self.assertEqual([], self.testtable._values)

    def test_insert_args(self):
        self.testtable.insert(['c1'], [1])
        self.assertEqual(['INSERT INTO testtable (c1) VALUES (%s)'],
                         self.testtable._query)
        self.assertEqual([1], self.testtable._values)

    def test_insert_many_args(self):
        self.testtable.insert(['c1'], [[1], [2]])
        self.assertEqual(['INSERT INTO testtable (c1) VALUES (%s)'],
                         self.testtable._query)
        self.assertEqual([[1], [2]], self.testtable._values)


class ModelUpdateTestCase(ModelSubclassObject):

    def test_update_no_args(self):
        with self.assertRaises(ValueError):
            self.testtable.update()

    def test_update_args(self):
        self.testtable.update(c1=1)
        self.assertEqual(['UPDATE testtable SET c1=%s'],
                         self.testtable._query)
        self.assertEqual([1], self.testtable._values)


class ModelDeleteTestCase(ModelSubclassObject):

    def test_delete(self):
        self.testtable.delete()
        self.assertEqual(['DELETE FROM testtable'], self.testtable._query)


class ModelWhereTestCase(ModelSubclassObject):

    def test_where_no_args(self):
        with self.assertRaises(ValueError):
            self.testtable.where()

    def test_where_single_args(self):
        self.testtable.where(c1=1)
        self.assertEqual(['WHERE c1=%s'], self.testtable._query)
        self.assertEqual([1], self.testtable._values)

    def test_where_multiple_args(self):
        self.testtable.where(c1=1, c2=2)
        try:
            self.assertEqual(['WHERE c1=%s AND c2=%s'],
                             self.testtable._query)
        except:
            self.assertEqual(['WHERE c2=%s AND c1=%s'],
                             self.testtable._query)
        try:
            self.assertItemsEqual([1, 2], self.testtable._values)
        except AttributeError:
            self.assertCountEqual([1, 2], self.testtable._values)

    def test_multiple_where(self):
        self.testtable.where(c1=1).where(condition='or', comparison='<', c2=2)
        self.assertEqual(['WHERE c1=%s', 'OR c2<%s'], self.testtable._query)
        try:
            self.assertItemsEqual([1, 2], self.testtable._values)
        except AttributeError:
            self.assertCountEqual([1, 2], self.testtable._values)

    def test_where_wrong_condition(self):
        with self.assertRaises(ValueError):
            self.testtable.where(condition='wrong', c1=1)

    def test_where_wrong_comparison(self):
        with self.assertRaises(ValueError):
            self.testtable.where(comparison='wrong', c1=1)


class ModelAppendQueryTestCase(ModelSubclassObject):

    def test_append_query(self):
        self.testtable.append_query('query')

        self.assertEqual(['query'], self.testtable._query)


class ModelExtendValuesTestCase(ModelSubclassObject):

    def test_extend_values_list(self):
        self.testtable.extend_values(['val1', 'val2'])

        self.assertEqual(['val1', 'val2'], self.testtable._values)

    def test_extend_values_list_of_lists(self):
        self.testtable.extend_values([['val1', 'val2'], ['val3', 'val4']])

        self.assertEqual([['val1', 'val2'], ['val3', 'val4']],
                         self.testtable._values)


class ModelColumnsLowerTestCase(ModelSubclassObject):

    def test_columns_lower_args(self):

        self.assertEqual(('c1', 'c2'),
                         self.testtable.columns_lower('C1', 'C2'))

    def test_columns_lower_kwargs(self):

        self.assertEqual({'c1': 1, 'c2': 'val'},
                         self.testtable.columns_lower(C1=1, C2='val'))


class ModelCheckColumnsTestCase(ModelSubclassObject):

    def test_check_columns_valid(self):
        testtable = self.TestTable()

        self.assertTrue(testtable.check_columns('c1', 'c2'))

    def test_check_columns_raise_error(self):
        testtable = self.TestTable()

        with self.assertRaises(ValueError):
            testtable.check_columns('c3')

    def test_check_columns_invalid_no_error(self):
        testtable = self.TestTable(raise_error_on_validation=False)

        self.assertFalse(testtable.check_columns('c3'))

    def test_check_columns_no_validation(self):
        testtable = self.TestTable(validate_columns=False)

        self.assertTrue(testtable.check_columns('c3'))


class ModelResetQuery(ModelSubclassObject):

    def test_reset_query(self):
        self.testtable._query.append(1)
        self.testtable._values.append(1)

        self.testtable.reset_query()

        self.assertEqual([], self.testtable._query)
        self.assertEqual([], self.testtable._values)
