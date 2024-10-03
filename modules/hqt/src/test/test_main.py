#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib-Hqt
   @package: test.hqt
      @file: tpl-test_main.py
   @created: Tue, 1 Jun 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright·(c)·2024,·HSPyLib
"""

import sys
import unittest

from hspylib.core.tools.commons import dirname

TEST_DIR = dirname(__file__)


class TestMain(unittest.TestCase):
    # Setup tests
    def setUp(self):
        pass

    # Teardown tests
    def tearDown(self):
        pass

    # TEST CASES ----------

    def test_should_test_something(self):
        pass


# Program entry point.
if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMain)
    unittest.TextTestRunner(verbosity=2, failfast=True, stream=sys.stdout).run(suite)
