#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib-AskAI
   @package: main.clitt.core.tui.line_input
      @file: keyboard_input.py
   @created: Wed, 17 Jan 2024
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright·(c)·2024,·HSPyLib
"""
import os
from collections import defaultdict
from typing import Optional, Callable, TypeAlias

from clitt.core.term.commons import Direction, Position
from clitt.core.term.terminal import Terminal
from clitt.core.tui.tui_component import TUIComponent
from hspylib.core.tools.dict_tools import get_or_default
from hspylib.modules.cli.keyboard import Keyboard
from hspylib.modules.cli.vt100.vt_color import VtColor

KeyBinding: TypeAlias = dict[Keyboard, Callable[[], None]]


class KeyboardInput(TUIComponent):
    """Provides a keyboard input for terminal UIs with undo and history."""

    # minimum length to be considered as history store.
    _MIN_HIST_STORE_LEN: int = 3

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
        for entry in history:
            cls._add_history(entry)
        cls._HIST_INDEX = max(0, len(cls._HISTORY))

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
        if not len(input_text) > cls._MIN_HIST_STORE_LEN:
            return
        if cls._HISTORY[-1] != '':
            cls._HISTORY.append('')
        if input_text:
            idx: int = max(1, len(cls._HISTORY))
            if input_text in cls._HISTORY:
                idx -= 1
                cls._HISTORY.remove(input_text)
            cls._HISTORY.insert(idx - 1, input_text)
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
        placeholder: str = "",
        prompt_color: VtColor = VtColor.NC,
        text_color: VtColor = VtColor.NC,
        navbar_enable: bool = False,
    ):
        self._HISTORY[-1] = ""
        self._HIST_INDEX = max(0, len(self._HISTORY) - 1)
        super().__init__(prompt)
        self._placeholder: str = placeholder
        self._prompt_color: VtColor = prompt_color
        self._text_color: VtColor = text_color
        self._navbar_enable: bool = navbar_enable
        self._offset: Position = 0, 0
        self._input_index: int = 0
        self._input_text: str = ""
        self._suggestion: str = ""
        self._bindings: KeyBinding = defaultdict()
        self._bind_keys()

    @property
    def prompt(self) -> str:
        return f"{self.prompt_color}{self.title}{self.text_color}"

    @property
    def text(self) -> str:
        return self._input_text

    @text.setter
    def text(self, value: str) -> None:
        self._input_text = value

    @property
    def length(self) -> int:
        return len(self.text) if self.text else 0

    @property
    def prompt_color(self) -> str:
        return self._prompt_color.placeholder

    @property
    def text_color(self) -> str:
        return self._text_color.placeholder

    @property
    def placeholder(self) -> str:
        return self._placeholder

    @property
    def bindings(self) -> KeyBinding:
        return self._bindings

    def execute(self) -> Optional[str | Keyboard]:
        keypress = self._loop(cleanup=False) or Keyboard.VK_ESC
        if keypress.isEnter():
            self._add_history(self.text)
            self._UNDO_HISTORY.clear()
            self._REDO_HISTORY.clear()
            self.cursor.erase(Direction.DOWN)
        elif keypress == Keyboard.VK_ESC:
            self.text = None
        self.writeln("%NC%")

        return self.text

    def reset(self) -> None:
        """Reset the contents of the input."""
        self._input_index = 0
        self._update_input("")

    def home(self) -> None:
        """Place the cursor at the start of the input text."""
        self._input_index = 0

    def end(self) -> None:
        """Place the cursor at the end of the input text."""
        self._input_index = self.length

    def complete(self) -> None:
        """Complete the input text with the suggested text."""
        text: str = self.text + self._suggestion
        self._update_input(text)
        self._input_index = len(text)

    def render(self) -> None:
        Terminal.set_show_cursor(False)
        self.cursor.move(self._offset[0], Direction.UP)
        self.cursor.move(self._offset[1], Direction.LEFT)
        self.cursor.erase(Direction.DOWN)
        self.write(self.prompt)
        if self.text:
            self.write(self.text)
            self._render_suggestions()
        else:
            self.write(f"%GRAY%{self.placeholder}%NC%")
            self.cursor.erase(Direction.DOWN)
            self.cursor.move(len(self.placeholder), Direction.LEFT)
        self._re_render = False
        self._set_cursor_pos()
        self._offset = self.prompt.count(os.linesep), self.cursor.position[1]
        Terminal.set_show_cursor()

    def navbar(self, **kwargs) -> str:
        ...

    def handle_keypress(self) -> Keyboard:
        if keypress := Keyboard.wait_keystroke():
            match keypress:
                # Default key bindings.
                case Keyboard.VK_BACKSPACE:
                    if self._input_index > 0:
                        self._input_index = max(0, self._input_index - 1)
                        self._update_input(
                            self.text[: self._input_index] + self.text[1 + self._input_index:]
                        )
                case Keyboard.VK_DELETE:
                    self._update_input(
                        self.text[: self._input_index] + self.text[1 + self._input_index:]
                    )
                case Keyboard.VK_LEFT:
                    self._input_index = max(0, self._input_index - 1)
                case Keyboard.VK_RIGHT:
                    self._input_index = min(self.length, self._input_index + 1)
                case Keyboard.VK_UP:
                    self.text = self._prev_in_history()
                    self._input_index = self.length
                case Keyboard.VK_DOWN:
                    self.text = self._next_in_history()
                    self._input_index = self.length
                # Customizable key bindings.
                case _ as key if key in self.bindings:
                    if (fn := self.bindings[key]) and callable(fn):
                        fn()
                # Printable characters
                case _ as key if key.val.isprintable():
                    text: str = key.val
                    while (key := Keyboard.wait_keystroke(False)) != Keyboard.VK_NONE:
                        if key.val and key.val.isprintable():
                            text += key.val
                    self._update_input(
                        self.text[: self._input_index] + text + self.text[self._input_index:])
                    self._input_index += len(text)
                # Loop breaking characters
                case _ as key if key in Keyboard.break_keys():
                    self._done = True
                case _:
                    self.text = keypress
                    self._done = True
            self._re_render = True

        return keypress

    def _bind_keys(self) -> None:
        """Configure the default key bindings."""
        self._bindings.update({
            Keyboard.VK_CTRL_A: self.home,
            Keyboard.VK_CTRL_E: self.end,
            Keyboard.VK_CTRL_R: self.reset,
            Keyboard.VK_CTRL_F: self.forget_history,
            Keyboard.VK_HOME: self.home,
            Keyboard.VK_END: self.end,
            Keyboard.VK_TAB: self.complete
        })

    def _set_cursor_pos(self):
        """Set the cursor position on the input."""
        index_offset = max(0, self.length - self._input_index)
        self.screen.cursor.move(index_offset, Direction.LEFT)

    def _update_input(self, text: str) -> str:
        """Update the value of the input.
        :param text: The text to be set.
        """
        self._UNDO_HISTORY.append(self.text)
        self._HISTORY[-1] = text if text not in self._HISTORY else self.text
        self.text = text
        self._HIST_INDEX = max(0, len(self._HISTORY) - 1)
        return text

    def _render_suggestions(self) -> None:
        """Render the input suggestions."""
        edt_text: str = self.text
        filtered: list[str] = list(filter(lambda h: h.startswith(edt_text), self._HISTORY))
        hint: str = ''

        if edt_text and edt_text in filtered:
            edt_idx = filtered.index(edt_text) - 1
            index = max(0, min(edt_idx, self._HIST_INDEX))
            hint: str = get_or_default(filtered, index, '') or filtered[-1]
            if hint and (hint := hint[len(edt_text):]):
                self.write(f"%GRAY%{hint}%NC%")
                self._terminal.cursor.erase(Direction.DOWN)
                self.cursor.move(len(hint), Direction.LEFT)
            else:
                self._terminal.cursor.erase(Direction.DOWN)
        else:
            self._terminal.cursor.erase(Direction.DOWN)

        self._suggestion = hint

    def _next_in_history(self) -> str:
        """Return the next input in history."""
        edt_text: str = self._HISTORY[-1]
        filtered: list[str] = list(filter(lambda h: h.lower().startswith(edt_text.lower()), self._HISTORY))
        if edt_text in filtered:
            edt_idx = filtered.index(edt_text)
            index = min(edt_idx, self._HIST_INDEX + 1)
            text = get_or_default(filtered, index, None) or filtered[-1]
            self._HIST_INDEX = filtered.index(text)
            return text
        return edt_text

    def _prev_in_history(self) -> str:
        """Return the previous input in history."""
        edt_text: str = self._HISTORY[-1]
        filtered: list[str] = list(filter(lambda h: h.lower().startswith(edt_text.lower()), self._HISTORY))
        if edt_text in filtered:
            edt_idx = filtered.index(edt_text) - 1
            index = max(0, min(edt_idx, self._HIST_INDEX - 1))
            text = get_or_default(filtered, index, None) or filtered[-1]
            self._HIST_INDEX = filtered.index(text)
            return text
        return edt_text
