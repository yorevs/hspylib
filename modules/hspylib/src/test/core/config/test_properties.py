#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   test.config
      @file: test_properties.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

import logging as log
import sys
import unittest

from core.config.properties import Properties
from core.tools.commons import get_path

TEST_DIR = get_path(__file__)


class TestProperties(unittest.TestCase):

    # TEST CASES ----------
    def test_should_load_properties_using_defaults(self):
        expected_size = 6
        properties = Properties()
        self.assertIsNotNone(properties)
        self.assertEqual(expected_size, len(properties))
        log.info(properties)

    def test_should_load_properties_using_custom_attributes(self):
        expected_size = 6
        load_dir = f'{TEST_DIR}/resources'
        filename = 'config.properties'
        profile = "test"
        properties = Properties(filename=filename, profile=profile, load_dir=load_dir)
        self.assertIsNotNone(properties)
        self.assertEqual(expected_size, len(properties))

    def test_should_load_properties_from_ini_file(self):
        expected_size = 6
        load_dir = f'{TEST_DIR}/resources'
        filename = 'application.ini'
        properties = Properties(filename=filename, load_dir=load_dir)
        self.assertIsNotNone(properties)
        self.assertEqual(expected_size, len(properties))

    def test_should_load_properties_from_yaml_file(self):
        expected_size = 6
        load_dir = f'{TEST_DIR}/resources'
        filename = 'application.yaml'
        properties = Properties(filename=filename, load_dir=load_dir)
        self.assertIsNotNone(properties)
        self.assertEqual(expected_size, len(properties))

    def test_properties_should_be_subscriptable(self):
        expected_size = 6
        properties = Properties(load_dir=f'{TEST_DIR}/resources')
        self.assertIsNotNone(properties)
        self.assertEqual(expected_size, len(properties))
        expected_value = 'this is. = a weird value'
        self.assertEqual(expected_value, properties['test.weird.property'])

    def test_properties_should_be_iterable(self):
        expected_properties = ['this is. = a weird value', '1055', '3.14', 'FALse', 'TRue', 'should not be gotten']
        expected_size = 6
        properties = Properties(load_dir=f'{TEST_DIR}/resources')
        self.assertIsNotNone(properties)
        self.assertEqual(expected_size, len(properties))
        for prop in properties.values():
            self.assertTrue(prop in expected_properties)
            del expected_properties[0]
        self.assertEqual(0, len(expected_properties))


# Program entry point.
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestProperties)
    unittest \
        .TextTestRunner(verbosity=2, failfast=True, stream=sys.stdout) \
        .run(suite)
