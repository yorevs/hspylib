#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: main.modules.cli.application
      @file: options_builder.py
   @created: hu, 14 Feb 2022
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
from argparse import ArgumentParser
from typing import Any

from hspylib.modules.application.parser_action import ParserAction


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
        nargs: str | int = None,
        default: Any = None,
    ) -> "OptionsBuilder":
        """TODO"""

        self._arg_parser.add_argument(
            f"-{shortopt.replace('^-', '')[0]}",
            f"--{longopt.replace('^-*', '')}",
            dest=name,
            help=help_string or f"the {longopt}",
            required=required,
            action=ParserAction.STORE.value,
            choices=choices,
            nargs=nargs,
            default=default,
        )

        return self
