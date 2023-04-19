#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   test.tools
      @file: test_commons.py
   @created: Thu, 03 Nov 2022
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""
import sys
import unittest

from hspylib.core.tools.commons import str_to_bool, syserr, sysout


class TestCommons(unittest.TestCase):
    def test_should_return_proper_bool_value(self) -> None:
        self.assertFalse(str_to_bool(""))
        self.assertFalse(str_to_bool("0"))
        self.assertFalse(str_to_bool("off"))
        self.assertFalse(str_to_bool("no"))
        self.assertTrue(str_to_bool("1"))
        self.assertTrue(str_to_bool("true"))
        self.assertTrue(str_to_bool("True"))
        self.assertTrue(str_to_bool("on"))
        self.assertTrue(str_to_bool("yes"))

        self.assertFalse(str_to_bool("good"))
        self.assertTrue(str_to_bool("good", {"good"}))
        self.assertFalse(str_to_bool("bad", {"good"}))

    def test_shouldNotFailIfReceivedNoneValueToSysoutOrSyserr(self) -> None:
        try:
            sysout(None)
            syserr(None)
            sysout('')
            syserr('')
        except TypeError as err:
            self.fail(f"sysout/syserr raised TypeError unexpectedly => {err}")


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCommons)
    unittest.TextTestRunner(verbosity=2, failfast=True, stream=sys.stdout).run(suite)
