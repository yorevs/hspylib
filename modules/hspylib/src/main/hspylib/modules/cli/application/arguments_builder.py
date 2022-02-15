#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: main.modules.cli.application
      @file: arguments_builder.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""
from argparse import ArgumentParser


class ArgumentsBuilder:

    def __init__(self, arg_parser: ArgumentParser):
        self._arg_parser = arg_parser

    def argument(
        self,
        name: str,
        help: str = None,
        choices: list = None) -> 'ArgumentsBuilder':

        self._arg_parser.add_argument(
            dest=name,
            help=help or f'the {name}',
            action='append',
            choices=choices)

        return self
