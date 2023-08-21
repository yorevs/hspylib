#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib
   @package: clitt.core.tui.minput
      @file: menu_input.py
   @created: Wed, 17 May 2023
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""
from clitt.core.icons.font_awesome.form_icons import FormIcons
from clitt.core.icons.font_awesome.nav_icons import NavIcons
from clitt.core.term.commons import Direction, get_cursor_position
from clitt.core.term.terminal import Terminal
from clitt.core.tui.minput import minput_utils as mu
from clitt.core.tui.minput.form_builder import FormBuilder
from clitt.core.tui.minput.form_field import FormField
from clitt.core.tui.minput.input_type import InputType
from clitt.core.tui.minput.minput_utils import MASK_SYMBOLS, VALUE_SEPARATORS
from clitt.core.tui.tui_component import TUIComponent
from functools import reduce
from hspylib.core.exception.exceptions import InvalidInputError, InvalidStateError
from hspylib.core.namespace import Namespace
from hspylib.core.tools.text_tools import xstr
from hspylib.modules.cli.keyboard import Keyboard
from operator import add
from time import sleep
from typing import List, Optional

import pyperclip
import re


class MenuInput(TUIComponent):
    """Provide a form input for terminal UIs."""

    NAV_ICONS = NavIcons.compose(NavIcons.UP, NavIcons.DOWN)

    @classmethod
    def builder(cls) -> FormBuilder:
        return FormBuilder()

    def __init__(self, title: str, fields: List[FormField]):
        super().__init__(title)
        self.fields = fields
        self.positions = [(0, 0) for _ in fields]
        self.cur_field = self._done = None
        self.cur_row = self.cur_col = self.tab_index = 0
        self.max_label_length = max(len(field.label) for field in fields)
        self.max_value_length = max(field.max_length for field in fields)
        self.max_detail_length = max(mu.detail_len(field) for field in fields)

    def execute(self) -> Optional[Namespace]:
        if len(self.fields) == 0:
            return None

        self._prepare_render()
        keypress = self._loop()

        if keypress == Keyboard.VK_ENTER:
            form_fields = Namespace("FormFields")
            for field in self.fields:
                form_fields.setattr(field.dest, field.value)
            return form_fields

        return None

    def render(self) -> None:
        Terminal.set_show_cursor(False)
        self.cursor.restore()
        self.writeln(f"{self.prefs.title_color.placeholder}{self.title}%EOL%%NC%")

        for idx, field in enumerate(self.fields):
            field_length = field.length
            if self.tab_index == idx:
                mu.mi_print(
                    self.screen, f"  {field.label}", self.prefs.sel_bg_color.placeholder, self.max_label_length + 2
                )
                self.cur_field = field
            else:
                mu.mi_print(self.screen, f"  {field.label}", field_len=self.max_label_length + 2)
            self._buffer_positions(idx, field_length)
            self._render_field(field)
            self._render_details(field, field_length)

        self.cursor.erase(Direction.DOWN)
        self.draw_navbar(self.navbar())
        self._re_render = False
        self._set_cursor_pos()
        Terminal.set_show_cursor()

    def navbar(self, **kwargs) -> str:
        return (
            f"%EOL%{NavIcons.POINTER} %GREEN%{self.cur_field.tooltip or f'the {self.cur_field.label.lower()}'}%NC%"
            f"%EOL%{self.prefs.navbar_color.placeholder}%EOL%"
            f"[Enter] Submit  [{self.NAV_ICONS}] "
            f"Navigate  [{NavIcons.TAB}] Next  [Space] Toggle  [^P] Paste  [Esc] Quit %NC%"
        )

    def handle_keypress(self) -> Keyboard:
        length = len(self.fields)

        if keypress := Keyboard.wait_keystroke():
            match keypress:
                case Keyboard.VK_ESC:
                    self._done = True
                case _ as key if key in [Keyboard.VK_TAB, Keyboard.VK_DOWN]:
                    self.tab_index = min(length - 1, self.tab_index + 1)
                case _ as key if key in [Keyboard.VK_SHIFT_TAB, Keyboard.VK_UP]:
                    self.tab_index = max(0, self.tab_index - 1)
                case Keyboard.VK_BACKSPACE:
                    if not self.cur_field.can_write():
                        self._display_error("This field is read only !")
                    else:
                        self._handle_backspace()
                case Keyboard.VK_CTRL_P:
                    self._handle_ctrl_p()
                case Keyboard.VK_ENTER:
                    return self._handle_enter()
                case _ as key if key.isalnum() or key.ispunct() or key == Keyboard.VK_SPACE:
                    if not self.cur_field.can_write():
                        self._display_error("This field is read only !")
                    else:
                        self._handle_input(keypress)

        self._re_render = True

        return keypress

    def _handle_enter(self) -> Optional[Keyboard]:
        """Handle 'enter' press. Validate & Save form and exit."""
        invalid = next((field for field in self.fields if not field.validate_field()), None)
        if invalid:
            idx = self.fields.index(invalid)
            pos = self.positions[idx]
            self.cur_row = pos[0]
            self.tab_index = idx
            self._display_error("Form field is not valid: " + str(invalid))
            return None

        for idx, field in enumerate(self.fields):
            match field.itype:
                case InputType.MASKED:
                    field.value = re.split(VALUE_SEPARATORS, field.value)[0]
                case InputType.CHECKBOX:
                    field.value = bool(field.value)
                case InputType.SELECT:
                    _, field.value = mu.get_selected(field.value)
        self._done = True
        return Keyboard.VK_ENTER

    def _handle_input(self, keypress: Keyboard) -> None:
        """Handle a form input.
        :param keypress: the input provided by the keypress.
        """

        match self.cur_field.itype:
            case InputType.CHECKBOX:
                if keypress == Keyboard.VK_SPACE:
                    self.cur_field.value = not self.cur_field.value
            case InputType.SELECT:
                if keypress == Keyboard.VK_SPACE:
                    if self.cur_field.value:
                        self.cur_field.value = mu.toggle_selected(xstr(self.cur_field.value))
            case InputType.MASKED:
                value, mask = mu.unpack_masked(xstr(self.cur_field.value))
                try:
                    self.cur_field.value = mu.append_masked(value, mask, keypress.value)
                except InvalidInputError as err:
                    self._display_error(str(err))
            case _:
                if len(xstr(self.cur_field.value)) < self.cur_field.max_length:
                    if self.cur_field.validate_input(keypress.value):
                        self.cur_field.value = (str(self.cur_field.value) if self.cur_field.value else "") + str(
                            keypress.value
                        )
                    else:
                        self._display_error(
                            f"Input '{keypress.value}' is invalid. "
                            f"This field takes only {self.cur_field.input_validator}!"
                        )

    def _handle_backspace(self) -> None:
        """Handle 'backspace' press. Delete previous input."""

        if self.cur_field.itype == InputType.MASKED:
            value, mask = mu.unpack_masked(str(self.cur_field.value))
            value = value[:-1]
            while mask[len(value) - 1] not in MASK_SYMBOLS:
                value = value[:-1]
            self.cur_field.value = f"{value}|{mask}"
        elif self.cur_field.itype not in [InputType.CHECKBOX, InputType.SELECT]:
            if self.cur_field.can_write() and len(str(self.cur_field.value)) >= 1:
                self.cur_field.value = str(self.cur_field.value)[:-1]
            elif not self.cur_field.can_write():
                self._display_error("This field is read only !")

    def _handle_ctrl_p(self) -> None:
        """Handle 'ctrl + p' press. Paste content from clipboard."""
        for c in pyperclip.paste():
            self._handle_input(Keyboard.of_value(c))

    def _set_cursor_pos(self) -> None:
        """Set the cursor at the right position according to the ATB index."""
        pos = self.positions[self.tab_index]
        self.screen.cursor.move_to(pos[0], pos[1] + self.cur_field.length)

    def _render_field(self, field: FormField) -> None:
        """Render the specified form field.
        :param field: the form field to render.
        """
        match field.itype:
            case InputType.TEXT:
                mu.mi_print(self.screen, xstr(field.value), field_len=self.max_value_length)
            case InputType.PASSWORD:
                mu.mi_print(self.screen, "*" * field.length, field_len=self.max_value_length)
            case InputType.CHECKBOX:
                mu.mi_print(
                    self.screen,
                    " ",
                    FormIcons.CHECK_SQUARE.unicode if field.value else FormIcons.UNCHECK_SQUARE.unicode,
                    field_len=self.max_value_length - 1,
                )
            case InputType.SELECT:
                if field.value:
                    mat = re.search(rf".*({VALUE_SEPARATORS})?<(.+)>({VALUE_SEPARATORS})?.*", str(field.value))
                    sel_value = mat.group(2) if mat else re.split(VALUE_SEPARATORS, str(field.value))[0]
                    mu.mi_print(self.screen, f"{sel_value}", field_len=self.max_value_length)
            case InputType.MASKED:
                value, mask = mu.unpack_masked(str(field.value))
                mu.mi_print(self.screen, mu.over_masked(value, mask), field_len=self.max_value_length)
            case _:
                raise InvalidStateError(f"Invalid form field type: {field.itype}")

    def _render_details(self, field: FormField, field_details: int) -> None:
        """Render details about total/remaining field characters.
        :param field: the form field to render.
        :param field_details: details about the form field (total / remaining) size.
        """
        padding = 1 - len(str(self.max_detail_length / 2))
        fmt = "{:<3}{:>" + str(padding) + "}/{:<" + str(padding) + "}  %NC%"
        if field.itype == InputType.SELECT:
            idx, _ = mu.get_selected(field.value)
            count = len(re.split(VALUE_SEPARATORS, field.value))
            self.writeln(fmt.format(field.icon, idx + 1 if idx >= 0 else 1, count))
        elif field.itype == InputType.MASKED:
            value, mask = mu.unpack_masked(xstr(field.value))
            self.writeln(
                fmt.format(
                    field.icon,
                    reduce(add, list(map(mask[: len(value)].count, MASK_SYMBOLS))),
                    reduce(add, list(map(mask.count, MASK_SYMBOLS))),
                )
            )
        else:
            self.writeln(fmt.format(field.icon, field_details, field.max_length))

    def _buffer_positions(self, field_index: int, field_size: int) -> None:
        """Buffer all cursor positions to avoid calling get_cursor_pos over and over because it is a very
        expensive call.
        :param field_index: the current form field index.
        :param field_size: the form field length.
        """
        if f_pos := get_cursor_position() if self.positions[field_index] == (0, 0) else self.positions[field_index]:
            self.positions[field_index] = f_pos
            if self.tab_index == field_index:
                self.cur_row, self.cur_col = f_pos[0], f_pos[1] + field_size

    def _display_error(self, err_msg: str) -> None:
        """Display a form filling or submitting error.
        :param err_msg: the error message.
        """
        Terminal.set_enable_echo(False)
        Terminal.set_show_cursor(False)
        offset = 15  # Sum of minput used characters that are not related to the field.
        err_pos = offset + self.max_label_length + self.max_value_length + self.max_detail_length
        self.cursor.move_to(self.cur_row, err_pos)
        mu.mi_print_err(self.screen, f"{FormIcons.ARROW_LEFT} {err_msg}")
        # This calculation gives a good delay amount based on the size of the message.
        sleep(max(2.0, int(len(err_msg) / 21)))
        Terminal.set_enable_echo()
        # Erase the message after the timeout
        self.cursor.move_to(self.cur_row, err_pos)
        self.cursor.erase(Direction.RIGHT)
        Terminal.set_show_cursor()
        self._re_render = True
