#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   hspylib.test.hspylib.modules.application
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
from hspylib.core.exception.exceptions import InvalidOptionError, InvalidArgumentError
from hspylib.core.metaclass.singleton import Singleton
from hspylib.core.tools.commons import dirname
from hspylib.modules.cli.application.application import Application
from hspylib.modules.cli.application.option import Option
from test.hspylib.shared.application_test import ApplicationTest



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
        self.assertTrue('version' in app._options)  # pylint: disable=protected-access
        self.assertTrue('help' in app._options)  # pylint: disable=protected-access
        op_version = app._find_option('version')  # pylint: disable=protected-access
        self.assertIsNotNone(op_version)
        op_help = app._find_option('help')  # pylint: disable=protected-access
        self.assertIsNotNone(op_help)
        self.assertEqual(str(op_version), str(expected_op_version))
        self.assertEqual(str(op_help), str(expected_op_help))

    # TC5 - Check when passing defined options and arguments
    def test_calling_an_app_with_correct_opts_and_args_should_not_raise_errors(self):
        app = ApplicationTest('APP-TEST')
        params = ['-i', 'input.txt', '-o', 'output.txt', 'one', 'donut']
        app.run(params)
        self.assertEqual('input.txt', app.getopt('input'))
        self.assertEqual('output.txt', app.getopt('output'))
        self.assertEqual('one', app.getarg('amount'))
        self.assertEqual('donut', app.getarg('item'))

    # TC6 - Check when passing undefined options and arguments
    def test_calling_an_app_with_incorrect_opts_should_raise_errors(self):
        app = ApplicationTest('APP-TEST')
        params = ['-g', 'input.txt', '-j', 'output.txt', 'one', 'donut']
        self.assertRaises(InvalidOptionError, app.run, params)

    # TC7 - Check when passing undefined options and arguments
    def test_calling_an_app_with_incorrect_args_should_raise_errors_part_1(self):
        app = ApplicationTest('APP-TEST')
        params = ['-i', 'input.txt', '-o', 'output.txt', 'four', 'donut']
        self.assertRaises(InvalidArgumentError, app.run, params)

    # TC8 - Check when passing undefined options and arguments
    def test_calling_an_app_with_incorrect_args_should_raise_errors_part_2(self):
        app = ApplicationTest('APP-TEST')
        params = ['-i', 'input.txt', '-o', 'output.txt', 'one', 'pretzel']
        self.assertRaises(InvalidArgumentError, app.run, params)

    # TC9 - Check options and arguments passed can be retrieved
    def test_should_be_able_to_retrieve_passed_args_and_opts(self):
        app = ApplicationTest('APP-TEST')
        params = ['-i', 'input.txt', '-o', 'output.txt', 'one', 'donut']
        app.run(params)
        self.assertEqual('input.txt', app.getopt('input'))
        self.assertEqual('output.txt', app.getopt('output'))
        self.assertEqual('one', app.getarg('amount'))
        self.assertEqual('donut', app.getarg('item'))


# Program entry point.
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestApplication)
    unittest \
        .TextTestRunner(verbosity=2, failfast=True, stream=sys.stdout) \
        .run(suite)
