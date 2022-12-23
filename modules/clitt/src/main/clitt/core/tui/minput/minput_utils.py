#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: clitt.core.tui.minput
      @file: minput_utils.py
   @created: Thu, 20 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
import re
from abc import ABC
from typing import Any, Optional, Tuple

from hspylib.core.exception.exceptions import InvalidInputError
from hspylib.core.preconditions import check_argument
from hspylib.core.tools.commons import sysout


class MInputUtils(ABC):
    """TODO"""

    @staticmethod
    def detail_len(field: Any) -> int:
        max_len = len(str(field.max_length))
        return 1 + (2 * max_len)

    @staticmethod
    def mi_print(size: int = 0, text: str = None, prepend: str = None, end: str = "") -> None:
        """TODO"""
        fmt = ("{}" if prepend else "") + "{:<" + str(size) + "} : "
        if prepend:
            sysout(fmt.format(prepend, text), end=end)
        else:
            sysout(fmt.format(text or ""), end=end)

    @staticmethod
    def toggle_selected(tokenized_values: str) -> str:
        """TODO"""
        values = tokenized_values.split("|")
        cur_idx = next((idx for idx, val in enumerate(values) if val.find("<") >= 0), -1)
        if cur_idx < 0:
            if len(values) > 1:
                values[1] = f"<{values[1]}>"
            else:
                values[0] = f"<{values[0]}>"
            return "|".join(values)
        unselected = list(map(lambda x: x.replace("<", "").replace(">", ""), values))
        # fmt: off
        return '|'.join([
            f'<{val}>'
            if idx == (cur_idx + 1) or ((cur_idx + 1) >= len(unselected) and idx == 0)
            else val for idx, val in enumerate(unselected)
        ])
        # fmt: on

    @staticmethod
    def get_selected(tokenized_values: str) -> Optional[Tuple[int, str]]:
        """TODO"""
        values = tokenized_values.split("|")
        # fmt: off
        sel_item = next((
            val.replace('<', '').replace('>', '')
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

    @staticmethod
    def unpack_masked(value: str) -> Tuple[str, str]:
        """TODO"""
        parts = value.split("|")
        check_argument(len(parts) == 2, "Invalid masked value: {}", value)
        return parts[0], parts[1]

    @staticmethod
    def append_masked(value: str, mask: str, keypress_value: chr) -> str:
        """TODO"""
        idx = len(value)
        if keypress_value == mask[idx]:
            return f"{value}{keypress_value}|{mask}"
        masked_value = value
        while idx < len(mask) and mask[idx] not in ["#", "@", "*"]:
            masked_value += mask[idx]
            idx += 1
        if mask and idx < len(mask):
            mask_regex = mask[idx].replace("#", "[0-9]").replace("@", "[a-zA-Z]").replace("*", ".")
            if re.search(mask_regex, keypress_value):
                masked_value += keypress_value
            else:
                raise InvalidInputError(f"Value {keypress_value} is not a valid value against mask: {mask}")

        return f"{masked_value}|{mask}"

    @staticmethod
    def over_masked(value: str, mask: str) -> str:
        """TODO"""
        masked_value = ""
        for idx, element in enumerate(mask):
            if element in ["#", "@", "*"]:
                masked_value += value[idx] if idx < len(value) else "_"
            else:
                masked_value += element

        return masked_value
