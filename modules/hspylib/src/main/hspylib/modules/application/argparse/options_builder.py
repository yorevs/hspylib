#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib
   @package: hspylib.modules.application.argparse
      @file: options_builder.py
   @created: hu, 14 Feb 2022
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""
from argparse import ArgumentParser
from functools import partial
from hspylib.modules.application.argparse.parser_action import ParserAction
from typing import Any


class OptionsBuilder:
    """Class to provide an option parser builder."""

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
        """Assign a new option to the parser."""

        add_argument = partial(
            self._arg_parser.add_argument,
            f"-{shortopt.replace('^-', '')[0]}",
            f"--{longopt.replace('^-*', '')}",
            dest=name,
            help=help_string or f"the {longopt}",
            required=required,
            action=action.value,
            default=default,
        )

        if action == ParserAction.STORE:
            add_argument(choices=choices, nargs=nargs)
        else:
            add_argument()

        return self
