#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib
   @package: hspylib.modules.application.argparse
      @file: argument_chain_builder.py
   @created: hu, 14 Feb 2022
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""
from argparse import ArgumentParser
from functools import partial
from hspylib.modules.application.argparse.parser_action import ParserAction
from typing import Any, Union


class ChainedArgumentsBuilder:
    """Class to provide chained arguments parser builder."""

    def __init__(self, arg_parser: ArgumentParser, subcommand_name: str, subcommand_help: str):
        self._arg_parser = arg_parser
        self._subparsers = self._arg_parser.add_subparsers(
            title=subcommand_name, dest=subcommand_name, help=subcommand_help, required=True
        )
        self._current = arg_parser

    def argument(self, name: str, help_string: str = None) -> "ChainedArgumentsBuilder":
        """Assign a new chained argument to the parser."""

        self._current = self._subparsers.add_parser(name, help=help_string)

        return self

    def add_parameter(
        self,
        name: str,
        help_string: str = None,
        choices: list = None,
        nargs: Union[str, int] = None,
        action: ParserAction = ParserAction.STORE,
    ) -> "ChainedArgumentsBuilder":
        """Assign a new chained argument parameter to the parser."""

        add_argument = partial(
            self._current.add_argument, help=help_string or f"the {name}", dest=name, action=action.value
        )

        if action == ParserAction.STORE:
            add_argument(choices=choices, nargs=nargs)
        else:
            add_argument()

        return self

    def add_option(
        self,
        name: str,
        shortopt: str,
        longopt: str,
        help_string: str = None,
        choices: list = None,
        required: bool = False,
        nargs: Union[str, int] = None,
        action: ParserAction = ParserAction.STORE,
        default: Any = None,
    ) -> "ChainedArgumentsBuilder":
        """Assign a new chained option parameter to the parser."""

        add_arg = partial(
            self._current.add_argument,
            f"-{shortopt.replace('^-', '')[0]}",
            f"--{longopt.replace('^-*', '')}",
            dest=name,
            help=help_string or f"the {longopt}",
            required=required,
            action=action.value,
            default=default,
        )
        if action == ParserAction.STORE:
            add_arg(choices=choices, nargs=nargs)
        else:
            add_arg()

        return self
