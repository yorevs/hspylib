#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib
   test.config
      @file: test_properties.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""

from hspylib.core.config.properties import Properties
from hspylib.core.tools.commons import get_path

import logging as log
import os
import sys
import unittest

TEST_DIR = get_path(__file__)

RESOURCE_DIR = f"{TEST_DIR}/resources"


class TestProperties(unittest.TestCase):

    # Setup tests
    def setUp(self):
        os.environ["ACTIVE_PROFILE"] = ""

    # TEST CASES ----------

    def test_should_load_properties_using_defaults(self) -> None:
        expected_size = 6
        properties = Properties()
        self.assertIsNotNone(properties)
        self.assertEqual(expected_size, len(properties))
        log.debug(properties)

    def test_should_load_properties_using_custom_attributes(self) -> None:
        expected_size = 6
        filename = "config.properties"
        profile = "test"
        properties = Properties(filename=filename, profile=profile, load_dir=RESOURCE_DIR)
        self.assertIsNotNone(properties)
        self.assertEqual(expected_size, len(properties))

    def test_should_load_properties_from_ini_file(self) -> None:
        expected_size = 6
        filename = "application.ini"
        properties = Properties(filename=filename, load_dir=RESOURCE_DIR)
        self.assertIsNotNone(properties)
        self.assertEqual(expected_size, len(properties))

    def test_should_load_properties_from_yaml_file(self) -> None:
        expected_size = 6
        filename = "application.yaml"
        properties = Properties(filename=filename, load_dir=RESOURCE_DIR)
        self.assertIsNotNone(properties)
        self.assertEqual(expected_size, len(properties))

    def test_should_load_properties_from_toml_file(self) -> None:
        expected_size = 9
        filename = "application.toml"
        properties = Properties(filename=filename, load_dir=RESOURCE_DIR)
        self.assertIsNotNone(properties)
        self.assertEqual(expected_size, len(properties))

    def test_properties_should_be_subscriptable(self) -> None:
        expected_size = 6
        properties = Properties(load_dir=RESOURCE_DIR)
        self.assertIsNotNone(properties)
        self.assertEqual(expected_size, len(properties))
        expected_value = "this is. = a weird value"
        self.assertEqual(expected_value, properties["test.weird.property"])

    def test_properties_should_be_iterable(self) -> None:
        properties = Properties(load_dir=RESOURCE_DIR)
        expected_properties = ["this is. = a weird value", "1055", "3.14", "FALse", "TRue", "should not be gotten"]
        expected_size = 6
        self.assertIsNotNone(properties)
        self.assertEqual(expected_size, len(properties))
        for prop in properties.values:
            self.assertTrue(prop in expected_properties)
            del expected_properties[0]
        self.assertEqual(0, len(expected_properties))

    def test_should_load_properties_with_profile(self) -> None:
        os.environ["ACTIVE_PROFILE"] = "stage"
        properties = Properties(load_dir=RESOURCE_DIR)
        expected_properties = ["First property", "2022", "2.666", "TRue"]
        expected_size = 4
        self.assertIsNotNone(properties)
        self.assertEqual(expected_size, len(properties))
        for prop in properties.values:
            self.assertTrue(prop in expected_properties)
            del expected_properties[0]
        self.assertEqual(0, len(expected_properties))


# Program entry point.
if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestProperties)
    unittest.TextTestRunner(verbosity=2, failfast=True, stream=sys.stdout).run(suite)
