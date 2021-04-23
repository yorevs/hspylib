import os
import sys
import unittest

from hspylib.core.config.app_config import AppConfigs

TEST_DIR = os.path.dirname(os.path.realpath(__file__))


class TestAppConfig(unittest.TestCase):

    # Setup tests
    def setUp(self):
        resource_dir = '{}/resources'.format(TEST_DIR)
        os.environ['ACTIVE_PROFILE'] = "test"
        self.configs = AppConfigs(
            source_root=TEST_DIR, resource_dir=resource_dir, log_dir=resource_dir
        )
        self.assertIsNotNone(self.configs)
        self.assertIsNotNone(AppConfigs.INSTANCE)
        self.configs.logger().info(self.configs)
        os.environ['TEST_OVERRIDDEN_BY_ENVIRON'] = 'yes its overridden'

    # Teardown tests
    def tearDown(self):
        pass

    # TEST CASES ----------

    def test_should_get_a_weird_valued_property(self):
        expected_value = 'this is. = a weird value'
        self.assertEqual(expected_value, AppConfigs.INSTANCE.get('test.weird.property'))

    def test_should_get_the_overridden_value(self):
        expected_value = 'yes its overridden'
        self.assertEqual(expected_value, AppConfigs.INSTANCE.get('test.overridden.by.environ'))

    def test_should_get_int_property(self):
        expected_value = 1055
        self.assertEqual(expected_value, AppConfigs.INSTANCE.get_int('test.int.property'))

    def test_should_get_float_property(self):
        expected_value = 3.14
        self.assertEqual(expected_value, AppConfigs.INSTANCE.get_float('test.float.property'))

    def test_should_get_bool_property(self):
        expected_value_1 = False
        expected_value_2 = True
        self.assertEqual(expected_value_1, AppConfigs.INSTANCE.get_bool('test.bool.property1'))
        self.assertEqual(expected_value_2, AppConfigs.INSTANCE.get_bool('test.bool.property2'))

    def test_should_fail_due_to_invalid_type(self):
        with self.assertRaises(ValueError) as context:
            AppConfigs.INSTANCE.get_int('test.overridden.by.environ')
        self.assertTrue('invalid literal for int() with base 10' in str(context.exception))

    def test_should_be_subscriptable(self):
        expected_value_1 = 'FALse'
        expected_value_2 = 'TRue'
        self.assertEqual(expected_value_1, AppConfigs.INSTANCE['test.bool.property1'])
        self.assertEqual(expected_value_2, AppConfigs.INSTANCE['test.bool.property2'])


# Program entry point.
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAppConfig)
    unittest \
        .TextTestRunner(verbosity=2, failfast=True, stream=sys.stdout) \
        .run(suite)
