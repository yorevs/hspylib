#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   test.modules.application
      @file: test_application.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
import argparse
import os
import sys
import unittest
from hspylib.core.config.app_config import AppConfigs
from hspylib.core.metaclass.singleton import Singleton
from hspylib.core.tools.commons import get_path
from hspylib.modules.cli.application.application import Application
from hspylib.modules.cli.application.version import Version
from shared.application_test import ApplicationTest

APP_VERSION = Version((0, 1, 0))


class TestApplication(unittest.TestCase):

    # TEST CASES ----------
    def setUp(self) -> None:
        os.environ['ACTIVE_PROFILE'] = ''
        Singleton.del_instance(Application)
        Singleton.del_instance(AppConfigs)
        Singleton.del_instance(ApplicationTest)

    # TC1 - Application should be singleton
    def test_application_should_be_singleton(self):
        app_1 = Application('App-test-1', APP_VERSION)
        app_2 = Application('App-test-2', APP_VERSION)
        self.assertIsNotNone(app_1)
        self.assertIsNotNone(app_2)
        self.assertEqual(app_1, app_2)

    # TC2 - Creating an application without specifying source root directory
    def test_should_not_instantiate_configs(self):
        Application('APP-TEST', APP_VERSION, resource_dir='/gabs')
        self.assertFalse(hasattr(AppConfigs, 'INSTANCE'))

    # TC3 - Creating an application specifying source root directory
    def test_should_instantiate_configs(self):
        cur_dir = get_path(__file__)
        Application('APP-TEST', APP_VERSION, resource_dir=f'{str(cur_dir)}/resources')
        self.assertTrue(hasattr(AppConfigs, 'INSTANCE'))

    # TC4 - Check when passing defined options and arguments
    def test_calling_an_app_with_correct_opts_and_args_should_not_raise_errors(self):
        app = ApplicationTest('APP-TEST')
        params = ['-i', 'input.txt', '-o', 'output.txt', 'one', 'donut']
        app.run(params, no_exit=True)
        self.assertEqual('input.txt', app.get_arg('input'))
        self.assertEqual('output.txt', app.get_arg('output'))
        self.assertEqual('one', app.get_arg('amount'))
        self.assertEqual('donut', app.get_arg('item'))

    # TC5 - Check when passing undefined options and arguments
    def test_calling_an_app_with_incorrect_opts_should_raise_errors(self):
        app = ApplicationTest('APP-TEST')
        params = ['-g', 'input.txt', '-j', 'output.txt', 'one', 'donut']
        self.assertRaises(argparse.ArgumentError, lambda: app.run(params, no_exit=True))

    # TC6 - Check when passing undefined options and arguments
    def test_calling_an_app_with_incorrect_args_should_raise_errors_part_1(self):
        app = ApplicationTest('APP-TEST')
        params = ['-i', 'input.txt', '-o', 'output.txt', 'four', 'donut']
        self.assertRaises(argparse.ArgumentError, lambda: app.run(params, no_exit=True))

    # TC7 - Check when passing undefined options and arguments
    def test_calling_an_app_with_incorrect_args_should_raise_errors_part_2(self):
        app = ApplicationTest('APP-TEST')
        params = ['-i', 'input.txt', '-o', 'output.txt', 'one', 'pretzel']
        self.assertRaises(argparse.ArgumentError, lambda: app.run(params, no_exit=True))

    # TC8 - Check options and arguments passed can be retrieved
    def test_should_be_able_to_retrieve_passed_args_and_opts(self):
        app = ApplicationTest('APP-TEST')
        params = ['-i', 'input.txt', '-o', 'output.txt', 'one', 'donut']
        app.run(params, no_exit=True)
        self.assertEqual('input.txt', app.get_arg('input'))
        self.assertEqual('output.txt', app.get_arg('output'))
        self.assertEqual('one', app.get_arg('amount'))
        self.assertEqual('donut', app.get_arg('item'))


# Program entry point.
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestApplication)
    unittest \
        .TextTestRunner(verbosity=2, failfast=True, stream=sys.stdout) \
        .run(suite)
