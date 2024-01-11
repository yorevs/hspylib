#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib-AskAI
   @package: askai.core
      @file: ask_ai_configs.py
   @created: Fri, 5 Jan 2024
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright·(c)·2024,·HSPyLib
"""
from hspylib.core.config.app_config import AppConfigs
from hspylib.core.metaclass.singleton import Singleton


class AskAiConfigs(metaclass=Singleton):
    """TODO"""

    INSTANCE = None

    def __init__(self):
        self._configs = AppConfigs.INSTANCE or AppConfigs()

    @property
    def stream_speed(self) -> int:
        return self._configs.get_int("askai.stream.speed")

    @property
    def is_stream(self) -> bool:
        return self._configs.get_bool("askai.stream.response")
