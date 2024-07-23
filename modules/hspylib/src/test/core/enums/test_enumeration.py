#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib
   test.enum
      @file: test_enumeration.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright·(c)·2024,·HSPyLib
"""

from hspylib.core.enums.enumeration import Enumeration

import sys
import unittest


class TestClass(unittest.TestCase):
    class MyIntEnum(Enumeration):
        ENUM_1 = 1
        ENUM_2 = 2
        ENUM_3 = 4
        ENUM_4 = 8

    class MyStrEnum(Enumeration):
        ENUM_a = "a"
        ENUM_b = "b"
        ENUM_c = "c"
        ENUM_d = "d"

    # TC1 - Test value of from strings.
    def test_should_convert_string_to_enum(self):
        self.assertEqual(self.MyIntEnum.ENUM_1, self.MyIntEnum.value_of("ENUM_1"))
        self.assertEqual(self.MyIntEnum.ENUM_2, self.MyIntEnum.value_of("ENUM_2"))
        self.assertEqual(self.MyIntEnum.ENUM_3, self.MyIntEnum.value_of("ENUM_3"))
        self.assertEqual(self.MyIntEnum.ENUM_4, self.MyIntEnum.value_of("ENUM_4"))

    # TC2 - Test value of from strings ignoring case.
    def test_should_convert_string_to_enum_ignoring_case(self):
        self.assertEqual(self.MyIntEnum.ENUM_1, self.MyIntEnum.value_of("enum_1"))
        self.assertEqual(self.MyIntEnum.ENUM_2, self.MyIntEnum.value_of("EnuM_2"))
        self.assertEqual(self.MyIntEnum.ENUM_3, self.MyIntEnum.value_of("ENum_3"))
        self.assertEqual(self.MyIntEnum.ENUM_4, self.MyIntEnum.value_of("enUM_4"))

    # TC3 - Test value of from strings not ignoring case.
    def test_should_not_convert_string_to_enum_when_not_ignoring_case(self):
        self.assertRaises(TypeError, self.MyIntEnum.value_of, "enum_1", ignore_case=False)
        self.assertRaises(TypeError, self.MyIntEnum.value_of, "EnuM_2", ignore_case=False)
        self.assertRaises(TypeError, self.MyIntEnum.value_of, "ENum_3", ignore_case=False)
        self.assertRaises(TypeError, self.MyIntEnum.value_of, "enUM_4", ignore_case=False)

    # TC4 - Test of value from Any
    def test_should_convert_value_to_enum(self):
        self.assertEqual(self.MyIntEnum.ENUM_1, self.MyIntEnum.of_value(1))
        self.assertEqual(self.MyIntEnum.ENUM_2, self.MyIntEnum.of_value(2))
        self.assertEqual(self.MyIntEnum.ENUM_3, self.MyIntEnum.of_value(4))
        self.assertEqual(self.MyIntEnum.ENUM_4, self.MyIntEnum.of_value(8))

    # TC5 - Test of value from Any
    def test_should_not_convert_value_to_enum_when_not_matching(self):
        self.assertRaises(TypeError, self.MyIntEnum.of_value, 0)
        self.assertRaises(TypeError, self.MyIntEnum.of_value, 3)
        self.assertRaises(TypeError, self.MyIntEnum.of_value, 5)
        self.assertRaises(TypeError, self.MyIntEnum.of_value, 7)

    # TC6 - Test of value from Any
    def test_should_convert_value_to_enum_when_ignoring_Case(self):
        self.assertEqual(self.MyStrEnum.ENUM_a, self.MyStrEnum.of_value("A", True))
        self.assertEqual(self.MyStrEnum.ENUM_b, self.MyStrEnum.of_value("B", True))
        self.assertEqual(self.MyStrEnum.ENUM_c, self.MyStrEnum.of_value("C", True))
        self.assertEqual(self.MyStrEnum.ENUM_d, self.MyStrEnum.of_value("D", True))

    # TC7 - Test of value from Any
    def test_should_not_convert_value_to_enum_when_not_ignoring_Case(self):
        self.assertRaises(TypeError, self.MyStrEnum.of_value, "A")
        self.assertRaises(TypeError, self.MyStrEnum.of_value, "B")
        self.assertRaises(TypeError, self.MyStrEnum.of_value, "C")
        self.assertRaises(TypeError, self.MyStrEnum.of_value, "D")


# Program entry point.
if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestClass)
    unittest.TextTestRunner(verbosity=2, failfast=True, stream=sys.stdout).run(suite)
