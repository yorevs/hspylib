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
from functools import partial
from shutil import which
from threading import Thread
from typing import List, Optional

from clitt.core.term.commons import Direction, Portion
from clitt.core.term.terminal import Terminal
from clitt.core.tui.line_input.line_input import line_input
from hspylib.core.metaclass.singleton import Singleton
from hspylib.core.tools.commons import sysout
from hspylib.core.tools.text_tools import ensure_endswith
from hspylib.modules.application.exit_status import ExitStatus

from askai.core.askai_configs import AskAiConfigs
from askai.core.askai_messages import AskAiMessages
from askai.core.askai_prompt import AskAiPrompt
from askai.core.engine.protocols.ai_engine import AIEngine
from askai.language.language import Language
from askai.utils.constants import Constants
from askai.utils.utilities import stream


class AskAi(metaclass=Singleton):
    """Responsible for the OpenAI functionalities."""

    INSTANCE = None

    MSG = AskAiMessages.INSTANCE or AskAiMessages()

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
        self._prompts = AskAiPrompt.INSTANCE or AskAiPrompt()
        self._interactive: bool = interactive
        self._terminal: Terminal = Terminal.INSTANCE
        self._engine: AIEngine = engine
        self._query_string: str = str(" ".join(query_string) if isinstance(query_string, list) else query_string)
        self._user: str = os.getenv("USER", "you")
        self._done: bool = False
        self._processing: bool | None = None
        self._configs.is_stream = is_stream
        self._configs.is_speak = is_speak
        self._configs.stream_speed = tempo
        self.MSG.user = self.user
        self.MSG.nickname = self._engine.nickname()

    def __str__(self) -> str:
        return (
            f"%GREEN%"
            f"{'-=' * 40} %EOL%"
            f"     Engine: {self._engine.ai_name()} %EOL%"
            f"      Model: {self._engine.ai_model()} %EOL%"
            f"   Nickname: {self.engine} %EOL%"
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

    @property
    def user(self) -> str:
        return f"%EL0%  {self._user.title()}"

    @property
    def engine(self) -> str:
        return f"%EL0%  {self._engine.nickname()}"

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

    def run(self) -> None:
        """Run the program."""
        if self._interactive:
            sysout(self)
            self._prompt()
        elif self._query_string:
            if not re.match(Constants.TERM_EXPRESSIONS, self._query_string.lower()):
                sysout("", end="")
                sysout(f"{self.user}: {self._query_string}")
                self._ask_and_reply(self._query_string)

    def _input(self, prompt: str) -> Optional[str]:
        """Prompt for user input.
        :param prompt: The prompt to display to the user.
        """
        ret = line_input(prompt)
        if self.is_speak and ret == Constants.PUSH_TO_TALK:  # Use audio as input method.
            self._terminal.cursor.erase(Portion.LINE)
            self._terminal.cursor.move(len(prompt), Direction.LEFT)
            spoken_text = self._engine.speech_to_text(
                partial(self._reply, self.MSG.listening), partial(self._reply, self.MSG.transcribing)
            )
            if spoken_text:
                sysout(f"{self.user}: {spoken_text}")
                ret = spoken_text
        elif not self.is_speak and not isinstance(ret, str):
            self._terminal.cursor.move(1, Direction.UP)
            self._terminal.cursor.erase(Portion.LINE)
            self._terminal.cursor.move(len(prompt), Direction.LEFT)
            sysout(f"{self.user}: %YELLOW%Speech-To-Text is disabled!%NC%")

        return ret if isinstance(ret, str) else ret.val

    def _prompt(self) -> None:
        """Prompt for user interaction."""
        self._reply(self.MSG.welcome(self._user.title()))
        while query := self._input(f"{self.user}: "):
            if not query:
                continue
            elif re.match(Constants.TERM_EXPRESSIONS, query.lower()):
                self._reply(self.MSG.goodbye)
                break
            else:
                self._ask_and_reply(query)
        if not query:
            self._reply(self.MSG.goodbye)
        sysout("")

    def _reply(self, message: str, speak: bool = True) -> str:
        """Reply to the user with the AI response.
        :param message: The message to reply to the user.
        :param speak: Whether to speak the reply or not.
        """
        if self.is_stream and speak and self.is_speak:
            self._engine.text_to_speech(message, self._configs.stream_speed, cb_started=self._stream_text)
        elif not self.is_stream and speak and self.is_speak:
            self._engine.text_to_speech(message, self._configs.stream_speed, cb_started=sysout)
        elif self.is_stream:
            self._stream_text(message)
        else:
            message = f"{self.engine}: {message}"
            sysout(message)

        return message

    def _reply_error(self, error_message: str) -> None:
        """Reply API or system errors.
        :param error_message: The error message to be displayed.
        """
        sysout(f"{self.engine}: {error_message}")

    def _stream_text(self, message: str) -> None:
        """Stream the message using default parameters.
        :param message: The message to be streamed.
        """
        self.is_processing = False
        sysout(f"{self.engine}: ", end="")
        stream_thread = Thread(target=stream, args=(message, self._configs.stream_speed))
        stream_thread.start()
        stream_thread.join()  # Block until the text is fully streamed.

    def _process_command(self, cmd_line: str) -> None:
        """Attempt to process command.
        :param cmd_line: The command line to execute.
        """
        if (command := cmd_line.split(" ")[0]) and which(command):
            log.debug("Processing command `%s'", cmd_line)
            self._reply(self.MSG.executing(cmd_line))
            cmd_line = cmd_line.replace("~", os.getenv("HOME"))
            cmd_ret, exit_code = Terminal.shell_exec(cmd_line, stderr=sys.stdout.fileno())
            if exit_code == ExitStatus.SUCCESS:
                self._reply(self.MSG.cmd_success(exit_code))
                if cmd_ret:
                    self._ask_and_reply(self._prompts.cmd_ret(cmd_ret))
                else:
                    self._reply(self.MSG.cmd_no_output())
            else:
                self._reply(self.MSG.cmd_failed(command))
        else:
            self._reply(self.MSG.cmd_no_exist(command))

    def _ask_and_reply(self, query: str) -> None:
        """Ask the question and provide the reply.
        :param query: The question to ask to the AI engine.
        """
        self.is_processing = True
        if (response := self._engine.ask(query)) and response.is_success():
            if (reply := response.reply_text()) and (
                mat := re.match(r".*`{3}(bash|zsh)(.+)`{3}.*", reply.strip().replace("\n", ""), re.I | re.M)
            ):
                self._process_command(mat.group(2))
            else:
                self._reply(reply)
        else:
            self._reply_error(response.reply_text())
