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

from typing import Protocol


class AIEngine(Protocol):
    """Provide an interface for AI methods."""

    def ai_name(self) -> str:
        """Get the name of the AI."""
        ...

    def ai_model(self) -> str:
        """Get the type of the AI."""
        ...

    def nickname(self) -> str:
        """Get the AI nickname."""
        ...

    def ask(self, question: str) -> str:
        """Ask AI assistance for the given question."""
        ...

    def reset(self) -> None:
        """Forget the context and restart over."""
        ...
