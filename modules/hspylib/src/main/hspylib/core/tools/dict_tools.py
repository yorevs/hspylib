#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: main.tools
      @file: dict_tools.py
   @created: Thu, 03 May 2022
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
from typing import Any, Dict, Iterable, List, Optional, Tuple


def search_dict(root_element: dict, search_path: str, parent_key="", sep=".") -> Optional[Any]:
    """
    TODO
    :param root_element:
    :param search_path:
    :param parent_key:
    :param sep:
    :return:
    """
    found = search_path == parent_key
    el = None
    if not found and isinstance(root_element, dict):
        for key, value in root_element.items():
            if found:
                break
            el_path = parent_key + sep + key if parent_key else key
            if search_path == el_path:
                found, el = True, value
                break
            if isinstance(value, dict):
                found, el = search_dict(value, search_path, el_path, sep=sep)
            elif isinstance(value, list):
                for next_val in value:
                    found, el = search_dict(next_val, search_path, el_path, sep=sep)
            # Skip if the element is a leaf

    return found, el


def flatten_dict(dictionary: dict, parent_key="", sep=".") -> dict:
    """Flatten a dictionary and all it's items.
    :param dictionary: The dictionary to be flattened
    :param parent_key: The parent key name
    :param sep: The separator between keys
    :return:
    """
    flat_dict = {}
    for key, value in dictionary.items():
        new_key = parent_key + sep + key if parent_key else key
        if isinstance(value, dict):
            flat_dict.update(flatten_dict(value, new_key, sep=sep).items())
        else:
            flat_dict.update({new_key: value})

    return flat_dict


def merge(list_of_dicts: List[Dict] | Tuple[Dict]) -> dict:
    """Merge a list of iterables of dicts into a single dictionary.
    :param list_of_dicts: The list of iterables to be merged
    """
    return {a: av for d in list_of_dicts for a, av in d.items()}


def intersect(left_dict: Iterable, right_dict: Iterable) -> Iterable:
    """Intersect two iterables of dicts into a single dictionary.
    :param left_dict: the left side dictionary
    :param right_dict: the right side dictionary
    """
    return type(left_dict)([value for value in left_dict if value in right_dict])


def get_or_default(options: tuple | list, index: int, default_value: Any = None) -> Optional[Any]:
    """Retrieve an item from the options list or default_value if index is out of range
    :param options: The available list of options
    :param index: The index of the item
    :param default_value: The default value if the index is out of range
    """
    return options[index] if index < len(options) else default_value


def get_or_default_by_key(options: dict, key: str, default_value: Any = None) -> Optional[Any]:
    """Retrieve an item from the options list or default_value if key was not found
    :param options: The available list of options
    :param key: The key of the item
    :param default_value: The default value if the index is not found
    """
    return options[key] if key in options else default_value
