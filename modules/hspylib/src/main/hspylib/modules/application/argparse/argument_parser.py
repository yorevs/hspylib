#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib
   @package: hspylib.modules.application.argparse
      @file: argument_parser.py
   @created: Thu, 14 Feb 2022
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""
from argparse import ArgumentParser
from hspylib.modules.application.exit_status import ExitStatus
from typing import Any

import argparse
import sys


class HSArgumentParser(ArgumentParser):
    """Class to provide a custom argument parser."""

    def _check_value(self, action, value: Any):
        if action.choices is not None and value not in action.choices:
            msg = f"Invalid choice '{value}'. Choose from [{', '.join(map(repr, action.choices))}]"
            raise argparse.ArgumentError(action, msg)

    def error(self, message):
        self.print_help(sys.stderr)
        self.exit(ExitStatus.FAILED.val, f"\n### Error {self.prog} -> {message}\n\n")
