import os
import sys
import unittest

from main.hspylib.core.config.app_config import AppConfigs
from test.hspylib.core.crud.resources.TestFirebaseRepository import TestFirebaseRepository

TEST_DIR = os.path.dirname(os.path.realpath(__file__))


class TestClass(unittest.TestCase):

    # Setup tests
    def setUp(self):
        resource_dir = '{}/resources'.format(TEST_DIR)
        os.environ['ACTIVE_PROFILE'] = "test"
        AppConfigs(
            source_root=TEST_DIR, resource_dir=resource_dir, log_dir=resource_dir
        ).logger().info(AppConfigs.INSTANCE)
        # self.repository = TestFirebaseRepository()

    # Teardown tests
    def tearDown(self):
        pass

    # TEST CASES ----------

    # TC1 - Test inserting a single object into firebase.
    def test_should_insert_into_firebase(self):
        pass

    # TC2 - Test updating a single object from firebase.
    def test_should_update_firebase(self):
        pass

    # TC3 - Test selecting all objects from firebase.
    def test_should_select_all_from_firebase(self):
        pass

    # TC4 - Test selecting a single object from firebase.
    def test_should_select_one_from_firebase(self):
        pass

    # TC5 - Test deleting one object from firebase.
    def test_should_delete_from_firebase(self):
        pass


# Program entry point.
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestClass)
    unittest \
        .TextTestRunner(verbosity=2, failfast=True, stream=sys.stdout) \
        .run(suite)
