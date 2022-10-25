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
from typing import List

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

def get_set() -> Set[tuple]:
    zet = set()
    list(map(lambda v: zet.add(tuple(v.items())), get_dict()))
    return zet


class TestCollectionFilter(unittest.TestCase):

    def setUp(self) -> None:
        self.arr = get_dict()
        self.deq = get_deque()
        self.zet = get_set()
        self.f = CollectionFilter()

    def test_should_filter_less_than(self) -> None:
        self.f.apply_filter('f1', 'score', FilterCondition.LESS_THAN, 5.0)
        expected = [
            {'active': True, 'age': 22, 'id': 1, 'name': 'joao', 'score': 2.5},
            {'active': True, 'age': 15, 'id': 2, 'name': 'juca', 'score': 4.0},
            {'active': True, 'age': 67, 'id': 3, 'name': 'kako', 'score': 3.9}
        ]
        result = self.f.filter(self.arr)
        self.assertListEqual(list(result), expected)
        result = self.f.filter(self.deq)
        self.assertListEqual(list(result), expected)
        result = self.f.filter(self.zet)
        self.assertTrue(all(d in expected for d in [{k: v for k, v in e} for e in result]))

    def test_should_filter_less_than_or_equals_to(self) -> None:
        self.f.apply_filter('f1', 'score', FilterCondition.LESS_THAN_OR_EQUALS_TO, 5.0)
        expected = [
            {'active': True, 'age': 22, 'id': 1, 'name': 'joao', 'score': 2.5},
            {'active': True, 'age': 15, 'id': 2, 'name': 'juca', 'score': 4.0},
            {'active': True, 'age': 67, 'id': 3, 'name': 'kako', 'score': 3.9},
            {'active': True, 'age': 33, 'id': 4, 'name': 'lucas', 'score': 5.0},
        ]
        result = self.f.filter(self.arr)
        self.assertListEqual(list(result), expected)
        result = self.f.filter(self.deq)
        self.assertListEqual(list(result), expected)
        result = self.f.filter(self.zet)
        self.assertTrue(all(d in expected for d in [{k: v for k, v in e} for e in result]))

    def test_should_filter_greater_than(self) -> None:
        self.f.apply_filter('f1', 'score', FilterCondition.GREATER_THAN, 5.0)
        expected = [
            {'active': True, 'age': 43, 'id': 0, 'name': 'hugo', 'score': 9.8},
            {'active': False, 'age': 1, 'id': 5, 'name': 'gabits', 'score': 7.8},
            {'active': True, 'age': 34, 'id': 6, 'name': 'claudia', 'score': 6.1},
            {'active': False, 'age': 10, 'id': 7, 'name': 'be', 'score': 10.0}
        ]
        result = self.f.filter(self.arr)
        self.assertListEqual(list(result), expected)
        result = self.f.filter(self.deq)
        self.assertListEqual(list(result), expected)
        result = self.f.filter(self.zet)
        self.assertTrue(all(d in expected for d in [{k: v for k, v in e} for e in result]))

    def test_should_filter_greater_than_or_equals_to(self) -> None:
        self.f.apply_filter('f1', 'score', FilterCondition.GREATER_THAN_OR_EQUALS_TO, 5.0)
        expected = [
            {'active': True, 'age': 43, 'id': 0, 'name': 'hugo', 'score': 9.8},
            {'active': True, 'age': 33, 'id': 4, 'name': 'lucas', 'score': 5.0},
            {'active': False, 'age': 1, 'id': 5, 'name': 'gabits', 'score': 7.8},
            {'active': True, 'age': 34, 'id': 6, 'name': 'claudia', 'score': 6.1},
            {'active': False, 'age': 10, 'id': 7, 'name': 'be', 'score': 10.0}
        ]
        result = self.f.filter(self.arr)
        self.assertListEqual(list(result), expected)
        result = self.f.filter(self.deq)
        self.assertListEqual(list(result), expected)
        result = self.f.filter(self.zet)
        self.assertTrue(all(d in expected for d in [{k: v for k, v in e} for e in result]))

    def test_should_filter_equals_to(self) -> None:
        self.f.apply_filter('f1', 'active', FilterCondition.EQUALS_TO, False)
        self.f.apply_filter('f2', 'name', FilterCondition.EQUALS_TO, 'gabits')
        expected = [
            {'active': False, 'age': 1, 'id': 5, 'name': 'gabits', 'score': 7.8}
        ]
        result = self.f.filter(self.arr)
        self.assertListEqual(list(result), expected)
        result = self.f.filter(self.deq)
        self.assertListEqual(list(result), expected)
        result = self.f.filter(self.zet)
        self.assertTrue(all(d in expected for d in [{k: v for k, v in e} for e in result]))

    def test_should_filter_different_from(self) -> None:
        self.f.apply_filter('f1', 'active', FilterCondition.DIFFERENT_FROM, False)
        self.f.apply_filter('f2', 'name', FilterCondition.EQUALS_TO, 'hugo')
        expected = [
            {'active': True, 'age': 43, 'id': 0, 'name': 'hugo', 'score': 9.8}
        ]
        result = self.f.filter(self.arr)
        self.assertListEqual(list(result), expected)
        result = self.f.filter(self.deq)
        self.assertListEqual(list(result), expected)
        result = self.f.filter(self.zet)
        self.assertTrue(all(d in expected for d in [{k: v for k, v in e} for e in result]))

    def test_should_filter_contains(self) -> None:
        self.f.apply_filter('f1', 'name', FilterCondition.CONTAINS, 'u')
        expected = [
            {'active': True, 'age': 43, 'id': 0, 'name': 'hugo', 'score': 9.8},
            {'active': True, 'age': 15, 'id': 2, 'name': 'juca', 'score': 4.0},
            {'active': True, 'age': 33, 'id': 4, 'name': 'lucas', 'score': 5.0},
            {'active': True, 'age': 34, 'id': 6, 'name': 'claudia', 'score': 6.1}
        ]
        result = self.f.filter(self.arr)
        self.assertListEqual(list(result), expected)
        result = self.f.filter(self.deq)
        self.assertListEqual(list(result), expected)
        result = self.f.filter(self.zet)
        self.assertTrue(all(d in expected for d in [{k: v for k, v in e} for e in result]))

    def test_should_filter_does_not_contain(self) -> None:
        self.f.apply_filter('f1', 'name', FilterCondition.DOES_NOT_CONTAIN, 'u')
        expected = [
            {'active': True, 'age': 22, 'id': 1, 'name': 'joao', 'score': 2.5},
            {'active': True, 'age': 67, 'id': 3, 'name': 'kako', 'score': 3.9},
            {'active': False, 'age': 1, 'id': 5, 'name': 'gabits', 'score': 7.8},
            {'active': False, 'age': 10, 'id': 7, 'name': 'be', 'score': 10.0}
        ]
        result = self.f.filter(self.arr)
        self.assertListEqual(list(result), expected)
        result = self.f.filter(self.deq)
        self.assertListEqual(list(result), expected)
        result = self.f.filter(self.zet)
        self.assertTrue(all(d in expected for d in [{k: v for k, v in e} for e in result]))

    def test_should_filter_is(self) -> None:
        self.f.apply_filter('f1', 'active', FilterCondition.IS, True)
        expected = [
            {'active': True, 'age': 43, 'id': 0, 'name': 'hugo', 'score': 9.8},
            {'active': True, 'age': 22, 'id': 1, 'name': 'joao', 'score': 2.5},
            {'active': True, 'age': 15, 'id': 2, 'name': 'juca', 'score': 4.0},
            {'active': True, 'age': 67, 'id': 3, 'name': 'kako', 'score': 3.9},
            {'active': True, 'age': 33, 'id': 4, 'name': 'lucas', 'score': 5.0},
            {'active': True, 'age': 34, 'id': 6, 'name': 'claudia', 'score': 6.1}
        ]
        result = self.f.filter(self.arr)
        self.assertListEqual(list(result), expected)
        result = self.f.filter(self.deq)
        self.assertListEqual(list(result), expected)
        result = self.f.filter(self.zet)
        self.assertTrue(all(d in expected for d in [{k: v for k, v in e} for e in result]))

    def test_should_filter_is_not(self) -> None:
        self.f.apply_filter('f1', 'active', FilterCondition.IS_NOT, True)
        expected = [
            {'active': False, 'age': 1, 'id': 5, 'name': 'gabits', 'score': 7.8},
            {'active': False, 'age': 10, 'id': 7, 'name': 'be', 'score': 10.0}
        ]
        result = self.f.filter(self.arr)
        self.assertListEqual(list(result), expected)
        result = self.f.filter(self.deq)
        self.assertListEqual(list(result), expected)
        result = self.f.filter(self.zet)
        self.assertTrue(all(d in expected for d in [{k: v for k, v in e} for e in result]))

    def test_should_filter_mixed_filters(self) -> None:
        self.f.apply_filter('f1', 'active', FilterCondition.IS, True)
        self.f.apply_filter('f2', 'age', FilterCondition.GREATER_THAN, 18)
        self.f.apply_filter('f3', 'score', FilterCondition.LESS_THAN, 5.0)
        self.f.apply_filter('f4', 'age', FilterCondition.GREATER_THAN_OR_EQUALS_TO, 30)
        expected = [
            {'active': True, 'age': 67, 'id': 3, 'name': 'kako', 'score': 3.9}
        ]
        result = self.f.filter(self.arr)
        self.assertListEqual(list(result), expected)
        result = self.f.filter(self.deq)
        self.assertListEqual(list(result), expected)
        result = self.f.filter(self.zet)
        self.assertTrue(all(d in expected for d in [{k: v for k, v in e} for e in result]))

    def test_should_not_allow_repeated_filter_names(self) -> None:
        self.f.apply_filter('f1', 'active', FilterCondition.IS, True)
        self.assertRaisesRegex(
            InvalidArgumentError,
            'Filter f1 already exists!',
            lambda: self.f.apply_filter('f1', 'age', FilterCondition.GREATER_THAN, 18))

    def test_should_not_allow_repeated_filter_conditions(self) -> None:
        self.f.apply_filter('f1', 'active', FilterCondition.IS, True)
        self.f.apply_filter('f2', 'active', FilterCondition.IS, True)
        self.assertEqual(len(self.f), 1)

    def test_should_discard_filter(self) -> None:
        self.f.apply_filter('f1', 'active', FilterCondition.IS, True)
        self.f.apply_filter('f2', 'age', FilterCondition.GREATER_THAN, 18)
        self.f.apply_filter('f3', 'score', FilterCondition.LESS_THAN, 5.0)
        self.f.apply_filter('f4', 'age', FilterCondition.GREATER_THAN_OR_EQUALS_TO, 30)
        expected = [
            {'active': True, 'age': 67, 'id': 3, 'name': 'kako', 'score': 3.9}
        ]
        result = self.f.filter(self.arr)
        self.assertListEqual(list(result), expected)
        result = self.f.filter(self.deq)
        self.assertListEqual(list(result), expected)
        result = self.f.filter(self.zet)
        self.assertTrue(all(d in expected for d in [{k: v for k, v in e} for e in result]))
        self.f.discard('f4')
        expected = [
            {'active': True, 'age': 22, 'id': 1, 'name': 'joao', 'score': 2.5},
            {'active': True, 'age': 67, 'id': 3, 'name': 'kako', 'score': 3.9}
        ]
        result = self.f.filter(self.arr)
        self.assertListEqual(list(result), expected)

    def test_should_filter_inverse(self) -> None:
        self.f.apply_filter('f1', 'active', FilterCondition.IS, True)
        expected = [
            {'active': False, 'age': 1, 'id': 5, 'name': 'gabits', 'score': 7.8},
            {'active': False, 'age': 10, 'id': 7, 'name': 'be', 'score': 10.0}
        ]
        result = self.f.filter_inverse(self.arr)
        self.assertListEqual(list(result), expected)
        result = self.f.filter_inverse(self.deq)
        self.assertListEqual(list(result), expected)
        result = self.f.filter_inverse(self.zet)
        self.assertTrue(all(d in expected for d in [{k: v for k, v in e} for e in result]))


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCollectionFilter)
    unittest \
        .TextTestRunner(verbosity=2, failfast=True, stream=sys.stdout) \
        .run(suite)
