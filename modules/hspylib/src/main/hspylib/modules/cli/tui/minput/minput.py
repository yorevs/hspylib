#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: main.modules.cli.tui.components
      @file: minput.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
import re
import time
from typing import List, Optional

import pyperclip

from hspylib.core.exception.exceptions import InvalidInputError
from hspylib.core.namespace import Namespace
from hspylib.core.tools.commons import syserr, sysout
from hspylib.modules.cli.icons.font_awesome.form_icons import FormIcons
from hspylib.modules.cli.icons.font_awesome.nav_icons import NavIcons
from hspylib.modules.cli.keyboard import Keyboard
from hspylib.modules.cli.tui.minput.form_builder import FormBuilder
from hspylib.modules.cli.tui.minput.form_field import FormField
from hspylib.modules.cli.tui.minput.input_type import InputType
from hspylib.modules.cli.tui.minput.minput_utils import MInputUtils
from hspylib.modules.cli.tui.tui_component import TUIComponent
from hspylib.modules.cli.vt100.vt_utils import (
    get_cursor_position, prepare_render, restore_cursor, set_enable_echo,
)


def minput(
    form_fields: List[FormField],
    title: str = "Please fill all fields of the form fields below"
) -> Optional[Namespace]:
    """
    TODO
    :param form_fields:
    :param title:
    :return:
    """
    return MenuInput(title, form_fields).execute()


