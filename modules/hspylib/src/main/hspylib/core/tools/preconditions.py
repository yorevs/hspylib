#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: main.tools
      @file: preconditions.py
   @created: Fri, 16 Jul 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

from typing import Tuple, TypeVar

from hspylib.core.exception.exceptions import InvalidArgumentError, InvalidStateError

T = TypeVar('T')


def check_argument(expression: bool, error_message: str = None, *args) -> bool:
    """Ensures the truth of an expression involving one or more parameters to the calling method."""
    if not expression:
        raise InvalidArgumentError(
            error_message.format(*args) if error_message else 'Precondition failed: Invalid argument')

    return expression


def check_state(expression: bool, error_message: str = None, *args) -> bool:
    """Ensures the truth of an expression involving the state of the calling instance, but not involving
    any parameters to the calling method."""
    if not expression:
        raise InvalidStateError(
            error_message.format(*args) if error_message else 'Precondition failed: Invalid state')

    return expression


def check_not_none(reference: T, error_message: str = None, *args) -> T:
    """Ensures that an object reference passed as a parameter to the calling method is not None."""
    if reference is None:
        raise TypeError(
            error_message.format(*args) if error_message else 'Precondition failed: Null reference')
    return reference


def check_element_index(index: int, size: int, desc: str = None) -> int:
    """Ensures that index specifies a valid element in an array, list or string of size size."""

    if size < 0:
        raise InvalidArgumentError('Size is negative')
    if index < 0 or index >= size:
        raise IndexError(desc or 'Precondition failed: Index is negative or out of bounds')

    return index


def check_index_in_range(start: int, end: int, size: int, desc: str = None) -> Tuple[int, int]:
    """Ensures that start and end specify a valid positions in an array, list or string of size size, and
    are in order."""
    if size < 0:
        raise InvalidArgumentError('Size is negative')
    if start < 0 or end < 0 or start >= size or end >= size:
        raise IndexError(desc or 'Precondition failed: Index is negative or greater than size')
    if end < start:
        raise IndexError(desc or 'Precondition failed: End is less than start')

    return start, end
