#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib
   @package: hspylib.modules.application.argparse
      @file: arguments_builder.py
   @created: Thu, 14 Feb 2022
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""
from argparse import ArgumentParser
from functools import partial
from hspylib.modules.application.parser_action import ParserAction
from typing import Any, Union


class ArgumentsBuilder:
    """TODO"""

    def __init__(self, arg_parser: ArgumentParser):
        self._arg_parser = arg_parser

    def argument(
        self,
        name: str,
        help_string: str = None,
        choices: list = None,
        nargs: Union[str, int] = None,
        action: ParserAction = ParserAction.STORE,
        default: Any = None,
    ) -> "ArgumentsBuilder":
        """TODO"""

        add_arg = partial(
            self._arg_parser.add_argument,
            dest=name,
            help=help_string or f"the {name}",
            action=action.value,
            default=default,
        )
        if action == ParserAction.STORE:
            add_arg(choices=choices, nargs=nargs)
        else:
            add_arg()

        return self
