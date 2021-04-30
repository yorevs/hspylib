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
        expected_size = 6
        properties = Properties()
        self.assertIsNotNone(properties)
        self.assertEqual(expected_size, properties.size())
        log.info(properties)

    def test_should_load_properties_using_custom_attributes(self):
        expected_size = 6
        load_dir = f'{TEST_DIR}/resources'
        filename = 'config.properties'
        profile = "test"
        properties = Properties(
            filename=filename, profile=profile, load_dir=load_dir
        )
        self.assertIsNotNone(properties)
        self.assertEqual(expected_size, properties.size())
        log.info(properties)

    def test_should_load_properties_from_ini_file(self):
        expected_size = 6
        load_dir = f'{TEST_DIR}/resources'
        filename = 'application.ini'
        properties = Properties(
            filename=filename, load_dir=load_dir
        )
        self.assertIsNotNone(properties)
        self.assertEqual(expected_size, properties.size())
        log.info(properties)

    def test_should_load_properties_from_yaml_file(self):
        expected_size = 6
        load_dir = f'{TEST_DIR}/resources'
        filename = 'application.yaml'
        properties = Properties(
            filename=filename, load_dir=load_dir
        )
        self.assertIsNotNone(properties)
        self.assertEqual(expected_size, properties.size())
        log.info(properties)

    def test_properties_should_be_subscriptable(self):
        expected_size = 6
        properties = TestProperties.properties
        self.assertIsNotNone(properties)
        self.assertEqual(expected_size, properties.size())
        expected_value = 'this is. = a weird value'
        self.assertEqual(expected_value, TestProperties.properties['test.weird.property'])

    def test_properties_should_be_iterable(self):
        expected_properties = [
            'this is. = a weird value', '1055', '3.14', 'FALse', 'TRue', 'should not be gotten',
        ]
        expected_size = 6
        properties = TestProperties.properties
        self.assertIsNotNone(properties)
        self.assertEqual(expected_size, properties.size())
        for prop in properties.values():
            self.assertTrue(prop in expected_properties)
            del expected_properties[0]
        self.assertEquals(0, len(expected_properties))


# Program entry point.
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestProperties)
    unittest \
        .TextTestRunner(verbosity=2, failfast=True, stream=sys.stdout) \
        .run(suite)
