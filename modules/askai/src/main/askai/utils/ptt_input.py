#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib-AskAI
   @package: askai.utils
      @file: ptt_input.py
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
from hspylib.core.preconditions import check_argument
from hspylib.modules.cli.keyboard import Keyboard
from hspylib.modules.cli.vt100.vt_color import VtColor


def ptt_input(
        prompt: str = "",
        ptt_keypress: Keyboard = Keyboard.VK_CTRL_L,
        prompt_color: VtColor = VtColor.NC
    ) -> Optional[str | Keyboard]:
    """Read a string from standard input.
    :param prompt: The message to be displayed to the user.
    :param ptt_keypress: The key assigned to trigger the push-to-talk.
    :param prompt_color: The color of the prompt text.
    """
    ptt = PTTInput(prompt, ptt_keypress, prompt_color)
    return ptt.execute()


class PTTInput(TUIComponent):
    """Provides a push-to-talk input for terminal UIs with history."""

    # fmt: off
    _RESERVED_KEYS = [
        Keyboard.VK_ESC,        # Used to interrupt the input.
        Keyboard.VK_ENTER,      # Used to accept the input.
        Keyboard.VK_LEFT,       # Used to navigate left on the current text.
        Keyboard.VK_RIGHT,      # Used to navigate right on the current text.
        Keyboard.VK_UP,         # Used to navigate get the previous entry in history.
        Keyboard.VK_BACKSPACE,  # Used to erase previous character.
        Keyboard.VK_DELETE,     # Used to erase current character.
        Keyboard.VK_CTRL_P,     # Used to paste from the clipboard.
        Keyboard.VK_CTRL_R,     # Used to reset the input.
        Keyboard.VK_CTRL_U,     # Used to undo last change.
    ]
    # fmt: on

    # Stack containing all previously accepted inputs.
    _HISTORY: List[str] = []

    # Stack containing current input changes.
    _UNDO_HISTORY: List[str] = []

    def __init__(
        self,
        prompt: str = "",
        ptt_keypress: Keyboard = Keyboard.VK_CTRL_L,
        prompt_color: VtColor = VtColor.NC
    ):
        super().__init__(prompt)
        self._input_text: str = ""
        self._hist_index: int = 0
        self._input_index = 0
        check_argument(
            ptt_keypress not in PTTInput._RESERVED_KEYS,
            f"The key {ptt_keypress} is reserved for internal use.",
        )
        self._ptt_keypress: Keyboard = ptt_keypress
        self._prompt_color = prompt_color

    def _prepare_render(self, auto_wrap: bool = False, show_cursor: bool = False) -> None:
        """Prepare the screen for renderization."""
        Terminal.set_auto_wrap(auto_wrap)
        Terminal.set_show_cursor(show_cursor)
        self.cursor.save()

    def _loop(self, break_keys: List[Keyboard] = None) -> Keyboard:
        """Loop and wait for a keypress. Render the component if required."""

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
            self.writeln("")
            return self._input_text
        elif keypress == Keyboard.VK_ESC:
            self.writeln("")
            return None

        return self._input_text

    def render(self) -> None:
        Terminal.set_show_cursor(False)
        self.cursor.restore()

        self._terminal.cursor.erase(Portion.LINE)
        self.write(f"{self._prompt_color.placeholder}{self.title}%NC%")
        self.write(self._input_text)

        self.screen.cursor.move(len(self._input_text) - self._input_index, Direction.LEFT)
        self._re_render = False
        Terminal.set_show_cursor()

    def navbar(self, **kwargs) -> str:
        pass

    def handle_keypress(self) -> Keyboard:
        if keypress := Keyboard.wait_keystroke():
            match keypress:
                case Keyboard.VK_ESC:
                    self._done = True
                case Keyboard.VK_ENTER:
                    self._done = True
                case self._ptt_keypress:
                    self._input_text = self._ptt_keypress
                    self._input_index = 0
                    self._done = True
                case Keyboard.VK_BACKSPACE:
                    if self._input_index > 0:
                        self._input_index = max(0, self._input_index - 1)
                        self._input_text = (
                            self._input_text[:self._input_index]
                            + self._input_text[1 + self._input_index:]
                        )
                case Keyboard.VK_DELETE:
                    self._input_text = (
                        self._input_text[:self._input_index]
                        + self._input_text[1 + self._input_index:]
                    )
                case Keyboard.VK_CTRL_P:
                    self._input_text = pyperclip.paste() or self._input_text
                    self._input_index = len(self._input_text)
                case Keyboard.VK_CTRL_R:
                    self._input_text = ""
                    self._input_index = 0
                case Keyboard.VK_LEFT:
                    self._input_index = max(0, self._input_index - 1)
                    self._terminal.cursor.move(2, Direction.LEFT)
                case Keyboard.VK_RIGHT:
                    self._input_index = min(
                        max(0, len(self._input_text)), self._input_index + 1
                    )
                    self._terminal.cursor.move(1, Direction.RIGHT)
                case _ as key if key.val.isprintable():
                    self._input_text = (
                        self._input_text[: self._input_index]
                        + key.val
                        + self._input_text[self._input_index :]
                    )
                    self._input_index += 1
                case _:
                    keypress = None
        self._re_render = True

        return keypress


if __name__ == "__main__":
    print("-=" * 30)
    while (i := ptt_input("What is it? ")) not in ["bye", ""]:
        if i == Keyboard.VK_CTRL_L:
            print("PTT")
        else:
            print("Input:", i)
