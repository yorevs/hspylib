import os
import sys
import unittest

from pymysql.err import InternalError
from requests.structures import CaseInsensitiveDict

from main.hspylib.core.config.app_config import AppConfigs
from test.hspylib.core.crud.resources.TestRepository import TestRepository, TestEntity

TEST_DIR = os.path.dirname(os.path.realpath(__file__))


class TestMySqlRepository(unittest.TestCase):

    # Setup tests
    def setUp(self):
        resource_dir = '{}/resources'.format(TEST_DIR)
        os.environ['ACTIVE_PROFILE'] = "test"
        AppConfigs(
            source_root=TEST_DIR, resource_dir=resource_dir, log_dir=resource_dir
        ).logger().info(AppConfigs.INSTANCE)
        self.repository = TestRepository()
        self.table = self.repository.table_name()
        assert self.repository, "Unable to instantiate TestRepository"
        self.repository.connect()
        self.assertTrue(self.repository.is_connected())
        try:
            self.repository.execute(
                'CREATE TABLE {} (UUID varchar(36) NOT NULL, COMMENT varchar(128) NOT NULL, PRIMARY KEY (UUID))'
                .format(self.table))
        except InternalError as err:
            if "Table 'TEST' already exists" not in str(err):
                raise err
            else:
                pass

    # Teardown tests
    def tearDown(self):
        self.repository.execute('DROP TABLE {}'.format(self.table))
        self.repository.disconnect()
        self.assertFalse(self.repository.is_connected())

    # TEST CASES ----------

    # TC1 - Test inserting a single row into the database.
    def test_should_insert_into_database(self):
        test_entity = TestEntity(comment='My-Test Data')
        self.repository.insert(test_entity)
        result_set = self.repository.find_all(sql_filters=CaseInsensitiveDict({
            "UUID": '{}'.format(test_entity.uuid)
        }))
        assert result_set, "Result set is empty"
        self.assertEqual(1, len(result_set))
        self.assertEqual(test_entity.uuid, result_set[0].uuid)

    # TC2 - Test updating a single row from the database.
    def test_should_update_database(self):
        test_entity = TestEntity(comment='My-Test Data')
        self.repository.insert(test_entity)
        test_entity.comment = 'Updated My-Test Data'
        self.repository.update(test_entity)
        result_set = self.repository.find_all(sql_filters=CaseInsensitiveDict({
            "UUID": '{}'.format(test_entity.uuid)
        }))
        assert result_set, "Result set is empty"
        self.assertEqual(1, len(result_set))
        self.assertEqual(test_entity.comment, result_set[0].comment)

    # TC3 - Test selecting all rows on the database.
    def test_should_select_all_from_database(self):
        test_entity = TestEntity(comment='My-Test Data')
        self.repository.insert(test_entity)
        result_set = self.repository.find_all()
        assert result_set, "Result set is empty"
        self.assertIsInstance(result_set, list)
        self.assertEqual(1, len(result_set))
        self.assertEqual(test_entity.uuid, result_set[0].uuid)

    # TC4 - Test selecting a single rows from the database.
    def test_should_select_one_from_database(self):
        test_entity = TestEntity(comment='My-Test Data')
        self.repository.insert(test_entity)
        result_set = self.repository.find_by_id(entity_id=str(test_entity.uuid))
        assert result_set, "Result set is empty"
        self.assertIsInstance(result_set, TestEntity)
        self.assertEqual(test_entity.uuid, result_set.uuid)

    # TC5 - Test selecting all rows and bring only specified columns.
    def test_should_select_columns_from_database(self):
        test_entity = TestEntity(comment='My-Test Data')
        self.repository.insert(test_entity)
        result_set = self.repository.find_all(column_set=["UUID"])
        assert result_set, "Result set is empty"
        self.assertIsInstance(result_set, list)
        self.assertEqual(1, len(result_set))
        self.assertEqual(test_entity.uuid, result_set[0].uuid)
        self.assertIsNone(result_set[0].comment)

    # TC6 - Test deleting one row from the database.
    def test_should_delete_from_database(self):
        test_entity = TestEntity(comment='My-Test Data')
        self.repository.insert(test_entity)
        result_set = self.repository.delete(test_entity)
        assert not result_set, "Result set is empty"


# Program entry point.
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMySqlRepository)
    unittest \
        .TextTestRunner(verbosity=2, failfast=True, stream=sys.stdout) \
        .run(suite)
