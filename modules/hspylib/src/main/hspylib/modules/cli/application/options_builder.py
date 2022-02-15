#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: main.modules.cli.application
      @file: options_builder.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""
from argparse import ArgumentParser


class OptionsBuilder:

    def __init__(self, arg_parser: ArgumentParser):
        self._arg_parser = arg_parser

    def option(
        self,
        name: str,
        shortopt: str,
        longopt: str,
        help: str = None) -> 'OptionsBuilder':

        self._arg_parser.add_argument(
            f"-{shortopt.replace('^-','')[0]}",
            f"--{longopt.replace('^-','')[0]}",
            dest=name,
            help=help or f'the {longopt}',
            action='store_true')

        return self