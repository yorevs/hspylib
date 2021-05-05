#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.test.hspylib.modules.application
      @file: test_application.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

import sys
import unittest

from hspylib.core.config.app_config import AppConfigs
from hspylib.core.meta.singleton import Singleton
from hspylib.core.tools.commons import dirname
from hspylib.modules.cli.application.application import Application
from hspylib.modules.cli.application.option import Option


class TestApplication(unittest.TestCase):
    
    # TEST CASES ----------
    def setUp(self) -> None:
        Singleton.del_instance(Application)
        Singleton.del_instance(AppConfigs)
    
    # TC1 - Application should be singleton
    def test_application_should_be_singleton(self):
        app_1 = Application('App-test-1')
        app_2 = Application('App-test-2')
        self.assertIsNotNone(app_1)
        self.assertIsNotNone(app_2)
        self.assertEqual(app_1, app_2)
    
    # TC2 - Creating an application without specifying source root directory
    def test_should_not_instantiate_configs(self):
        Application('App-test')
        self.assertFalse(hasattr(AppConfigs, 'INSTANCE'))
    
    # TC3 - Creating an application specifying source root directory
    def test_should_instantiate_configs(self):
        Application('App-test', source_dir=dirname(__file__))
        self.assertTrue(hasattr(AppConfigs, 'INSTANCE'))
    
    # TC4 - Check application should accept -v|--version when version is specified
    def test_should_define_version_and_help_options(self):
        app = Application('App-test', app_version=(0, 0, 1), app_usage="Usage: This is a test")
        expected_op_version = Option('-v', '--version', cb_handler=app.version)
        expected_op_help = Option('-h', '--help', cb_handler=app.usage)
        self.assertTrue('version' in app.options)
        self.assertTrue('help' in app.options)
        op_version = app.get_option('version')
        self.assertIsNotNone(op_version)
        op_help = app.get_option('help')
        self.assertIsNotNone(op_help)
        self.assertEqual(str(op_version), str(expected_op_version))
        self.assertEqual(str(op_help), str(expected_op_help))


# Program entry point.
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestApplication)
    unittest \
        .TextTestRunner(verbosity=2, failfast=True, stream=sys.stdout) \
        .run(suite)
