#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib-AskAI
   @package: askai.core
      @file: askai_configs.py
   @created: Fri, 5 Jan 2024
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright·(c)·2024,·HSPyLib
"""
import os

from hspylib.core.config.app_config import AppConfigs
from hspylib.core.metaclass.singleton import Singleton

from askai.__classpath__ import _Classpath
from askai.lang.language import Language


class AskAiConfigs(metaclass=Singleton):
    """TODO"""

    INSTANCE = None

    # The resources folder
    RESOURCE_DIR = str(_Classpath.resource_path())

    def __init__(self):
        self._configs = AppConfigs.INSTANCE or AppConfigs(self.RESOURCE_DIR)
        self._stream_speed = self._configs.get_int("askai.stream.speed")
        self._is_stream = self._configs.get_bool("askai.stream.response")
        self._is_speak = self._configs.get_bool("askai.speak.response")
        self._language = Language.of_locale(os.getenv("LC_ALL", os.getenv("LC_TYPE", os.getenv("LANG", "en_US.UTF-8"))))

    @property
    def stream_speed(self) -> int:
        return self._stream_speed

    @stream_speed.setter
    def stream_speed(self, value: int) -> None:
        self._stream_speed = value

    @property
    def is_stream(self) -> bool:
        return self._is_stream

    @is_stream.setter
    def is_stream(self, value: bool) -> None:
        self._is_stream = value

    @property
    def is_speak(self) -> bool:
        return self._is_speak

    @is_speak.setter
    def is_speak(self, value: bool) -> None:
        self._is_speak = value

    @property
    def language(self) -> Language:
        return self._language

    @property
    def encoding(self) -> str:
        return self._language.encoding
