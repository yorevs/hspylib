#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib-AskAI
   @package: askai.core
      @file: askai.py
   @created: Fri, 5 Jan 2024
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright·(c)·2024,·HSPyLib
"""

import logging as log
import os
import re
import sys
from functools import lru_cache
from threading import Thread
from typing import List

from clitt.core.term.commons import Direction, Portion
from clitt.core.term.terminal import Terminal
from hspylib.core.tools.commons import sysout
from hspylib.modules.application.exit_status import ExitStatus
from hspylib.modules.cache.ttl_cache import TTLCache

from askai.core.askai_configs import AskAiConfigs
from askai.core.engine.ai_engine import AIEngine
from askai.lang.language import Language
from askai.lang.textual_messages import TextualMessages
from askai.utils.constants import Constants
from askai.utils.utilities import stream, hash_text, ptt_input


class AskAi:
    """Responsible for the OpenAI functionalities."""

    MSG = TextualMessages.INSTANCE or TextualMessages()

    @staticmethod
    def _abort():
        """Abort the execution and exit."""
        sys.exit(ExitStatus.FAILED.val)

    def __init__(
        self,
        interactive: bool,
        is_stream: bool,
        is_speak: bool,
        tempo: int,
        engine: AIEngine,
        query_string: str | List[str],
    ):
        self._configs: AskAiConfigs = AskAiConfigs.INSTANCE or AskAiConfigs()
        self._interactive: bool = interactive
        self._terminal: Terminal = Terminal.INSTANCE
        self._cache: TTLCache = TTLCache(ttl_minutes=60)
        self._engine: AIEngine = engine
        self._query_string: str = str(
            " ".join(query_string) if isinstance(query_string, list) else query_string
        )
        self._user: str = os.getenv("USER", "you")
        self._done: bool = False
        self._processing: bool | None = None
        self._configs.is_stream = is_stream
        self._configs.is_speak = is_speak
        self._configs.stream_speed = tempo
        self.MSG.user = self._user
        self.MSG.nickname = self._engine.nickname()

    def __str__(self) -> str:
        return (
            f"%GREEN%"
            f"{'-=' * 40} %EOL%"
            f"     Engine: {self._engine.ai_name()} %EOL%"
            f"      Model: {self._engine.ai_model()} %EOL%"
            f"   Nickname: {self._engine.nickname()} %EOL%"
            f"{'--' * 40} %EOL%"
            f"   Language: {self.language.description} %EOL%"
            f"Interactive: ON %EOL%"
            f"  Streaming: {'ON' if self.is_stream else 'OFF'} %EOL%"
            f"   Speaking: {'ON' if self.is_speak else 'OFF'} %EOL%"
            f"      Tempo: {self.stream_speed} %EOL%"
            f"{'--' * 40} %EOL%%NC%"
        )

    @property
    def query_string(self) -> str:
        return self._query_string

    @property
    def stream_speed(self) -> int:
        return self._configs.stream_speed

    @property
    def is_stream(self) -> bool:
        return self._configs.is_stream

    @property
    def is_speak(self) -> bool:
        return self._configs.is_speak

    @property
    def language(self) -> Language:
        return self._configs.language

    @property
    def is_processing(self) -> bool:
        return self._processing

    @is_processing.setter
    def is_processing(self, processing: bool) -> None:
        msg = self.MSG.wait
        if processing:
            self._reply(msg)
        elif not processing and self._processing is not None and processing != self._processing:
            self._terminal.cursor.move(1, Direction.UP)
            self._terminal.cursor.erase(Portion.LINE)
            self._terminal.cursor.move(len(msg), Direction.LEFT)
        self._processing = processing

    @lru_cache(maxsize=500)
    def ask(self, question: str) -> str:
        """Ask the question and expect the response.
        :param question: The question to ask to the AI engine.
        """
        return self._engine.ask(question)

    def run(self) -> None:
        """Run the program."""
        if self._interactive:
            sysout(self)
            self._prompt()
        elif self._query_string:
            if not re.match(Constants.TERM_EXPRESSIONS, self._query_string.lower()):
                sysout("", end="")
                sysout(f"  {self._user}: {self._query_string}")
                self._ask_and_reply(self._query_string)

    def _input(self) -> str:
        """Prompt for user input."""
        ret = ptt_input(f"  {self._user}: ")
        if self.is_speak and ret == Constants.PUSH_TO_TALK_STR:
            spoken_text = self._engine.speech_to_text(
                f"  {self._engine.nickname()}: {self.MSG.listening}",
                f"  {self._engine.nickname()}: {self.MSG.transcribing}",
            )
            if spoken_text:
                sysout(f"  {self._user}: {spoken_text}")
            return spoken_text

        return ret

    def _prompt(self) -> None:
        """Prompt for user interaction."""
        self._reply(self.MSG.welcome(self._user))
        while question := self._input():
            if not question or re.match(Constants.TERM_EXPRESSIONS, question.lower()):
                self._reply(self.MSG.goodbye)
                break
            elif not self._process_command(question):
                self._ask_and_reply(question)
            else:
                self._reply(question)

    def _process_command(self, command: str) -> bool:
        """Attempt to process command."""

        log.debug("Question: \"%s\" is not a COMMAND", command)

        return False

    def _ask_and_reply(self, question: str) -> None:
        """Ask the question and provide the reply.
        :param question: The question to ask to the AI engine.
        """
        self.is_processing = True
        key = hash_text(question)
        if not (reply := self._cache.read(key)):
            log.debug(
                'Response was not found for "{question}" in cache. Fetching from AI engine'
            )
            reply = self.ask(question)
            self._cache.save(key, reply)
        else:
            log.debug(f'Response found for "{question}" in cache.')
        self._reply(reply)

    def _reply(self, message: str, speak: bool = True) -> None:
        """Reply to the user with the AI response.
        :param message: The message to reply to the user.
        :param speak: Whether to speak the reply or not.
        """
        if self.is_stream and speak and self.is_speak:
            self._engine.text_to_speech(
                message, self._configs.stream_speed, cb_started=self._stream_text
            )
        elif not self.is_stream and speak and self.is_speak:
            self._engine.text_to_speech(
                message, self._configs.stream_speed, cb_started=sysout
            )
        elif self.is_stream:
            self._stream_text(message)
        else:
            sysout(f"  {self._engine.nickname()}: {message}")

    def _stream_text(self, message: str) -> None:
        """Stream the message using default parameters.
        :param message: The message to be streamed.
        """
        self.is_processing = False
        sysout(f"  {self._engine.nickname()}: ", end="")
        stream_thread = Thread(
            target=stream, args=(message, self._configs.stream_speed)
        )
        stream_thread.start()
        # Block until the text is fully streamed.
        stream_thread.join()
