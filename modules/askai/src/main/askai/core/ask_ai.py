#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib-AskAI
   @package: askai.core
      @file: ask_ai.py
   @created: Fri, 5 May 2024
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright·(c)·2024,·HSPyLib
"""
import sys
from time import sleep

from clitt.core.term.terminal import Terminal
from hspylib.core.tools.commons import sysout
from hspylib.modules.application.exit_status import ExitStatus
from hspylib.modules.cache.ttl_cache import TTLCache

from askai.core.engine.ai_engine import AIEngine
from askai.core.engine.openai.openai_engine import OpenAIEngine


class AIBrain:
    """Responsible for the OpenAI functionalities."""

    @staticmethod
    def _abort():
        """Abort the execution and exit."""
        sys.exit(ExitStatus.FAILED.val)

    def __init__(self, engine: AIEngine = OpenAIEngine.GPT_3_5_TURBO):
        self._terminal = Terminal.INSTANCE
        self._cache = TTLCache()
        self._engine = engine
        self._done = False

    def __str__(self) -> str:
        return (
            f"%EOL%%GREEN%"
            f"{'-=' * 40} %EOL%"
            f" AI-Name: {self._engine.ai_name()} %EOL%"
            f"AI-Model: {self._engine.ai_model()} %EOL%"
            f"{'-=' * 40}"
        )

    def ask(self, question: str, streamed: bool = True) -> str:
        """Ask the question and expect the response."""
        reply = self._engine.ask(question)

        return reply if not streamed else self._stream(reply)

    def _stream(
        self, reply: str,
        interval: float = 0.010,
        alpha_interval: float = 0.010,
        number_interval: float = 0.020,
        comma_interval: float = 0.250,
        punct_interval: float = 0.400
        ) -> None:
        """Stream the response from the AI Engine. Simulates a typewriter effect."""
        for next_chr in reply:
            sysout(next_chr, end='')
            if next_chr.isalpha():
                sleep(alpha_interval)
            elif next_chr.isnumeric():
                sleep(number_interval)
            elif next_chr in [',', ';']:
                sleep(comma_interval)
            elif next_chr in ['.', '?', '!']:
                sleep(punct_interval)
            sleep(interval)
        sysout('', end='')
