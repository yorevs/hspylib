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

from typing import Optional

from clitt.core.term.commons import Direction
from clitt.core.term.terminal import Terminal
from clitt.core.tui.tui_component import TUIComponent
from hspylib.core.tools.dict_tools import get_or_default
from hspylib.modules.cli.keyboard import Keyboard
from hspylib.modules.cli.vt100.vt_color import VtColor


class KeyboardInput(TUIComponent):
    """Provides a keyboard input for terminal UIs with undo and history."""

    # Current history index.
    _HIST_INDEX: int = 0

    # Dict containing all previously accepted inputs.
    _HISTORY: list[str] = [""]

    # Stack containing current input changes.
    _UNDO_HISTORY: list[str] = []

    # Stack containing current input reverts.
    _REDO_HISTORY: list[str] = []

    @classmethod
    def preload_history(cls, history: list[str]) -> None:
        """Preload the input with the provided dictionary.
        :param history: The history keyboard inputs.
        """
        for entry in reversed(history):
            cls._add_history(entry)
        cls._HIST_INDEX = max(0, len(cls._HISTORY) - 1)

    @classmethod
    def forget_history(cls) -> None:
        """Forget all input history entries."""
        tmp: str = cls._HISTORY[-1]
        cls._HISTORY.clear()
        cls._HISTORY.append(tmp)

    @classmethod
    def history(cls) -> list[str]:
        """Return the actual input history."""
        return list(filter(lambda v: v, cls._HISTORY))

    @classmethod
    def _add_history(cls, input_text: str) -> None:
        """Add the following input to the history set.
        :param input_text: The input text to add to the history.
        """
        if input_text and input_text not in list(cls._HISTORY)[1:]:
            idx: int = max(1, len(cls._HISTORY))
            if input_text not in cls._HISTORY:
                cls._HISTORY.insert(idx - 1, input_text)
            else:
                cls._HISTORY = cls._HISTORY[1:-1] + cls._HISTORY[:1] + cls._HISTORY[-1:]
            cls._HIST_INDEX = idx

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
        self,
        prompt: str = "",
        prompt_color: VtColor = VtColor.NC,
        text_color: VtColor = VtColor.NC,
        navbar_enable: bool = False,
    ):
        super().__init__(prompt)
        self._prompt_color: VtColor = prompt_color
        self._text_color: VtColor = text_color
        self._navbar_enable: bool = navbar_enable
        self._input_index: int = 0
        self._input_text: str = ""
        self._HISTORY[-1] = ""

    @property
    def length(self) -> int:
        return len(self._input_text) if self._input_text else 0

    def _prepare_render(self, auto_wrap: bool = True, show_cursor: bool = True) -> None:
        self.screen.add_watcher(self.invalidate)
        Terminal.set_auto_wrap(auto_wrap)
        Terminal.set_show_cursor(show_cursor)
        self.cursor.save()

    def execute(self) -> Optional[str | Keyboard]:
        self._prepare_render()
        keypress = self._loop() or Keyboard.VK_ESC

        if keypress.isEnter():
            self._HISTORY.append('')
            self._UNDO_HISTORY.clear()
            self._REDO_HISTORY.clear()
        elif keypress == Keyboard.VK_ESC:
            self._input_text = None

        self.writeln("%NC%")

        return self._input_text

    def reset(self) -> None:
        """Reset the contents of the input."""
        self._input_index = 0
        self._update_input("")

    def _loop(self, break_keys: list[Keyboard] = None) -> Keyboard:
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

    def render(self) -> None:
        Terminal.set_show_cursor(False)
        self.cursor.restore()
        self.write(f"{self._prompt_color.placeholder}{self.title}{self._text_color.placeholder}")
        self.write(self._input_text)
        self._terminal.cursor.erase(Direction.DOWN)
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
                            self._input_text[: self._input_index] + self._input_text[1 + self._input_index :]
                        )
                case Keyboard.VK_DELETE:
                    self._update_input(
                        self._input_text[: self._input_index] + self._input_text[1 + self._input_index :]
                    )
                case Keyboard.VK_CTRL_R:
                    self.reset()
                case Keyboard.VK_CTRL_F:
                    self.forget_history()
                case Keyboard.VK_LEFT:
                    self._input_index = max(0, self._input_index - 1)
                case Keyboard.VK_RIGHT:
                    self._input_index = min(self.length, self._input_index + 1)
                case Keyboard.VK_UP:
                    self._input_text = self._prev_in_history()
                    self._input_index = self.length
                case Keyboard.VK_DOWN:
                    self._input_text = self._next_in_history()
                    self._input_index = self.length
                case Keyboard.VK_HOME:
                    self._input_index = 0
                case Keyboard.VK_END:
                    self._input_index = self.length
                case _ as key if key.val.isprintable():
                    self._update_input(
                        self._input_text[: self._input_index] + key.val + self._input_text[self._input_index :]
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
        self._HISTORY[-1] = text if text not in self._HISTORY else self._input_text
        self._input_text = text
        return text

    def _next_in_history(self) -> str:
        """Return the next input in history."""
        edt_text: str = self._HISTORY[-1]
        filtered: list[str] = list(filter(lambda h: h.startswith(edt_text), self._HISTORY))
        index = min(len(filtered) - 1, self._HIST_INDEX + 1)
        text = get_or_default(filtered, index, "")
        self._HIST_INDEX = index
        return text or filtered[-1]

    def _prev_in_history(self) -> str:
        """Return the previous input in history."""
        edt_text: str = self._HISTORY[-1]
        filtered: list[str] = list(filter(lambda h: h.lower().startswith(edt_text.lower()), self._HISTORY))
        index = max(0, min(len(filtered) - 2, self._HIST_INDEX - 1))
        text = get_or_default(filtered, index, "")
        self._HIST_INDEX = index
        return text or filtered[-1]
