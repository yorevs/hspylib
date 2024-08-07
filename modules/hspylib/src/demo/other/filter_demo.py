#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib
   @package: demo.other
      @file: filter_demo.py
   @created: Wed, 8 Jun 2022
    @author: "<B>H</B>ugo <B>S</B>aporetti <B>J</B>unior
      @site: "https://github.com/yorevs/hspylib")
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright·(c)·2024,·HSPyLib
"""

from hspylib.core.collection_filter import CollectionFilter, FilterCondition
from typing import List

import collections


class Record:
    @staticmethod
    def of(items: List[dict]) -> List["Record"]:
        return list(map(Record, items))

    def __init__(self, item: dict):
        self.id = item["id"]
        self.name = item["name"]
        self.age = item["age"]
        self.score = item["score"]
        self.active = item["active"]

    def __str__(self):
        return f"Record: {str(self.__dict__)}"

    def __repr__(self):
        return str(self)


def example1() -> List[dict]:
    return [
        {"id": 0, "name": "hugo", "age": 43, "score": 9.8, "active": True},
        {"id": 1, "name": "joao", "age": 22, "score": 2.5, "active": True},
        {"id": 2, "name": "juca", "age": 15, "score": 4.0, "active": True},
        {"id": 3, "name": "kako", "age": 67, "score": 3.9, "active": True},
        {"id": 4, "name": "lucas", "age": 33, "score": 5.0, "active": True},
        {"id": 5, "name": "gabits", "age": 1, "score": 7.8, "active": False},
        {"id": 6, "name": "claudia", "age": 34, "score": 6.1, "active": True},
        {"id": 7, "name": "be", "age": 10, "score": 10.0, "active": False},
    ]


def example2() -> List[Record]:
    return Record.of(example1())


def example3() -> collections.deque:
    deq = collections.deque()
    list(map(deq.append, example1()))
    return deq


if __name__ == "__main__":
    arr = example1()
    records = example2()
    deq = example3()
    f = CollectionFilter()
    f.apply_filter("f1", "score", FilterCondition.GREATER_THAN_OR_EQUALS_TO, 5.0)
    f.apply_filter("f2", "active", FilterCondition.IS, True)
    f.apply_filter("f3", "name", FilterCondition.CONTAINS, "u")
    f.apply_filter("f4", "age", FilterCondition.LESS_THAN_OR_EQUALS_TO, 40)
    print(f"\n### Using List[dict] => Filters({type(arr)}): {f}\n")
    print("\n".join([str(e) for e in f.filter(arr)]))
    print(f"\n### Using List[Record] => Filters({type(records)}): {f}\n")
    print("\n".join([str(e) for e in f.filter(records)]))
    print(f"\n### Using Deque => Filters({type(deq)}): {f}\n")
    print("\n".join([str(e) for e in f.filter(list(deq))]))
    print(f"\n### Reverse => Filters({type(arr)}): {f}\n")
    print("\n".join([str(e) for e in f.filter_inverse(list(arr))]))
