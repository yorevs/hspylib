#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   test.tools
      @file: test_preconditions.py
   @created: Fri, 16 Jul 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
import sys
import unittest

from hspylib.core.preconditions import *


class TestPreconditions(unittest.TestCase):
    def test_should_allow_argument_that_matches(self):
        self.assertTrue(check_argument(True))

    def test_should_not_allow_argument_that_does_not_match(self):
        self.assertRaisesRegex(
            InvalidArgumentError, "Precondition failed: Invalid argument", lambda: check_argument(False)
        )

    def test_should_allow_state_that_matches(self):
        self.assertTrue(check_state(True))

    def test_should_not_allow_state_that_does_not_match(self):
        self.assertRaisesRegex(InvalidStateError, "Precondition failed: Invalid state", lambda: check_state(False))

    def test_should_not_allow_none_reference(self):
        self.assertRaisesRegex(TypeError, "Precondition failed: <None> reference found", lambda: check_not_none(None))
        self.assertRaisesRegex(
            TypeError, "Precondition failed: <None> reference found", lambda: check_not_none((10, None))
        )

    def test_should_allow_not_none_reference(self):
        self.assertTrue(check_not_none(True))

    def test_should_allow_index_in_bounds(self):
        arr = [0, 1, 2]
        self.assertEqual(check_element_index(1, arr), 1)

    def test_should_not_allow_negative_index(self):
        arr = [0, 1, 2]
        self.assertRaisesRegex(
            IndexError, "Precondition failed: Index is negative or out of bounds", lambda: check_element_index(-1, arr)
        )

    def test_should_not_allow_index_out_of_bounds(self):
        arr = [0, 1, 2]
        self.assertRaisesRegex(
            IndexError, "Precondition failed: Index is negative or out of bounds", lambda: check_element_index(4, arr)
        )

    def test_should_allow_index_in_range(self):
        arr = [0, 1, 2, 3, 4, 5]
        self.assertEqual(check_index_in_range(0, 5, arr), (0, 5))

    def test_should_not_allow_negative_start(self):
        arr = [0, 1, 2]
        self.assertRaisesRegex(
            IndexError,
            "Precondition failed: Index is negative or greater than size",
            lambda: check_index_in_range(-1, 1, arr),
        )

    def test_should_not_allow_negative_end(self):
        arr = [0, 1, 2]
        self.assertRaisesRegex(
            IndexError,
            "Precondition failed: Index is negative or greater than size",
            lambda: check_index_in_range(0, -1, arr),
        )

    def test_should_not_allow_index_out_of_range(self):
        arr = [0, 1, 2]
        self.assertRaisesRegex(
            IndexError,
            "Precondition failed: Index is negative or greater than size",
            lambda: check_index_in_range(1, len(arr), arr),
        )

    def test_should_not_allow_end_less_then_start(self):
        arr = [0, 1, 2, 4, 5]
        self.assertRaisesRegex(
            IndexError, "Precondition failed: End is less than start", lambda: check_index_in_range(2, 1, arr)
        )

    def test_should_get_the_element_value(self):
        dct = {"zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5}
        self.assertEqual(check_and_get("zero", dct), 0)
        self.assertEqual(check_and_get("one", dct), 1)
        self.assertEqual(check_and_get("two", dct), 2)
        self.assertEqual(check_and_get("three", dct), 3)
        self.assertEqual(check_and_get("four", dct), 4)
        self.assertEqual(check_and_get("five", dct), 5)

    def test_should_get_the_default_value(self):
        dct = {"zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5}
        self.assertEqual(check_and_get("six", dct, False, default=6), 6)
        self.assertEqual(check_and_get("seven", dct, False, default=7), 7)
        self.assertEqual(check_and_get("eight", dct, False), None)

    def test_should_fail_if_element_if_not_found_and_required(self):
        dct = {"zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5}
        self.assertRaisesRegex(
            InvalidArgumentError,
            "Precondition failed: Required attribute six was not found in the content dictionary",
            lambda: self.assertEqual(check_and_get("six", dct), 6),
        )


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPreconditions)
    unittest.TextTestRunner(verbosity=2, failfast=True, stream=sys.stdout).run(suite)
