#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib-AskAI
   @package: askai.utils
      @file: askai_prompt.py
   @created: Mon, 22 Jan 2024
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright·(c)·2024,·HSPyLib
"""
import os
from functools import lru_cache
from string import Template

from hspylib.core.metaclass.singleton import Singleton

from askai.utils.utilities import read_prompt


class AskAiPrompt(metaclass=Singleton):
    """Provide the prompts used by the AskAi."""

    INSTANCE = None

    def __init__(self):
        self._setup = Template(read_prompt("01-setup.txt"))
        self._query_id = Template(read_prompt("02-query.txt"))
        self._cmd_out = Template(read_prompt("03-cmd-out.txt"))
        self._shell = os.getenv("HHS_MY_SHELL", "bash")
        self._os_release = os.getenv("HHS_MY_OS_RELEASE", "linux")

    @lru_cache
    def setup(self) -> str:
        return self._setup.substitute(
            shell=self._shell,
            os_type=self._os_release
        )

    @lru_cache
    def cmd_out(self, number: int, output: str, cmd_line: str) -> str:
        return self._cmd_out.substitute(
            shell=self._shell,
            output_number=number,
            command_output=output,
            command_line=cmd_line
        )

    @lru_cache
    def query(self, number: int, query: str) -> str:
        return self._query_id.substitute(
            query_number=number,
            query_string=query
        )
