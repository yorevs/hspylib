#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   hspylib.main.hspylib.addons.appman.templates
      @file: tpl-test_main.py
   @created: Tue, 1 Jun 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

import logging as log
import os
import sys
import unittest

from hspylib.core.config.app_config import AppConfigs
from hspylib.core.tools.commons import dirname

TEST_DIR = dirname(__file__)


class TestMain(unittest.TestCase):

    # Setup tests
    def setUp(self):
        resource_dir = '{}/resources'.format(TEST_DIR)
        os.environ['ACTIVE_PROFILE'] = "test"
        self.configs = AppConfigs(
            source_root=TEST_DIR, resource_dir=resource_dir, log_dir=resource_dir
        )
        self.assertIsNotNone(self.configs)
        self.assertIsNotNone(AppConfigs.INSTANCE)
        log.info(self.configs)

    # Teardown tests
    def tearDown(self):
        pass

    # TEST CASES ----------

    def test_should_test_something(self):
        pass


# Program entry point.
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMain)
    unittest \
        .TextTestRunner(verbosity=2, failfast=True, stream=sys.stdout) \
        .run(suite)
