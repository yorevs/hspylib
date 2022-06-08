#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: main.modules.cli.tui.extra
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

from hspylib.core.exception.exceptions import InvalidInputError
from hspylib.core.tools.commons import new_dynamic_object, syserr, sysout
from hspylib.core.tools.text_tools import camelcase, snakecase
from hspylib.modules.cli.icons.font_awesome.form_icons import FormIcons
from hspylib.modules.cli.keyboard import Keyboard
from hspylib.modules.cli.tui.extra.minput.form_builder import FormBuilder
from hspylib.modules.cli.tui.extra.minput.form_field import FormField
from hspylib.modules.cli.tui.extra.minput.input_type import InputType
from hspylib.modules.cli.tui.extra.minput.minput_utils import MInputUtils
from hspylib.modules.cli.vt100.vt_codes import vt_print
from hspylib.modules.cli.vt100.vt_colors import VtColors
from hspylib.modules.cli.vt100.vt_utils import get_cursor_position, prepare_render, restore_cursor, restore_terminal, \
    set_enable_echo


def minput(
    form_fields: List[FormField],
    title: str = 'Please fill all fields of the form fields below',
    prefix: str = None,
    title_color: VtColors = VtColors.ORANGE,
    nav_color: VtColors = VtColors.YELLOW) -> Optional['MenuInput.FormFields']:
    """
    TODO
    :param form_fields:
    :param title:
    :param prefix:
    :param title_color:
    :param nav_color:
    :return:
    """
    return MenuInput(form_fields).input(title, prefix, title_color, nav_color)


