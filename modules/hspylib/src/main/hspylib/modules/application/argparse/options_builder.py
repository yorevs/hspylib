#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: hspylib.modules.application.argparse
      @file: options_builder.py
   @created: hu, 14 Feb 2022
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
from argparse import ArgumentParser
from functools import partial
from hspylib.modules.application.parser_action import ParserAction
from typing import Any


class OptionsBuilder:
    """TODO"""

    def __init__(self, arg_parser: ArgumentParser):
        self._arg_parser = arg_parser

    def option(
        self,
        name: str,
        shortopt: str,
        longopt: str,
        help_string: str = None,
        choices: list = None,
        required: bool = False,
        action: ParserAction = ParserAction.STORE,
        nargs: str | int = None,
        default: Any = None,
    ) -> "OptionsBuilder":
        """TODO"""
        add_arg = partial(
            self._arg_parser.add_argument,
            f"-{shortopt.replace('^-', '')[0]}", f"--{longopt.replace('^-*', '')}",
            dest=name, help=help_string or f"the {longopt}", required=required,
            action=action.value, default=default
        )
        if action == ParserAction.STORE:
            add_arg(choices=choices, nargs=nargs)
        else:
            add_arg()

        return self
