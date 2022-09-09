#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: hspylib
   @package: hspylib.test.tools
      @file: test_collection_filter.py
   @created: Fri, 1 Jul 2022
    @author: "<B>H</B>ugo <B>S</B>aporetti <B>J</B>unior")"
      @site: "https://github.com/yorevs/hspylib")
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

import collections
import sys
import unittest
from hspylib.core.exception.exceptions import InvalidArgumentError
from hspylib.core.tools.collection_filter import *


def get_dict() -> List[dict]:
    return [
        {'id': 0, 'name': 'hugo', 'age': 43, 'score': 9.8, 'active': True},
        {'id': 1, 'name': 'joao', 'age': 22, 'score': 2.5, 'active': True},
        {'id': 2, 'name': 'juca', 'age': 15, 'score': 4.0, 'active': True},
        {'id': 3, 'name': 'kako', 'age': 67, 'score': 3.9, 'active': True},
        {'id': 4, 'name': 'lucas', 'age': 33, 'score': 5.0, 'active': True},
        {'id': 5, 'name': 'gabits', 'age': 1, 'score': 7.8, 'active': False},
        {'id': 6, 'name': 'claudia', 'age': 34, 'score': 6.1, 'active': True},
        {'id': 7, 'name': 'be', 'age': 10, 'score': 10.0, 'active': False},
    ]


def get_deque() -> collections.deque:
    deq = collections.deque()
    list(map(deq.append, get_dict()))
    return deq


