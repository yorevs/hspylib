#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib-AskAI
   @package: askai.core
      @file: ask_ai.py
   @created: Fri, 5 Jan 2024
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright·(c)·2024,·HSPyLib
"""
import os
import re
import sys
from functools import lru_cache
from threading import Thread
from typing import List

from clitt.core.term.commons import Portion, Direction
from clitt.core.term.terminal import Terminal
from hspylib.core.tools.commons import sysout
from hspylib.modules.application.exit_status import ExitStatus
from hspylib.modules.cache.ttl_cache import TTLCache

from askai.core.ask_ai_configs import AskAiConfigs
from askai.core.engine.ai_engine import AIEngine
from askai.utils.utilities import stream


class AskAi:
    """Responsible for the OpenAI functionalities."""

    TERM_EXPRESSIONS = r"(good)?(bye ?)+|(tchau ?)+|quit|exit"

    @staticmethod
    def _abort():
        """Abort the execution and exit."""
        sys.exit(ExitStatus.FAILED.val)

    def __init__(
        self, interactive: bool, engine: AIEngine, query_string: str | List[str]
    ):
        self._configs: AskAiConfigs = AskAiConfigs()
        self._interactive: bool = interactive
        self._terminal: Terminal = Terminal.INSTANCE
        self._cache: TTLCache = TTLCache()
        self._engine: AIEngine = engine
        self._query_string: str = str(" ".join(query_string) if isinstance(query_string, list) else query_string)
        self._user: str = os.getenv("USER", "you")
        self._wait_msg: str = f"  {self._engine.nickname()}: Processing, please wait..."
        self._done: bool = False

    def __str__(self) -> str:
        return (
            f"%EOL%%GREEN%"
            f"{'-=' * 40} %EOL%"
            f"  Engine: {self._engine.ai_name()} %EOL%"
            f"   Model: {self._engine.ai_model()} %EOL%"
            f"Nickname: {self._engine.nickname()} %EOL%"
            f"{'--' * 40} %EOL%"
            f"Interactive Mode: ON %EOL%"
            f"{'Streaming: ON  Speed: ' + str(self.stream_speed) + '%EOL%' if self.is_stream else '' }%NC%"
        )

    @property
    def query_string(self) -> str:
        return self._query_string

    @property
    def wait_msg(self) -> str:
        return self._wait_msg

    @property
    def stream_speed(self) -> int:
        return self._configs.stream_speed

    @property
    def is_stream(self) -> bool:
        return self._configs.is_stream

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
            if not re.match(AskAi.TERM_EXPRESSIONS, self._query_string.lower()):
                sysout("", end="")
                sysout(f"  {self._user.title()}: {self._query_string}")
                self._ask_and_respond(self._query_string)

    def _input(self) -> str:
        """Prompt for user input."""
        return input(f"  {self._user.title()}: ")

    def _reply(self, message: str) -> None:
        """Reply to the user with the AI response."""
        if self.is_stream:
            self._engine.speak(message, self._stream_text)
        else:
            sysout(f"  {self._engine.nickname()}: {message}")

    def _ask_and_respond(self, question: str) -> None:
        """Ask the question and expect the response."""
        sysout(self.wait_msg, end="")
        reply = self.ask(question)
        self._terminal.cursor.erase(Portion.LINE)
        self._terminal.cursor.move(len(self.wait_msg), Direction.LEFT)
        self._reply(reply)

    def _prompt(self) -> None:
        """Prompt for user interaction."""
        self._reply(f"Hey {self._user}, How can I assist you today?")
        while question := self._input():
            if re.match(AskAi.TERM_EXPRESSIONS, question.lower()):
                self._reply(question.title())
                break
            self._ask_and_respond(question)
        if not question:
            self._reply("Bye")

    def _stream_text(self, message: str) -> None:
        sysout(f"  {self._engine.nickname()}: ", end="")
        stream_thread = Thread(target=stream, args=(message, self._configs.stream_speed, ))
        stream_thread.start()
        stream_thread.join()

