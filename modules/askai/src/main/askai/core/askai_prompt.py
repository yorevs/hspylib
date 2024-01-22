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
from string import Template

from hspylib.core.metaclass.singleton import Singleton

from askai.utils.utilities import read_prompt


class AskAiPrompt(metaclass=Singleton):
    """"""

    INSTANCE = None

    def __init__(self):
        self._setup = Template(read_prompt("01-setup.txt"))
        self._cmd_ret = Template(read_prompt("02-cmd-out.txt"))
        self._shell = os.getenv("HHS_MY_SHELL", "bash")
        self._os_release = os.getenv("HHS_MY_OS_RELEASE", "linux")

    def setup(self) -> str:
        return self._setup.substitute(
            shell=self._shell,
            os_type=self._os_release
        )

    def cmd_ret(self, output: str) -> str:
        return self._cmd_ret.substitute(
            shell=self._shell,
            cmd_ret=output
        )