class MenuInput:
    """TODO"""

    SELECTED_BG = '%MOD(44)%'

    NAV_ICONS = '\u2191\u2193'
    NAV_FMT = "\n{}[Enter] Submit  [{}] Navigate  [Tab] Next  [Space] Toggle  [Esc] Quit %EL0%"

    FormFields = new_dynamic_object('FormFields')  # New type definition to return filled fields

    @classmethod
    def builder(cls) -> FormBuilder:
        return FormBuilder()

    def __init__(self, all_fields: List[FormField]):
        self.all_fields = all_fields
        self.all_pos = [(0, 0) for _ in all_fields]
        self.cur_field = self.done = None
        self.cur_row = self.cur_col = self.tab_index = 0
        self.max_label_length = max([len(field.label) for field in all_fields])
        self.max_value_length = max([field.max_length for field in all_fields])
        self.max_detail_length = max([MInputUtils.detail_len(field) for field in all_fields])
        self.re_render = True

    def input(
        self,
        title: str,
        prefix: str,
        title_color: VtColors,
        nav_color: VtColors) -> Optional['MenuInput.FormFields']:
        """TODO"""

        ret_val = Keyboard.VK_NONE
        length = len(self.all_fields)

        if length == 0:
            return None

        prepare_render(title, title_color)

        # Wait for user interaction
        while not self.done and ret_val not in [Keyboard.VK_ENTER, Keyboard.VK_ESC]:
            # Menu Renderization
            if self.re_render:
                self._render(nav_color)

            # Navigation input
            ret_val = self._nav_input()

        restore_terminal()

        if ret_val == Keyboard.VK_ENTER:
            form_fields = self.FormFields
            for field in self.all_fields:
                att_name = f"{prefix or ''}{snakecase(field.label)}"
                setattr(form_fields, att_name, field.value)
            return form_fields

        return None

    def _render(self, nav_color: VtColors) -> None:
        """TODO"""

        restore_cursor()

        for idx, field in enumerate(self.all_fields):

            field_size = len(str(field.value))
            if self.tab_index == idx:
                MInputUtils.mi_print(self.max_label_length, camelcase(field.label), MenuInput.SELECTED_BG)
                self.cur_field = field
            else:
                MInputUtils.mi_print(self.max_label_length, camelcase(field.label))

            self._buffer_pos(field_size, idx)

            if field.itype == InputType.TEXT:
                MInputUtils.mi_print(self.max_value_length, field.value)
            elif field.itype == InputType.PASSWORD:
                MInputUtils.mi_print(self.max_value_length, '*' * field_size)
            elif field.itype == InputType.CHECKBOX:
                MInputUtils.mi_print(
                    self.max_value_length - 1, ' ', str(FormIcons.CHECK_SQUARE)
                    if field.value else str(FormIcons.UNCHECK_SQUARE))
            elif field.itype == InputType.SELECT:
                field_size = 1
                if field.value:
                    mat = re.search(r'.*\|?<(.+)>\|?.*', field.value)
                    sel_value = mat.group(1) if mat else field.value.split('|')[0]
                    MInputUtils.mi_print(self.max_value_length, f'{sel_value}')
            elif field.itype == InputType.MASKED:
                value, mask = MInputUtils.unpack_masked(str(field.value))
                MInputUtils.mi_print(self.max_value_length, MInputUtils.over_masked(value, mask))

            # Remaining/max characters
            self._render_details(field, field_size)

        sysout(self.NAV_FMT.format(nav_color.placeholder(), self.NAV_ICONS), end='')
        self.re_render = False

    def _buffer_pos(self, field_size: int, idx: int) -> None:
        """TODO"""

        # Buffering the all positions to avoid calling get_cursor_pos over and over
        f_pos = get_cursor_position() if self.all_pos[idx] == (0, 0) else self.all_pos[idx]
        if f_pos:
            self.all_pos[idx] = f_pos
            if self.tab_index == idx:
                self.cur_row = f_pos[0]
                self.cur_col = f_pos[1] + field_size

    def _render_details(self, field: FormField, field_size: int) -> None:
        """TODO"""

        # Print details about total/remaining field characters
        padding = 1 - len(str(self.max_detail_length / 2))
        fmt = '{:<3}{:>' + str(padding) + '}/{:<' + str(padding) + '} %MOD(0)%'
        if field.itype == InputType.SELECT:
            idx, _ = MInputUtils.get_selected(field.value)
            sysout(fmt.format(field.icon, idx + 1 if idx >= 0 else 1, len(field.value.split('|'))))
        elif field.itype == InputType.MASKED:
            value, _ = MInputUtils.unpack_masked(str(field.value))
            sysout(fmt.format(field.icon, len(value), field.max_length))
        else:
            sysout(fmt.format(field.icon, field_size, field.max_length))

    # pylint: disable=too-many-branches
    def _nav_input(self) -> chr:
        """TODO"""

        length = len(self.all_fields)
        keypress = Keyboard.read_keystroke()

        if keypress:
            if keypress == Keyboard.VK_ESC:
                self.done = True
            elif keypress in [Keyboard.VK_TAB, Keyboard.VK_DOWN]:  # Handle TAB and Cursor down
                self.tab_index = min(length - 1, self.tab_index + 1)
            elif keypress in [Keyboard.VK_SHIFT_TAB, Keyboard.VK_UP]:  # Handle Shift + TAB and Cursor up
                self.tab_index = max(0, self.tab_index - 1)
            elif keypress == Keyboard.VK_BACKSPACE:  # Handle backspace
                if not self.cur_field.can_write():
                    self._display_error('This field is read only !')
                else:
                    self._handle_backspace()
            elif keypress.isalnum() or keypress.ispunct() or keypress == Keyboard.VK_SPACE:  # Handle an input
                if not self.cur_field.can_write():
                    self._display_error('This field is read only !')
                else:
                    self._handle_input(keypress)
            elif keypress == Keyboard.VK_ENTER:  # Validate & Save form and exit
                for idx, field in enumerate(self.all_fields):
                    self.cur_row = self.all_pos[idx][0]
                    if not field.validate(field.value):
                        keypress = None
                        self._display_error(
                            f"Field \"{camelcase(field.label)}\" is not valid => \"{field.validator}\" !")
                        break
                    if field.itype == InputType.MASKED:
                        field.value = field.value.split('|')[0]
                    elif field.itype == InputType.CHECKBOX:
                        field.value = bool(field.value)
                    elif field.itype == InputType.SELECT:
                        _, field.value = MInputUtils.get_selected(field.value)

        self.re_render = True
        return keypress

    def _handle_input(self, keypress: chr) -> None:
        """TODO"""

        if self.cur_field.itype == InputType.CHECKBOX:
            if keypress == Keyboard.VK_SPACE:
                self.cur_field.value = 1 if not self.cur_field.value else 0
        elif self.cur_field.itype == InputType.SELECT:
            if keypress == Keyboard.VK_SPACE:
                if self.cur_field.value:
                    self.cur_field.value = MInputUtils.toggle_selected(str(self.cur_field.value))
        elif self.cur_field.itype == InputType.MASKED:
            value, mask = MInputUtils.unpack_masked(str(self.cur_field.value))
            if len(value) < self.cur_field.max_length:
                try:
                    self.cur_field.value = MInputUtils.append_masked(value, mask, keypress.value)
                except InvalidInputError as err:
                    self._display_error(f"{str(err)}")
        else:
            if len(str(self.cur_field.value)) < self.cur_field.max_length:
                if self.cur_field.validate(keypress.value):
                    self.cur_field.value = str(self.cur_field.value) + str(keypress.value)
                else:
                    self._display_error(
                        f"This {self.cur_field.itype} field only accept {self.cur_field.validator} !")

    def _handle_backspace(self) -> None:
        """TODO"""

        if self.cur_field.itype == InputType.MASKED:
            value, mask = MInputUtils.unpack_masked(str(self.cur_field.value))
            value = value[:-1]
            while mask[len(value) - 1] not in ['#', '@', '*']:
                value = value[:-1]
            self.cur_field.value = f"{value}|{mask}"
        elif self.cur_field.itype not in [InputType.CHECKBOX, InputType.SELECT]:
            if self.cur_field.can_write() and len(str(self.cur_field.value)) >= 1:
                self.cur_field.value = str(self.cur_field.value)[:-1]
            elif not self.cur_field.can_write():
                self._display_error('This field is read only !')

    def _display_error(self, err_msg) -> None:
        """TODO"""

        set_enable_echo(False)
        err_pos = self.max_label_length + self.max_value_length + self.max_detail_length + 12
        vt_print(f"%CUP({self.cur_row};{err_pos})%")
        syserr(f"{FormIcons.ERROR}  {err_msg}", end='')
        time.sleep(max(2, int(len(err_msg) / 25)))
        set_enable_echo()
        vt_print(f"%CUP({self.cur_row};{err_pos})%%EL0%")  # Remove the message after the timeout
