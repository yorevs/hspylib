import os
import sys
import unittest

from main.hspylib.core.config.app_config import AppConfigs
from test.hspylib.core.crud.resources.TestRepository import TestRepository

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
        assert self.repository, "Unable to instantiate MySqlRepository"
        self.repository.connect()

    # Teardown tests
    def tearDown(self):
        self.repository.disconnect()

    # TEST CASES ----------

    # TC1 - TODO comments.
    def test_should_implement(self):
        pass


# Program entry point.
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMySqlRepository)
    unittest \
        .TextTestRunner(verbosity=2, failfast=True, stream=sys.stdout) \
        .run(suite)