class TestCollectionFilter(unittest.TestCase):

    def setUp(self) -> None:
        self.arr = get_dict()
        self.deq = get_deque()
        self.f = CollectionFilter()

    def test_should_filter_less_than(self):
        self.f.apply_filter('f1', 'score', FilterConditions.LESS_THAN, 5.0)
        expected = [
            {'active': True, 'age': 22, 'id': 1, 'name': 'joao', 'score': 2.5},
            {'active': True, 'age': 15, 'id': 2, 'name': 'juca', 'score': 4.0},
            {'active': True, 'age': 67, 'id': 3, 'name': 'kako', 'score': 3.9}
        ]
        result = self.f.filter(self.arr)
        self.assertListEqual(result, expected)
        result = self.f.filter(list(self.deq))
        self.assertListEqual(result, expected)

    def test_should_filter_less_than_or_equals_to(self):
        self.f.apply_filter('f1', 'score', FilterConditions.LESS_THAN_OR_EQUALS_TO, 5.0)
        expected = [
            {'active': True, 'age': 22, 'id': 1, 'name': 'joao', 'score': 2.5},
            {'active': True, 'age': 15, 'id': 2, 'name': 'juca', 'score': 4.0},
            {'active': True, 'age': 67, 'id': 3, 'name': 'kako', 'score': 3.9},
            {'active': True, 'age': 33, 'id': 4, 'name': 'lucas', 'score': 5.0},
        ]
        result = self.f.filter(self.arr)
        self.assertListEqual(result, expected)
        result = self.f.filter(list(self.deq))
        self.assertListEqual(result, expected)

    def test_should_filter_greater_than(self):
        self.f.apply_filter('f1', 'score', FilterConditions.GREATER_THAN, 5.0)
        expected = [
            {'active': True, 'age': 43, 'id': 0, 'name': 'hugo', 'score': 9.8},
            {'active': False, 'age': 1, 'id': 5, 'name': 'gabits', 'score': 7.8},
            {'active': True, 'age': 34, 'id': 6, 'name': 'claudia', 'score': 6.1},
            {'active': False, 'age': 10, 'id': 7, 'name': 'be', 'score': 10.0}
        ]
        result = self.f.filter(self.arr)
        self.assertListEqual(result, expected)
        result = self.f.filter(list(self.deq))
        self.assertListEqual(result, expected)

    def test_should_filter_greater_than_or_equals_to(self):
        self.f.apply_filter('f1', 'score', FilterConditions.GREATER_THAN_OR_EQUALS_TO, 5.0)
        expected = [
            {'active': True, 'age': 43, 'id': 0, 'name': 'hugo', 'score': 9.8},
            {'active': True, 'age': 33, 'id': 4, 'name': 'lucas', 'score': 5.0},
            {'active': False, 'age': 1, 'id': 5, 'name': 'gabits', 'score': 7.8},
            {'active': True, 'age': 34, 'id': 6, 'name': 'claudia', 'score': 6.1},
            {'active': False, 'age': 10, 'id': 7, 'name': 'be', 'score': 10.0}
        ]
        result = self.f.filter(self.arr)
        self.assertListEqual(result, expected)
        result = self.f.filter(list(self.deq))
        self.assertListEqual(result, expected)

    def test_should_filter_equals_to(self):
        self.f.apply_filter('f1', 'active', FilterConditions.EQUALS_TO, False)
        self.f.apply_filter('f2', 'name', FilterConditions.EQUALS_TO, 'gabits')
        expected = [
            {'active': False, 'age': 1, 'id': 5, 'name': 'gabits', 'score': 7.8}
        ]
        result = self.f.filter(self.arr)
        self.assertListEqual(result, expected)
        result = self.f.filter(list(self.deq))
        self.assertListEqual(result, expected)

    def test_should_filter_different_from(self):
        self.f.apply_filter('f1', 'active', FilterConditions.DIFFERENT_FROM, False)
        self.f.apply_filter('f2', 'name', FilterConditions.EQUALS_TO, 'hugo')
        expected = [
            {'active': True, 'age': 43, 'id': 0, 'name': 'hugo', 'score': 9.8}
        ]
        result = self.f.filter(self.arr)
        self.assertListEqual(result, expected)
        result = self.f.filter(list(self.deq))
        self.assertListEqual(result, expected)

    def test_should_filter_contains(self):
        self.f.apply_filter('f1', 'name', FilterConditions.CONTAINS, 'u')
        expected = [
            {'active': True, 'age': 43, 'id': 0, 'name': 'hugo', 'score': 9.8},
            {'active': True, 'age': 15, 'id': 2, 'name': 'juca', 'score': 4.0},
            {'active': True, 'age': 33, 'id': 4, 'name': 'lucas', 'score': 5.0},
            {'active': True, 'age': 34, 'id': 6, 'name': 'claudia', 'score': 6.1}
        ]
        result = self.f.filter(self.arr)
        self.assertListEqual(result, expected)
        result = self.f.filter(list(self.deq))
        self.assertListEqual(result, expected)

    def test_should_filter_does_not_contain(self):
        self.f.apply_filter('f1', 'name', FilterConditions.DOES_NOT_CONTAIN, 'u')
        expected = [
            {'active': True, 'age': 22, 'id': 1, 'name': 'joao', 'score': 2.5},
            {'active': True, 'age': 67, 'id': 3, 'name': 'kako', 'score': 3.9},
            {'active': False, 'age': 1, 'id': 5, 'name': 'gabits', 'score': 7.8},
            {'active': False, 'age': 10, 'id': 7, 'name': 'be', 'score': 10.0}
        ]
        result = self.f.filter(self.arr)
        self.assertListEqual(result, expected)
        result = self.f.filter(list(self.deq))
        self.assertListEqual(result, expected)

    def test_should_filter_is(self):
        self.f.apply_filter('f1', 'active', FilterConditions.IS, True)
        expected = [
            {'active': True, 'age': 43, 'id': 0, 'name': 'hugo', 'score': 9.8},
            {'active': True, 'age': 22, 'id': 1, 'name': 'joao', 'score': 2.5},
            {'active': True, 'age': 15, 'id': 2, 'name': 'juca', 'score': 4.0},
            {'active': True, 'age': 67, 'id': 3, 'name': 'kako', 'score': 3.9},
            {'active': True, 'age': 33, 'id': 4, 'name': 'lucas', 'score': 5.0},
            {'active': True, 'age': 34, 'id': 6, 'name': 'claudia', 'score': 6.1}
        ]
        result = self.f.filter(self.arr)
        self.assertListEqual(result, expected)
        result = self.f.filter(list(self.deq))
        self.assertListEqual(result, expected)

    def test_should_filter_is_not(self):
        self.f.apply_filter('f1', 'active', FilterConditions.IS_NOT, True)
        expected = [
            {'active': False, 'age': 1, 'id': 5, 'name': 'gabits', 'score': 7.8},
            {'active': False, 'age': 10, 'id': 7, 'name': 'be', 'score': 10.0}
        ]
        result = self.f.filter(self.arr)
        self.assertListEqual(result, expected)
        result = self.f.filter(list(self.deq))
        self.assertListEqual(result, expected)

    def test_should_filter_mixed_filters(self):
        self.f.apply_filter('f1', 'active', FilterConditions.IS, True)
        self.f.apply_filter('f2', 'age', FilterConditions.GREATER_THAN, 18)
        self.f.apply_filter('f3', 'score', FilterConditions.LESS_THAN, 5.0)
        self.f.apply_filter('f4', 'age', FilterConditions.GREATER_THAN_OR_EQUALS_TO, 30)
        expected = [
            {'active': True, 'age': 67, 'id': 3, 'name': 'kako', 'score': 3.9}
        ]
        result = self.f.filter(self.arr)
        self.assertListEqual(result, expected)
        result = self.f.filter(list(self.deq))
        self.assertListEqual(result, expected)

    def test_should_not_allow_repeated_filter_names(self):
        self.f.apply_filter('f1', 'active', FilterConditions.IS, True)
        self.assertRaisesRegex(
            InvalidArgumentError,
            'Filter f1 already exists!',
            lambda: self.f.apply_filter('f1', 'age', FilterConditions.GREATER_THAN, 18))

    def test_should_not_allow_repeated_filter_conditions(self):
        self.f.apply_filter('f1', 'active', FilterConditions.IS, True)
        self.f.apply_filter('f2', 'active', FilterConditions.IS, True)
        self.assertEqual(self.f.size(), 1)

    def test_should_discard_filter(self):
        self.f.apply_filter('f1', 'active', FilterConditions.IS, True)
        self.f.apply_filter('f2', 'age', FilterConditions.GREATER_THAN, 18)
        self.f.apply_filter('f3', 'score', FilterConditions.LESS_THAN, 5.0)
        self.f.apply_filter('f4', 'age', FilterConditions.GREATER_THAN_OR_EQUALS_TO, 30)
        expected = [
            {'active': True, 'age': 67, 'id': 3, 'name': 'kako', 'score': 3.9}
        ]
        result = self.f.filter(self.arr)
        self.assertListEqual(result, expected)
        result = self.f.filter(list(self.deq))
        self.assertListEqual(result, expected)
        self.f.discard('f4')
        expected = [
            {'active': True, 'age': 22, 'id': 1, 'name': 'joao', 'score': 2.5},
            {'active': True, 'age': 67, 'id': 3, 'name': 'kako', 'score': 3.9}
        ]
        result = self.f.filter(self.arr)
        self.assertListEqual(result, expected)

    def test_should_filter_inverse(self):
        self.f.apply_filter('f1', 'active', FilterConditions.IS, True)
        expected = [
            {'active': False, 'age': 1, 'id': 5, 'name': 'gabits', 'score': 7.8},
            {'active': False, 'age': 10, 'id': 7, 'name': 'be', 'score': 10.0}
        ]
        result = self.f.filter_inverse(self.arr)
        self.assertListEqual(result, expected)
        result = self.f.filter_inverse(list(self.deq))
        self.assertListEqual(result, expected)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCollectionFilter)
    unittest \
        .TextTestRunner(verbosity=2, failfast=True, stream=sys.stdout) \
        .run(suite)
