#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib
   test.modules.application
      @file: test_application.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright·(c)·2024,·HSPyLib
"""
from hspylib.core.config.app_config import AppConfigs
from hspylib.core.exception.exceptions import ApplicationError
from hspylib.core.metaclass.singleton import Singleton
from hspylib.core.tools.commons import parent_path
from hspylib.modules.application.application import Application
from hspylib.modules.application.exit_status import ExitStatus
from hspylib.modules.application.version import Version
from shared.application_test import ApplicationTest

import os
import sys
import unittest

APP_VERSION = Version.initial()


class TestApplication(unittest.TestCase):
    class AppTest(Application, metaclass=Singleton):
        def __init__(self, name: str = "AppTest", version: Version = APP_VERSION, resource_dir: str = None):
            super().__init__(name, version, resource_dir=resource_dir)

        def _setup_arguments(self) -> None:
            pass

        def _main(self, *params, **kwargs) -> ExitStatus:
            pass

        def _cleanup(self) -> None:
            pass

    # TEST CASES ----------
    def setUp(self) -> None:
        os.environ["ACTIVE_PROFILE"] = ""
        if Singleton.has_instance(self.AppTest):
            Singleton.del_instance(self.AppTest)
        if Singleton.has_instance(AppConfigs):
            Singleton.del_instance(AppConfigs)
        if Singleton.has_instance(ApplicationTest):
            Singleton.del_instance(ApplicationTest)

    # Application should be singleton
    def test_application_should_be_singleton(self) -> None:
        app_1 = self.AppTest()
        app_2 = self.AppTest()
        self.assertIsNotNone(app_1)
        self.assertIsNotNone(app_2)
        self.assertEqual(app_1, app_2)

    # Creating an application without specifying source root directory
    def test_should_not_instantiate_configs(self) -> None:
        app = self.AppTest(resource_dir="/gabs")
        self.assertFalse(hasattr(app, "configs"))
        self.assertFalse(Singleton.has_instance(AppConfigs))

    # Creating an application specifying source root directory
    def test_should_instantiate_configs(self) -> None:
        cur_dir = parent_path(__file__)
        app = self.AppTest(resource_dir=f"{str(cur_dir)}/resources")
        self.assertTrue(hasattr(app.configs, "INSTANCE"))

    # Check when passing defined options and arguments
    def test_calling_an_app_with_correct_opts_and_args_should_not_raise_errors(self) -> None:
        app = ApplicationTest()
        params = ["-i", "input.txt", "-o", "output.txt", "one", "donut"]
        app.run(params, no_exit=True)
        self.assertEqual("input.txt", app.get_arg("input"))
        self.assertEqual("output.txt", app.get_arg("output"))
        self.assertEqual("one", app.get_arg("amount"))
        self.assertEqual("donut", app.get_arg("item"))

    # Check when passing undefined options and arguments
    def test_calling_an_app_with_incorrect_opts_should_raise_errors(self) -> None:
        app = ApplicationTest()
        params = ["-g", "input.txt", "-j", "output.txt", "one", "donut"]
        self.assertRaises(ApplicationError, lambda: app.run(params, no_exit=True))

    # Check when passing undefined options and arguments
    def test_calling_an_app_with_incorrect_args_should_raise_errors_part_1(self) -> None:
        app = ApplicationTest()
        params = ["-i", "input.txt", "-o", "output.txt", "four", "donut"]
        self.assertRaises(ApplicationError, lambda: app.run(params, no_exit=True))

    # Check when passing undefined options and arguments
    def test_calling_an_app_with_incorrect_args_should_raise_errors_part_2(self) -> None:
        app = ApplicationTest()
        params = ["-i", "input.txt", "-o", "output.txt", "one", "pretzel"]
        self.assertRaises(ApplicationError, lambda: app.run(params, no_exit=True))

    # Check options and arguments passed can be retrieved
    def test_should_be_able_to_retrieve_passed_args_and_opts(self) -> None:
        app = ApplicationTest()
        params = ["-i", "input.txt", "-o", "output.txt", "one", "donut"]
        app.run(params, no_exit=True)
        self.assertEqual("input.txt", app.get_arg("input"))
        self.assertEqual("output.txt", app.get_arg("output"))
        self.assertEqual("one", app.get_arg("amount"))
        self.assertEqual("donut", app.get_arg("item"))


# Program entry point.
if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestApplication)
    unittest.TextTestRunner(verbosity=2, failfast=True, stream=sys.stdout).run(suite)
