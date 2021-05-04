import os
import sys
import unittest
import logging as log

from hspylib.core.config.app_config import AppConfigs
from hspylib.core.tools.commons import __curdir__

TEST_DIR = __curdir__(__file__)


class TestMain(unittest.TestCase):

    # Setup tests
    def setUp(self):
        resource_dir = '{}/resources'.format(TEST_DIR)
        os.environ['ACTIVE_PROFILE'] = "test"
        self.configs = AppConfigs(
            source_root=TEST_DIR, resource_dir=resource_dir, log_dir=resource_dir
        )
        self.assertIsNotNone(self.configs)
        self.assertIsNotNone(AppConfigs.INSTANCE)
        log.info(self.configs)

    # Teardown tests
    def tearDown(self):
        pass

    # TEST CASES ----------

    def test_should_test_something(self):
        pass


# Program entry point.
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMain)
    unittest \
        .TextTestRunner(verbosity=2, failfast=True, stream=sys.stdout) \
        .run(suite)
