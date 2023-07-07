#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib
   @package: clitt.core.tui.minput
      @file: minput_utils.py
   @created: Thu, 20 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""
from clitt.core.term.screen import Screen
from hspylib.core.exception.exceptions import InvalidInputError
from typing import Any, Optional, Tuple

import re

MASK_SYMBOLS = ["#", "@", "%", "*"]

VALUE_SEPARATORS = r"[|,;]"

VALUE_SELECTORS = r"[<>]"


def detail_len(field: Any) -> int:
    """Return the length of the details, according to the form field.
    :param field: the form field to get details.
    """
    max_len = len(str(field.max_length))
    return 1 + (2 * max_len)


def mi_print(screen: Screen, text: str, prefix: str = None, field_len: int = 0, end: str = "") -> None:
    """Special menu input print.
    :param screen: the component's screen.
    :param text: the text to be printed.
    :param prefix the text to print before the text.
    :param field_len: the length of the field.
    :param end: string appended after the last value, default an empty string.
    """
    fmt = ("{}" if prefix else "") + "{:<" + str(field_len) + "} : "
    if prefix:
        screen.cursor.write(fmt.format(prefix, text), end=end)
    else:
        screen.cursor.write(fmt.format(text or ""), end=end)


def mi_print_err(screen: Screen, text: str) -> None:
    """Special menu input print error message.
    :param screen: the component's screen.
    :param text: the text to be printed.
    """
    screen.cursor.write(f"%RED%{text}%NC%")


def toggle_selected(tokenized_values: str) -> str:
    """Toggle the 'select' component value. Selects the next value on the token sequence.
    :param tokenized_values: the 'select' component tokenized values.
    """
    values = re.split(VALUE_SEPARATORS, tokenized_values)
    cur_idx = next((idx for idx, val in enumerate(values) if val.find("<") >= 0), -1)
    if cur_idx < 0:
        if len(values) > 1:
            values[1] = f"<{values[1]}>"
        else:
            values[0] = f"<{values[0]}>"
        return "|".join(values)
    unselected = list(map(lambda x: re.sub(VALUE_SELECTORS, "", x), values))
    # fmt: off
    return '|'.join([
        f'<{val}>'
        if idx == (cur_idx + 1) or ((cur_idx + 1) >= len(unselected) and idx == 0)
        else val for idx, val in enumerate(unselected)
    ])
    # fmt: on


def get_selected(tokenized_values: str) -> Optional[Tuple[int, str]]:
    """Get the selected value from the 'select' component tokens.
    :param tokenized_values: the 'select' component tokenized values.
    """
    values = re.split(VALUE_SEPARATORS, tokenized_values)
    # fmt: off
    sel_item = next((
        re.sub(VALUE_SELECTORS, '', val)
        for val in values if val.startswith('<') and val.endswith('>')
    ), values[0])
    # fmt: on
    try:
        return values.index(sel_item), sel_item
    except ValueError:
        try:
            return values.index(f"<{sel_item}>"), sel_item
        except ValueError:
            return -1, sel_item


def unpack_masked(value: str) -> Tuple[str, str]:
    """Unpack all values of the 'masked' component.
    :param value: the masked values to unpack.
    """
    if value:
        parts = re.split(VALUE_SEPARATORS, value)
        return parts[0], parts[1] if len(parts) == 2 else ""

    return "", ""


def append_masked(value: str, mask: str, keypress_value: chr) -> str:
    """Append a value to the masked field.
    :param value: the masked field current value.
    :param mask: the masked field's mask.
    :param keypress_value: the value to append (it can be a part of the mask itself).
    """
    idx = len(value)
    masked_value = value
    if idx < len(mask):
        if keypress_value == mask[idx]:
            return f"{value}{keypress_value}|{mask}"
        while idx < len(mask) and mask[idx] not in MASK_SYMBOLS:
            masked_value += mask[idx]
            idx += 1
        if mask and idx < len(mask):
            mask_re = mask_regex(mask, idx)
            if re.search(mask_re, keypress_value):
                masked_value += keypress_value
            else:
                raise InvalidInputError(f"Value '{keypress_value}' is invalid. Expecting: {mask_re}")

    return f"{masked_value}|{mask}"


def over_masked(value: str, mask: str) -> str:
    """
    Return the value to be printed by a 'masked' input field. A placeholder value will be used for unfilled values.
    :param value: the masked field current value.
    :param mask: the masked field's mask.
    """
    if value:
        over_masked_val = ""
        for idx, element in enumerate(mask):
            if element in MASK_SYMBOLS:
                over_masked_val += value[idx] if idx < len(value) else mask[idx]
            else:
                over_masked_val += element
        return over_masked_val

    return mask


def mask_regex(mask: str, idx: int) -> str:
    """Return a regex matching the index of the mask."""
    return mask[idx].replace("#", "[0-9]").replace("@", "[a-zA-Z]").replace("%", "[a-zA-Z0-9]").replace("*", ".")
