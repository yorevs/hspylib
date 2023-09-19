#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: main.modules.cli.application
      @file: arguments_builder.py
   @created: Thu, 14 Feb 2022
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""
from argparse import ArgumentError, ArgumentParser
from typing import Any

from modules.cli.application.parser_action import ParserAction


class ArgumentsBuilder:
    """TODO"""

    def __init__(self, arg_parser: ArgumentParser):
        self._arg_parser = arg_parser

    def argument(
        self,
        name: str,
        help_string: str = None,
        choices: list = None,
        nargs: str = None,
        default: Any = None) -> 'ArgumentsBuilder':
        """TODO"""

        self._arg_parser.add_argument(
            dest=name,
            help=help_string or f'the {name}',
            action=ParserAction.STORE.value,
            choices=choices,
            nargs=nargs,
            default=default)

        return self
