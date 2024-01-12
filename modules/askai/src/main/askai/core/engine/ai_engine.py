#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib-AskAI
   @package: askai.core.engine
      @file: ai_engine.py
   @created: Fri, 5 May 2024
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright·(c)·2024,·HSPyLib
"""

from typing import Callable, Optional, Protocol


class AIEngine(Protocol):
    """Provide an interface for AI engines."""

    def ai_name(self) -> str:
        """Get the AI engine name."""
        ...

    def ai_model(self) -> str:
        """Get the AI model name."""
        ...

    def nickname(self) -> str:
        """Get the AI engine nickname."""
        ...

    def ask(self, question: str) -> str:
        """Ask AI assistance for the given question.
        :param question: The question to ask to the AI engine.
        """
        ...

    def clear(self) -> None:
        """Forget the chat context and restart over."""
        ...

    def text_to_speech(
        self,
        text: str = None,
        speed: int = 0,
        cb_started: Optional[Callable[[str], None]] = None,
        cb_finished: Optional[Callable] = None,
    ) -> None:
        """Text-T0-Speech the provided text.
        :param text: The text to speech.
        :param speed: The tempo to play the generated audio [1..3].
        :param cb_started: The callback function called when the speaker starts.
        :param cb_finished: The callback function called when the speaker ends.
        """
        ...

    def speech_to_text(
        self,
        prompt: str = "Listening...",
        processing_msg: str = "Transcribing audio to text...",
    ) -> str:
        """Transcribes audio input from the microphone into the text input language."""
        ...
