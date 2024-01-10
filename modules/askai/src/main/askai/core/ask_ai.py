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
from typing import List

from clitt.core.term.commons import Portion, Direction
from clitt.core.term.terminal import Terminal
from hspylib.core.tools.commons import sysout
from hspylib.modules.application.exit_status import ExitStatus
from hspylib.modules.cache.ttl_cache import TTLCache

from askai.core.engine.ai_engine import AIEngine
from askai.utils.utilities import stream


class AskAI:
    """Responsible for the OpenAI functionalities."""

    TERM_EXPRESSIONS = r"(good)?(bye ?)+|(tchau ?)+|quit|exit"

    @staticmethod
    def _abort():
        """Abort the execution and exit."""
        sys.exit(ExitStatus.FAILED.val)

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
        self._wait_msg = f"  {self._engine.nickname()}: Processing, please wait..."
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

    @property
    def wait_msg(self) -> str:
        return self._wait_msg

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
                sysout('', end='')
                sysout(f"  {self._user.title()}: {self._query_string}")
                self._ask_and_respond(self._query_string)

    def _input(self) -> str:
        """Prompt for user input."""
        return input(f"  {self._user.title()}: ")

    def _reply(self, message: str) -> None:
        """Reply to the user with the AI response."""
        if self._interactive:
            sysout(f"  {self._engine.nickname()}: ", end='')
            stream(message)
        else:
            sysout(f"  {self._engine.nickname()}: {message}")

    def _ask_and_respond(self, question: str) -> None:
        """Ask the question and expect the response."""
        sysout(self.wait_msg, end='')
        reply = self.ask(question)
        self._terminal.cursor.erase(Portion.LINE)
        self._terminal.cursor.move(len(self.wait_msg), Direction.LEFT)
        self._reply(reply)

    def _prompt(self) -> None:
        """Prompt for user interaction."""
        self._reply(f"Hey {self._user}, How can I assist you today?")

        while question := self._input():
            if re.match(AskAI.TERM_EXPRESSIONS, question.lower()):
                self._reply(question.title())
                break
            self._ask_and_respond(question)

        if not question:
            self._reply("Bye")
