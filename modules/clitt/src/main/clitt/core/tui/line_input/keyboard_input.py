#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib-AskAI
   @package: main.clitt.core.tui.line_input
      @file: keyboard_input.py
   @created: Wed, 17 Jan 2024
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright·(c)·2024,·HSPyLib
"""

from typing import Optional, List, Dict

import pyperclip
from hspylib.modules.cli.keyboard import Keyboard
from hspylib.modules.cli.vt100.vt_color import VtColor

from clitt.core.term.commons import Direction
from clitt.core.term.terminal import Terminal
from clitt.core.tui.tui_component import TUIComponent


class KeyboardInput(TUIComponent):
    """Provides a keyboard input for terminal UIs with undo and history."""

    # Current history index.
    _HIST_INDEX: int = 0

    # Dict containing all previously accepted inputs.
    _HISTORY: Dict[int, str] = {0: ""}

    # Stack containing current input changes.
    _UNDO_HISTORY: List[str] = []

    # Stack containing current input reverts.
    _REDO_HISTORY: List[str] = []

    @staticmethod
    def preload_history(history: List[str]) -> None:
        """Preload the input with the provided dictionary."""
        for entry in history:
            KeyboardInput._add_history(entry)
        KeyboardInput._HIST_INDEX = 0

    @staticmethod
    def forget_history() -> None:
        """Forget all input history entries."""
        tmp: str = KeyboardInput._HISTORY[0]
        KeyboardInput._HISTORY.clear()
        KeyboardInput._HISTORY[0] = tmp

    @staticmethod
    def history() -> List[str]:
        """Return the actual input history."""
        return list(filter(lambda v: v, KeyboardInput._HISTORY.values()))

    @staticmethod
    def _add_history(input_text: str) -> None:
        """Add the following input to the history set.
        :param input_text: The input text to add to the history.
        """
        if input_text and input_text not in list(KeyboardInput._HISTORY.values())[1:]:
            idx: int = max(1, len(KeyboardInput._HISTORY))
            KeyboardInput._HISTORY[idx] = input_text
            KeyboardInput._HIST_INDEX = idx

    @classmethod
    def _next_in_history(cls) -> Optional[str]:
        index = min(len(cls._HISTORY) - 1, cls._HIST_INDEX + 1)
        text = cls._HISTORY.get(index, "")
        cls._HIST_INDEX = index
        return text or cls._HISTORY[0]

    @classmethod
    def _prev_in_history(cls) -> Optional[str]:
        index = max(0, cls._HIST_INDEX - 1)
        text = cls._HISTORY.get(index, "")
        cls._HIST_INDEX = index
        return text or cls._HISTORY[0]

    @classmethod
    def _undo(cls) -> Optional[str]:
        text = cls._UNDO_HISTORY.pop() if cls._UNDO_HISTORY else None
        if cls._HISTORY[0] not in cls._REDO_HISTORY:
            cls._REDO_HISTORY.append(cls._HISTORY[0])
        return text

    @classmethod
    def _redo(cls) -> Optional[str]:
        text = cls._REDO_HISTORY.pop() if cls._REDO_HISTORY else None
        if cls._HISTORY[0] not in cls._UNDO_HISTORY:
            cls._UNDO_HISTORY.append(cls._HISTORY[0])
        return text

    def __init__(
        self, prompt: str = "",
        prompt_color: VtColor = VtColor.NC,
        text_color: VtColor = VtColor.NC,
        navbar_enable: bool = False
    ):
        super().__init__(prompt)
        self._prompt_color = prompt_color
        self._text_color = text_color
        self._navbar_enable = navbar_enable
        self._input_index = 0
        self._input_text: str = ""
        self._HISTORY[0] = ""

    @property
    def length(self) -> int:
        return len(self._input_text) if self._input_text else 0

    def _prepare_render(self, auto_wrap: bool = True, show_cursor: bool = True) -> None:
        Terminal.set_auto_wrap(auto_wrap)
        Terminal.set_show_cursor(show_cursor)
        self.cursor.save()

    def _loop(self, break_keys: List[Keyboard] = None) -> Keyboard:
        break_keys = break_keys or Keyboard.break_keys()
        keypress = Keyboard.VK_NONE

        # Wait for user interaction
        while not self._done and keypress and keypress not in break_keys:
            # Menu Renderization
            if self._re_render:
                self.render()
            # Navigation input
            keypress = self.handle_keypress()

        return keypress

    def execute(self) -> Optional[str | Keyboard]:
        self.write(f"{self._prompt_color.placeholder}{self.title}{self._text_color.placeholder}")
        self._prepare_render()
        keypress = self._loop() or Keyboard.VK_ESC

        if keypress.isEnter():
            self._add_history(self._input_text)
            self._UNDO_HISTORY.clear()
            self._REDO_HISTORY.clear()
        elif keypress == Keyboard.VK_ESC:
            self._input_text = None

        self.writeln("%NC%")

        return self._input_text

    def render(self) -> None:
        Terminal.set_show_cursor(False)
        self.cursor.restore()
        self.write(self._input_text)
        self._terminal.cursor.erase(Direction.RIGHT)
        self._re_render = False
        self._set_cursor_pos()
        Terminal.set_show_cursor()

    def navbar(self, **kwargs) -> str:
        pass

    def handle_keypress(self) -> Keyboard:
        if keypress := Keyboard.wait_keystroke():
            match keypress:
                case Keyboard.VK_BACKSPACE:
                    if self._input_index > 0:
                        self._input_index = max(0, self._input_index - 1)
                        self._update_input(
                            self._input_text[: self._input_index] + self._input_text[1 + self._input_index:]
                        )
                case Keyboard.VK_DELETE:
                    self._update_input(
                        self._input_text[: self._input_index] + self._input_text[1 + self._input_index:]
                    )
                case Keyboard.VK_CTRL_F:  # Forget history
                    self.forget_history()
                case Keyboard.VK_CTRL_P:  # Paste from clipboard
                    text = (pyperclip.paste() or '').replace("\n", "↵")
                    self._update_input(
                        self._input_text[: self._input_index] + text + self._input_text[self._input_index:]
                    )
                    self._input_index += len(text)
                case Keyboard.VK_CTRL_R:  # Reset contents
                    self._input_index = 0
                    self._update_input("")
                case Keyboard.VK_LEFT:
                    self._input_index = max(0, self._input_index - 1)
                case Keyboard.VK_RIGHT:
                    self._input_index = min(self.length, self._input_index + 1)
                case Keyboard.VK_UP:
                    self._input_text = self._next_in_history()
                    self._input_index = self.length
                case Keyboard.VK_DOWN:
                    self._input_text = self._prev_in_history()
                    self._input_index = self.length
                case Keyboard.VK_HOME:
                    self._input_index = 0
                case Keyboard.VK_END:
                    self._input_index = self.length
                case _ as key if key.val.isprintable():
                    self._update_input(
                        self._input_text[: self._input_index] + key.val + self._input_text[self._input_index:]
                    )
                    self._input_index += 1
                case _ as key if key in Keyboard.break_keys():
                    self._done = True
                case _:
                    self._input_text = keypress
                    self._done = True
            self._re_render = True

        return keypress

    def _set_cursor_pos(self):
        """Set the cursor position on the input."""
        index_offset = max(0, self.length - self._input_index)
        self.screen.cursor.move(index_offset, Direction.LEFT)

    def _update_input(self, text: str) -> str:
        """Update the value of the input.
        :param text: The text to be set.
        """
        self._UNDO_HISTORY.append(self._input_text)
        self._HISTORY[0] = text if text not in self._HISTORY else self._input_text
        self._input_text = text
        return text
