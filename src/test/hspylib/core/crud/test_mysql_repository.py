import os
import sys
import unittest

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
        assert self.repository, "Unable to instantiate MySqlRepository"
        self.repository.connect()
        self.assertTrue(self.repository.is_connected())
        self.repository.execute(
            'CREATE TABLE {} (UUID varchar(36) NOT NULL, COMMENT varchar(128) NOT NULL, PRIMARY KEY (UUID))'\
            .format(self.table))

    # Teardown tests
    def tearDown(self):
        self.repository.execute('DROP TABLE {}'.format(self.table))
        self.repository.disconnect()
        self.assertFalse(self.repository.is_connected())

    # TEST CASES ----------

    # TC1 - TODO comments.
    def test_should_insert_into_database(self):
        test_entity = TestEntity('My-Test Data')
        self.repository.insert(test_entity)

    # TC2 - TODO comments.
    def test_should_update_database(self):
        test_entity = TestEntity('My-Test Data')
        self.repository.insert(test_entity)
        test_entity.comment = 'Updated My-Test Data'
        self.repository.update(test_entity)

    # TC3 - TODO comments.
    def test_should_select_from_database(self):
        test_entity = TestEntity('My-Test Data')
        self.repository.insert(test_entity)
        result_set = self.repository.find_all(CaseInsensitiveDict({
            "UUID": '{}'.format(test_entity.uuid)
        }))
        assert result_set, "Result set is empty"


# Program entry point.
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMySqlRepository)
    unittest \
        .TextTestRunner(verbosity=2, failfast=True, stream=sys.stdout) \
        .run(suite)
