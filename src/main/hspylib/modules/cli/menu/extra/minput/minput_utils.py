#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.main.hspylib.modules.cli.menu.extra.minput
      @file: minput_utils.py
   @created: Thu, 20 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

from abc import ABC
from typing import Optional, Tuple, Any
from hspylib.modules.cli.vt100.vt_codes import vt_print



class MInputUtils(ABC):
    @staticmethod
    def detail_len(field: Any) -> int:
        max_len = len(str(field.max_length))
        return 1 + (2 * max_len)

    @staticmethod
    def mi_print(size: int, text: str, prepend: str = None, end: str = '') -> None:
        fmt = ('{}' if prepend else '') + "{:<" + str(size) + "} : "
        if prepend:
            vt_print(fmt.format(prepend, text), end=end)
        else:
            vt_print(fmt.format(text), end=end)

    @staticmethod
    def toggle_selected(tokenized_values: str) -> str:
        values = tokenized_values.split('|')
        cur_idx = next((idx for idx, val in enumerate(values) if val.find('<') >= 0), -1)
        if cur_idx < 0:
            if len(values) > 1:
                values[1] = f'<{values[1]}>'
            else:
                values[0] = f'<{values[0]}>'
            return '|'.join(values)
        else:
            unselected = list(map(lambda x: x.replace('<', '').replace('>', ''), values))
            # @formatter:off
            return '|'.join([
                f'<{val}>'
                if
                idx == (cur_idx + 1)
                or ((cur_idx + 1) >= len(unselected) and idx == 0)
                else
                val
                for idx, val in enumerate(unselected)
            ])
            # @formatter:on

    @staticmethod
    def get_selected(tokenized_values: str) -> Optional[Tuple[int, str]]:
        values = tokenized_values.split('|')
        # @formatter:off
        sel_item = next(
            (
                val.replace('<', '').replace('>', '')
                for val in values if val.startswith('<') and val.endswith('>')
            ), values[0]
        )
        # @formatter:on
        try:
            return values.index(sel_item), sel_item
        except ValueError:
            try:
                return values.index(f"<{sel_item}>"), sel_item
            except ValueError:
                return -1, sel_item
