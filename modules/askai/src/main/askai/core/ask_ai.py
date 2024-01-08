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
import os
import re
import sys
from functools import lru_cache
from time import sleep
from typing import List

from clitt.core.term.commons import Portion, Direction
from clitt.core.term.terminal import Terminal
from hspylib.core.tools.commons import sysout
from hspylib.modules.application.exit_status import ExitStatus
from hspylib.modules.cache.ttl_cache import TTLCache

from askai.core.engine.ai_engine import AIEngine


class AskAI:
    """Responsible for the OpenAI functionalities."""

    TERM_EXPRESSIONS = r"(good)?(bye ?)+|(tchau ?)+|quit|exit"

    @staticmethod
    def _abort():
        """Abort the execution and exit."""
        sys.exit(ExitStatus.FAILED.val)

    @staticmethod
    def stream(
        reply: str,
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

        sysout('')

    def __init__(
        self,
        interactive: bool,
        engine: AIEngine,
        query_string: str | List[str]
        ):

        self._interactive: bool = interactive
        self._terminal: Terminal = Terminal.INSTANCE
        self._cache: TTLCache = TTLCache()
        self._engine: AIEngine = engine
        self._query_string: str = str(' '.join(query_string) if isinstance(query_string, list) else query_string)
        self._user: str = os.getenv('USER', 'you')
        self._done: bool = False

    def __str__(self) -> str:
        return (
            f"%EOL%%GREEN%"
            f"{'-=' * 40} %EOL%"
            f"  Engine: {self._engine.ai_name()} %EOL%"
            f"   Model: {self._engine.ai_model()} %EOL%"
            f"Nickname: {self._engine.nickname()} %EOL%"
            f"{'--' * 40}"
            f"%EOL%Interactive Mode is ON%EOL%%NC%"
        )

    @property
    def query_string(self) -> str:
        return self._query_string

    @lru_cache(maxsize=500)
    def ask(self, question: str) -> str:
        """Ask the question and expect the response."""
        return self._engine.ask(question)

    def run(self) -> None:
        """Run the program."""
        if self._interactive:
            sysout(self)
            self._prompt()
        elif self._query_string:
            if not re.match(AskAI.TERM_EXPRESSIONS, self._query_string.lower()):
                sysout(f"  {self._user.title()}: {self._query_string}")
                reply = self.ask(self._query_string)
                self._reply(reply, False)

    def _ask(self) -> str:
        """Ask the question and expect the response."""
        return input(f"  {self._user.title()}: ")

    def _reply(self, message: str, streamed: bool = True) -> None:
        """Reply to the user with the AI response."""
        if streamed:
            sysout(f"  {self._engine.nickname()}: ", end='')
            AskAI.stream(message)
        else:
            sysout(f"  {self._engine.nickname()}: {message}")

    def _prompt(self) -> None:
        """Prompt for user interaction."""
        wait_msg = f"  {self._engine.nickname()}: Processing, please wait..."
        self._reply(f"Hey {self._user}, How can I assist you today?")

        while message := self._ask():
            if re.match(AskAI.TERM_EXPRESSIONS, message.lower()):
                self._reply(message.title())
                break
            sysout(wait_msg, end='')
            reply = self.ask(message)
            self._terminal.cursor.erase(Portion.LINE)
            self._terminal.cursor.move(len(wait_msg), Direction.LEFT)
            self._reply(reply)

        if not message:
            self._reply("Bye")
