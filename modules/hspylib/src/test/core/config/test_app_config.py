#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib
   test.config
      @file: test_app_config.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright·(c)·2024,·HSPyLib
"""

from hspylib.core.config.app_config import AppConfigs
from hspylib.core.tools.commons import dirname

import logging as log
import os
import sys
import unittest

TEST_DIR = dirname(__file__)


class TestAppConfig(unittest.TestCase):
    # Setup tests
    def setUp(self):
        resource_dir = "{}/resources".format(TEST_DIR)
        os.environ["ACTIVE_PROFILE"] = "test"
        self.configs = AppConfigs(resource_dir=resource_dir)
        self.assertIsNotNone(self.configs)
        self.assertIsNotNone(AppConfigs.INSTANCE)
        log.info(self.configs)
        os.environ["TEST_OVERRIDDEN_BY_ENVIRON"] = "yes its overridden"

    # TEST CASES ----------

    def test_should_get_a_weird_valued_property(self):
        expected_value = "this is. = a weird value"
        self.assertEqual(expected_value, AppConfigs.INSTANCE["test.weird.property"])

    def test_should_get_the_overridden_value(self):
        expected_value = "yes its overridden"
        self.assertEqual(expected_value, AppConfigs.INSTANCE["test.overridden.by.environ"])

    def test_should_get_int_property(self):
        expected_value = 1055
        self.assertEqual(expected_value, AppConfigs.INSTANCE.get_int("test.int.property"))

    def test_should_get_float_property(self):
        expected_value = 3.14
        self.assertEqual(expected_value, AppConfigs.INSTANCE.get_float("test.float.property"))

    def test_should_get_bool_property(self):
        expected_value_1 = False
        expected_value_2 = True
        self.assertEqual(expected_value_1, AppConfigs.INSTANCE.get_bool("test.bool.property1"))
        self.assertEqual(expected_value_2, AppConfigs.INSTANCE.get_bool("test.bool.property2"))

    def test_should_fail_due_to_invalid_type(self):
        with self.assertRaises(ValueError) as context:
            AppConfigs.INSTANCE.get_int("test.overridden.by.environ")
        self.assertTrue("invalid literal for int() with base 10" in str(context.exception))

    def test_should_be_subscriptable(self):
        expected_value_1 = "FALse"
        expected_value_2 = "TRue"
        self.assertEqual(expected_value_1, AppConfigs.INSTANCE["test.bool.property1"])
        self.assertEqual(expected_value_2, AppConfigs.INSTANCE["test.bool.property2"])

    def test_should_replace_placeholders(self):
        expected_value_1 = 10
        expected_value_2 = 0.657
        expected_value_3 = False
        expected_value_4 = "Hello, my name is MyName and surname is MySurname"
        placeholders = {
            "PLACEHOLDER_INT": expected_value_1,
            "Placeholder_Float": expected_value_2,
            "Placeholder_Bool": "off",
            "Name": "MyName", "Surname": "MySurname"
        }
        self.assertEqual(
            expected_value_1, AppConfigs.INSTANCE.get_int("test.placeholder.int.property", placeholders))
        self.assertEqual(
            expected_value_2, AppConfigs.INSTANCE.get_float("test.placeholder.float.property", placeholders))
        self.assertEqual(
            expected_value_3, AppConfigs.INSTANCE.get_bool("test.placeholder.bool.property", placeholders))
        self.assertEqual(
            expected_value_4, AppConfigs.INSTANCE.get("test.placeholder.strings.property", placeholders))

    def test_should_replace_placeholder_using_environment_vars(self):
        os.environ['TEST_ENVIRON_1'] = 'Just'
        os.environ['TEST_ENVIRON_2'] = 'Test'
        expected_value = "This is Just a Test"
        self.assertEqual(
            expected_value, AppConfigs.INSTANCE.get("test.placeholder.environment"))


# Program entry point.
if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAppConfig)
    unittest.TextTestRunner(verbosity=2, failfast=True, stream=sys.stdout).run(suite)