class MenuInput(TUIComponent):
    """TODO"""

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
        self.max_detail_length = max(MInputUtils.detail_len(field) for field in fields)

    def execute(self) -> Optional[Namespace]:
        """TODO"""

        if len(self.fields) == 0:
            return None

        keypress = Keyboard.VK_NONE
        prepare_render()

        # Wait for user interaction
        while not self._done:
            # Menu Renderization
            if self._re_render:
                self._render()

            # Navigation input
            keypress = self._handle_keypress()

        if keypress == Keyboard.VK_ENTER:
            form_fields = Namespace("FormFields")
            for field in self.fields:
                form_fields.setattr(field.dest, field.value)
            return form_fields

        return None

    def _render(self) -> None:
        """TODO"""

        restore_cursor()
        sysout(f"{self.prefs.title_color.placeholder}{self.title}%EOL%%NC%")

        for idx, field in enumerate(self.fields):

            field_size = field.width
            if self.tab_index == idx:
                MInputUtils.mi_print(self.max_label_length + 2, f"  {field.label}", self.prefs.sel_bg_color.placeholder)
                self.cur_field = field
            else:
                MInputUtils.mi_print(self.max_label_length + 2, f"  {field.label}")

            self._buffer_pos(field_size, idx)
            self._render_field(field)
            self._render_details(field, field_size)

        sysout(self._navbar(), end="")
        self._re_render = False

    def _render_field(self, field: FormField) -> None:
        """Render the form field"""
        if field.itype == InputType.TEXT:
            MInputUtils.mi_print(self.max_value_length, field.value)
        elif field.itype == InputType.PASSWORD:
            MInputUtils.mi_print(self.max_value_length, "*" * field.width)
        elif field.itype == InputType.CHECKBOX:
            MInputUtils.mi_print(
                self.max_value_length - 1,
                " ",
                str(FormIcons.CHECK_SQUARE) if field.value else str(FormIcons.UNCHECK_SQUARE),
            )
        elif field.itype == InputType.SELECT:
            if field.value:
                mat = re.search(r".*\|?<(.+)>\|?.*", field.value)
                sel_value = mat.group(1) if mat else field.value.split("|")[0]
                MInputUtils.mi_print(self.max_value_length, f"{sel_value}")
        elif field.itype == InputType.MASKED:
            value, mask = MInputUtils.unpack_masked(str(field.value))
            MInputUtils.mi_print(self.max_value_length, MInputUtils.over_masked(value, mask))

    def _render_details(self, field: FormField, field_size: int) -> None:
        """Render details about total/remaining field characters"""
        padding = 1 - len(str(self.max_detail_length / 2))
        fmt = "{:<3}{:>" + str(padding) + "}/{:<" + str(padding) + "}  %NC%"
        if field.itype == InputType.SELECT:
            idx, _ = MInputUtils.get_selected(field.value)
            sysout(fmt.format(field.icon, idx + 1 if idx >= 0 else 1, len(field.value.split("|"))))
        elif field.itype == InputType.MASKED:
            value, _ = MInputUtils.unpack_masked(str(field.value))
            sysout(fmt.format(field.icon, len(value), field.max_length))
        else:
            sysout(fmt.format(field.icon, field_size, field.max_length))

    def _navbar(self) -> str:
        return \
            f"\n{self.prefs.navbar_color.placeholder}" \
            f"[Enter] Submit  [{self.NAV_ICONS}] " \
            f"Navigate  [{NavIcons.TAB}] Next  [Space] Toggle  [^P] Paste  [Esc] Quit %NC%%EL0%%EOL%%EOL%"

    def _handle_keypress(self) -> Keyboard:
        """TODO"""

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
                    self._handle_enter()
                case _ as key if key.isalnum() or key.ispunct() or key == Keyboard.VK_SPACE:
                    if not self.cur_field.can_write():
                        self._display_error("This field is read only !")
                    else:
                        self._handle_input(keypress)

        self._re_render = True

        return keypress

    def _handle_enter(self) -> None:
        """Validate & Save form and exit"""

        invalid = next((field for field in self.fields if not field.validate(field.value)), None)
        if invalid:
            idx = self.fields.index(invalid)
            self.cur_row = self.positions[idx][0]
            self.tab_index = idx
            self._display_error("Form field is not valid: " + str(invalid))
        else:
            for idx, field in enumerate(self.fields):
                match field.itype:
                    case InputType.MASKED:
                        field.value = field.value.split("|")[0]
                    case InputType.CHECKBOX:
                        field.value = bool(field.value)
                    case InputType.SELECT:
                        _, field.value = MInputUtils.get_selected(field.value)
            self._done = True

    def _handle_input(self, keypress: Keyboard) -> None:
        """TODO"""

        match self.cur_field.itype:
            case InputType.CHECKBOX:
                if keypress == Keyboard.VK_SPACE:
                    self.cur_field.value = 1 if not self.cur_field.value else 0
            case InputType.SELECT:
                if keypress == Keyboard.VK_SPACE:
                    if self.cur_field.value:
                        self.cur_field.value = MInputUtils.toggle_selected(str(self.cur_field.value))
            case InputType.MASKED:
                value, mask = MInputUtils.unpack_masked(str(self.cur_field.value))
                if len(value) < self.cur_field.max_length:
                    try:
                        self.cur_field.value = MInputUtils.append_masked(value, mask, keypress.value)
                    except InvalidInputError as err:
                        self._display_error(f"{str(err)}")
            case _:
                if len(str(self.cur_field.value)) < self.cur_field.max_length:
                    if self.cur_field.validate(keypress.value):
                        self.cur_field.value = str(self.cur_field.value) + str(keypress.value)
                    else:
                        self._display_error(
                            f"This field only accept {self.cur_field.validator} !")

    def _handle_backspace(self) -> None:
        """TODO"""

        if self.cur_field.itype == InputType.MASKED:
            value, mask = MInputUtils.unpack_masked(str(self.cur_field.value))
            value = value[:-1]
            while mask[len(value) - 1] not in ["#", "@", "*"]:
                value = value[:-1]
            self.cur_field.value = f"{value}|{mask}"
        elif self.cur_field.itype not in [InputType.CHECKBOX, InputType.SELECT]:
            if self.cur_field.can_write() and len(str(self.cur_field.value)) >= 1:
                self.cur_field.value = str(self.cur_field.value)[:-1]
            elif not self.cur_field.can_write():
                self._display_error("This field is read only !")

    def _handle_ctrl_p(self) -> None:
        """TODO"""
        for c in pyperclip.paste():
            self._handle_input(Keyboard.of_value(c))

    def _buffer_pos(self, field_size: int, idx: int) -> None:
        """TODO"""

        # Buffering the all positions to avoid calling get_cursor_pos over and over
        if f_pos := get_cursor_position() if self.positions[idx] == (0, 0) else self.positions[idx]:
            self.positions[idx] = f_pos
            if self.tab_index == idx:
                self.cur_row, self.cur_col = f_pos[0], f_pos[1] + field_size

    def _display_error(self, err_msg) -> None:
        """TODO"""
        set_enable_echo(False)
        offset = 16
        err_pos = self.max_label_length + self.max_value_length + self.max_detail_length + offset
        sysout(f"%CUP({self.cur_row};{err_pos})%", end="")
        syserr(f"{FormIcons.ERROR_CIRCLE}  {err_msg}", end="")
        time.sleep(max(2, int(len(err_msg) / 25)))
        set_enable_echo()
        sysout(f"%CUP({self.cur_row};{err_pos})%%EL0%", end="")  # Remove the message after the timeout
