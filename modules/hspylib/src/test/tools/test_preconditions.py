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

   Copyright 2021, HSPyLib team
"""
import sys
import unittest

from core.exception.exceptions import InvalidStateError, InvalidArgumentError
from core.tools.preconditions import check_not_none, check_state, check_argument, check_element_index, \
    check_index_in_range


class TestFetch(unittest.TestCase):

    def test_should_allow_argument_that_matches(self):
        self.assertTrue(check_argument(True))

    def test_should_not_allow_argument_that_does_not_match(self):
        self.assertRaisesRegex(
            InvalidArgumentError, 'Precondition failed: Invalid argument', lambda: check_argument(False))

    def test_should_allow_state_that_matches(self):
        self.assertTrue(check_state(True))

    def test_should_not_allow_state_that_does_not_match(self):
        self.assertRaisesRegex(
            InvalidStateError, 'Precondition failed: Invalid state', lambda: check_state(False))

    def test_should_not_allow_none_reference(self):
        self.assertRaisesRegex(
            TypeError, 'Precondition failed: Null reference', lambda: check_not_none(None))

    def test_should_allow_not_none_reference(self):
        self.assertTrue(check_not_none(True))

    def test_should_allow_index_in_bounds(self):
        arr = [0, 1, 2]
        self.assertEqual(check_element_index(1, len(arr)), 1)

    def test_should_not_allow_negative_index(self):
        arr = [0, 1, 2]
        self.assertRaisesRegex(
            IndexError,
            'Precondition failed: Index is negative or out of bounds',
            lambda: check_element_index(-1, len(arr)))

    def test_should_not_allow_index_out_of_bounds(self):
        arr = [0, 1, 2]
        self.assertRaisesRegex(
            IndexError,
            'Precondition failed: Index is negative or out of bounds',
            lambda: check_element_index(4, len(arr)))

    def test_should_allow_index_in_range(self):
        arr = [0, 1, 2, 3, 4, 5]
        self.assertEqual(check_index_in_range(0, 5, len(arr)), (0, 5))

    def test_should_not_allow_negative_start(self):
        arr = [0, 1, 2]
        self.assertRaisesRegex(
            IndexError,
            'Precondition failed: Index is negative or greater than size',
            lambda: check_index_in_range(-1, 1, len(arr)))

    def test_should_not_allow_negative_end(self):
        arr = [0, 1, 2]
        self.assertRaisesRegex(
            IndexError,
            'Precondition failed: Index is negative or greater than size',
            lambda: check_index_in_range(0, -1, len(arr)))

    def test_should_not_allow_index_out_of_range(self):
        arr = [0, 1, 2]
        self.assertRaisesRegex(
            IndexError,
            'Precondition failed: Index is negative or greater than size',
            lambda: check_index_in_range(1, len(arr), len(arr)))

    def test_should_not_allow_end_less_then_start(self):
        arr = [0, 1, 2, 4, 5]
        self.assertRaisesRegex(
            IndexError,
            'Precondition failed: End is less than start',
            lambda: check_index_in_range(2, 1, len(arr)))


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFetch)
    unittest \
        .TextTestRunner(verbosity=2, failfast=True, stream=sys.stdout) \
        .run(suite)