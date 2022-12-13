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

   Copyright 2022, HSPyLib team
"""

from hspylib.core.exception.exceptions import InvalidArgumentError, InvalidStateError
from typing import Any, Optional, Tuple, TypeVar

T = TypeVar("T")


def check_argument(expression: bool, error_message: str = None, *args) -> bool:
    """Ensures the truth of an expression involving one or more parameters to the calling method."""
    if not expression:
        raise InvalidArgumentError(
            error_message.format(*args) if error_message else "Precondition failed: Invalid argument"
        )

    return expression


def check_state(expression: bool, error_message: str = None, *args) -> bool:
    """Ensures the truth of an expression involving the state of the calling instance, but not involving
    any parameters to the calling method."""
    if not expression:
        raise InvalidStateError(error_message.format(*args) if error_message else "Precondition failed: Invalid state")

    return expression


def check_not_none(references: T | Tuple[T], error_message: str = None, *args) -> T:
    """Ensures that an object reference passed as a parameter to the calling method is not None."""
    if isinstance(references, Tuple):
        if not all(ref is not None for ref in references):
            raise TypeError(
                error_message.format(*args) if error_message else "Precondition failed: <None> reference found"
            )
    if references is None:
        raise TypeError(error_message.format(*args) if error_message else "Precondition failed: <None> reference found")
    return references


def check_element_index(index: int, array: list, desc: str = None) -> int:
    """Ensures that index specifies a valid element in an array, list or string of size size."""

    size = len(array)
    if size < 0:
        raise InvalidArgumentError("Size is negative")
    if index < 0 or index >= size:
        raise IndexError(desc or "Precondition failed: Index is negative or out of bounds")

    return index


def check_index_in_range(start: int, end: int, array: list, desc: str = None) -> Tuple[int, int]:
    """Ensures that start and end specify a valid positions in an array, list or string of size size, and
    are in order."""

    size = len(array)
    if size < 0:
        raise InvalidArgumentError("Size is negative")
    if start < 0 or end < 0 or start >= size or end >= size:
        raise IndexError(desc or "Precondition failed: Index is negative or greater than size")
    if end < start:
        raise IndexError(desc or "Precondition failed: End is less than start")

    return start, end


def check_and_get(
    element_name: str, content_dict: dict = None, required: bool = True, default: Any = None
) -> Optional[Any]:
    """Ensures that the element is in the content dictionary. If it is required and not found, an exception will be
    raised. If it is not found and not required, the default value is returned. If the element is found, then, it's a
    value is returned."""

    if content_dict and element_name in content_dict:
        return content_dict[element_name]

    if required:
        raise InvalidArgumentError(
            f"Precondition failed: Required attribute {element_name} was not found in the content dictionary"
        )

    return default
