import logging as log
import pathlib
import sys
import unittest

from hspylib.core.config.properties import Properties

# The directory containing this file
TEST_DIR = pathlib.Path(__file__).parent


class TestProperties(unittest.TestCase):

    properties = None

    # TEST CASES ----------
    @classmethod
    def setUpClass(cls) -> None:
        load_dir = f'{TEST_DIR}/resources'
        cls.properties = Properties(
            load_dir=load_dir
        )
        log.info(cls.properties)

    def test_should_load_properties_using_defaults(self):
        properties = Properties()
        self.assertIsNotNone(properties)
        log.info(properties)

    def test_should_load_properties_using_custom_attributes(self):
        load_dir = f'{TEST_DIR}/resources'
        filename = 'config.properties'
        profile = "test"
        properties = Properties(
            filename=filename, profile=profile, load_dir=load_dir
        )
        self.assertIsNotNone(properties)
        log.info(properties)

    def test_properties_should_be_subscriptable(self):
        self.assertIsNotNone(TestProperties.properties)
        expected_value = 'this is. = a weird value'
        self.assertEqual(expected_value, TestProperties.properties['test.weird.property'])

    # def text_properties_should


# Program entry point.
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestProperties)
    unittest \
        .TextTestRunner(verbosity=2, failfast=True, stream=sys.stdout) \
        .run(suite)
