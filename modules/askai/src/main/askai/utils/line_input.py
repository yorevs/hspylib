#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib-AskAI
   @package: askai.utils
      @file: line_input.py
   @created: Wed, 17 Jan 2024
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright·(c)·2024,·HSPyLib
"""
from typing import Optional, List

import pyperclip
from clitt.core.term.commons import Portion, Direction
from clitt.core.term.terminal import Terminal
from clitt.core.tui.tui_component import TUIComponent
from hspylib.modules.cli.keyboard import Keyboard
from hspylib.modules.cli.vt100.vt_color import VtColor


def line_input(
    prompt: str = "",
    prompt_color: VtColor = VtColor.NC
) -> Optional[str | Keyboard]:
    """Read a string from standard input.
    :param prompt: The message to be displayed to the user.
    :param prompt_color: The color of the prompt text.
    """
    ptt = KeyboardInput(prompt, prompt_color)
    return ptt.execute()


class KeyboardInput(TUIComponent):
    """Provides a keyboard input for terminal UIs with undo and history."""

    # Current history index.
    _HIST_INDEX: int = 0

    # Dict containing all previously accepted inputs.
    _HISTORY: dict[int, str] = {}

    # Stack containing current input changes.
    _UNDO_HISTORY: List[str] = []

    # Stack containing current input reverts.
    _REDO_HISTORY: List[str] = []

    @classmethod
    def _add_history(cls, input_text: str) -> None:
        """Add the following input to the history set.
        :param input_text: The input text to add to the history.
        """
        if input_text:
            cls._HISTORY[max(1, len(cls._HISTORY))] = input_text

    @classmethod
    def _next_in_history(cls) -> Optional[str]:
        cls._HIST_INDEX = min(max(0, len(cls._HISTORY) - 1), cls._HIST_INDEX + 1)
        text = cls._HISTORY.get(cls._HIST_INDEX, "")
        return text or cls._HISTORY.get(cls._HIST_INDEX - 1, "")

    @classmethod
    def _prev_in_history(cls) -> Optional[str]:
        cls._HIST_INDEX = max(0, cls._HIST_INDEX - 1)
        text = cls._HISTORY.get(cls._HIST_INDEX, "")
        return text

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
        prompt_color: VtColor = VtColor.NC
    ):
        super().__init__(prompt)
        self._prompt_color = prompt_color
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
        while not self._done and keypress not in break_keys:

            # Menu Renderization
            if self._re_render:
                self.render()
            # Navigation input
            keypress = self.handle_keypress()

        return keypress

    def execute(self) -> Optional[str | Keyboard]:
        self._prepare_render()
        keypress = self._loop()

        if keypress == Keyboard.VK_ENTER:
            self._add_history(self._input_text)
            self.writeln("")
            self._UNDO_HISTORY.clear()
            self._REDO_HISTORY.clear()
        elif keypress == Keyboard.VK_ESC:
            self.writeln("")
            self._input_text = None

        return self._input_text

    def render(self) -> None:
        Terminal.set_show_cursor(False)
        self.cursor.restore()
        self._terminal.cursor.erase(Portion.LINE)
        self.write(f"{self._prompt_color.placeholder}{self.title}%NC%")
        self.write(self._input_text)
        index_offset = max(0, self.length - self._input_index)
        self.screen.cursor.move(index_offset, Direction.LEFT)
        self._re_render = False
        Terminal.set_show_cursor(True)

    def navbar(self, **kwargs) -> str:
        pass

    def handle_keypress(self) -> Keyboard:
        if keypress := Keyboard.wait_keystroke():
            match keypress:
                case Keyboard.VK_ESC:
                    self._done = True
                case Keyboard.VK_ENTER:
                    self._done = True
                case Keyboard.VK_BACKSPACE:
                    if self._input_index > 0:
                        self._input_index = max(0, self._input_index - 1)
                        self._update_input(
                            self._input_text[:self._input_index]
                            + self._input_text[1 + self._input_index:]
                        )
                case Keyboard.VK_DELETE:
                    self._update_input(
                        self._input_text[:self._input_index]
                        + self._input_text[1 + self._input_index:]
                    )
                case Keyboard.VK_CTRL_P:
                    self._update_input(pyperclip.paste() or self._input_text)
                    self._input_index = self.length
                case Keyboard.VK_CTRL_R:
                    self._input_index = 0
                    self._update_input("")
                case Keyboard.VK_CTRL_U:
                    undo_text = self._undo()
                    self._input_text = undo_text
                    self._input_index = self.length
                    self._HISTORY[0] = self._input_text
                case Keyboard.VK_CTRL_K:
                    redo_text = self._redo()
                    self._input_text = redo_text if redo_text else self._input_text
                    self._input_index = self.length
                    self._HISTORY[0] = self._input_text
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
                case _ as key if key.val.isprintable():
                    self._input_index += 1
                    self._update_input(
                        self._input_text[:self._input_index]
                        + key.val
                        + self._input_text[self._input_index:]
                    )
                case _:
                    self._input_text = keypress
                    self._done = True
        self._re_render = True

        return keypress

    def _update_input(self, text: str) -> str:
        """TODO"""
        self._UNDO_HISTORY.append(self._input_text)
        self._input_text = text
        self._HISTORY[0] = text
        return text


if __name__ == "__main__":
    print("-=" * 30)
    while (i := line_input("What is it? ")) not in ["bye", ""]:
        if isinstance(i, Keyboard):
            print(i)
        else:
            print("Input:", i)
