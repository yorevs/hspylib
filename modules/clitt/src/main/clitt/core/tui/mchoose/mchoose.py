#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib
   @package: clitt.core.tui.mchoose
      @file: mchoose.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""
from clitt.core.tui.mchoose.menu_choose import MenuChoose
from hspylib.core.enums.charset import Charset
from typing import List, Optional, TypeVar

T = TypeVar("T")


def mchoose(
    items: List[T], checked: bool = True, title: str = "Please choose among the options", output: str = None
) -> Optional[List[T]]:
    """
    Terminal UI menu choose input method.
    :param items: the provided items to choose from.
    :param checked: whether all items ate initially marked or not.
    :param title: the title to be displayed before the options.
    :param output: optional output file containing the marked items.
    :return: the list of marked items.
    """

    result = MenuChoose(title, items, checked).execute()

    if result and output:
        with open(output, "w", encoding=Charset.UTF_8.val) as f_out:
            f_out.write(" ".join(result))

    return result
