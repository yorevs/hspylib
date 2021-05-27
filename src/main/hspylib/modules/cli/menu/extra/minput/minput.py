#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.main.hspylib.modules.cli.menu.extra
      @file: minput.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

import re
import signal
import time
from typing import Any, List

from hspylib.core.exception.exceptions import InvalidInputError
from hspylib.core.tools.commons import sysout
from hspylib.core.tools.text_helper import camelcase
from hspylib.modules.cli.icons.font_awesome.form_icons import FormIcons
from hspylib.modules.cli.keyboard import Keyboard
from hspylib.modules.cli.menu.extra.minput.access_type import AccessType
from hspylib.modules.cli.menu.extra.minput.form_builder import FormBuilder
from hspylib.modules.cli.menu.extra.minput.form_field import FormField
from hspylib.modules.cli.menu.extra.minput.input_type import InputType
from hspylib.modules.cli.menu.extra.minput.minput_utils import MInputUtils
from hspylib.modules.cli.menu.menu_utils import MenuUtils
from hspylib.modules.cli.vt100.vt_100 import Vt100
from hspylib.modules.cli.vt100.vt_codes import vt_print
from hspylib.modules.cli.vt100.vt_colors import VtColors
from hspylib.modules.cli.vt100.vt_utils import get_cursor_position, set_enable_echo


def minput(
        form_fields: List[Any],
        title: str = 'Please fill all fields of the form fields below',
        title_color: VtColors = VtColors.ORANGE,
        nav_color: VtColors = VtColors.YELLOW) -> List[Any]:
    """
    TODO
    :param form_fields:
    :param title:
    :param title_color:
    :param nav_color:
    :return:
    """
    return MenuInput(form_fields).input(title, title_color, nav_color)


class MenuInput:

    SELECTED_BG = '%MOD(44)%'

    NAV_FMT = "{}[Enter] Submit  [\u2191\u2193] Navigate  [Tab] Next  [Space] Toggle  [Esc] Quit %EL0%"

    @classmethod
    def builder(cls) -> Any:
        return FormBuilder()

    def __init__(self, all_fields: List[Any]):
        self.all_fields = all_fields
        self.all_pos = [(0, 0) for _ in all_fields]
        self.cur_field = None
        self.cur_row = 0
        self.cur_col = 0
        self.tab_index = 0
        self.max_label_length = max([len(field.label) for field in all_fields])
        self.max_value_length = max([field.max_length for field in all_fields])
        self.max_detail_length = max([MInputUtils.detail_len(field) for field in all_fields])
        self.done = None
        self.re_render = True

    def input(
            self,
            title: str = 'Please fill all fields of the form below',
            title_color: VtColors = VtColors.ORANGE,
            nav_color: VtColors = VtColors.YELLOW) -> List[FormField]:

        ret_val = None
        length = len(self.all_fields)
        signal.signal(signal.SIGINT, MenuUtils.exit_app)
        signal.signal(signal.SIGHUP, MenuUtils.exit_app)

        if length > 0:
            sysout(f"%ED2%%HOM%{title_color.placeholder()}{title}")
            vt_print('%HOM%%CUD(1)%%ED0%')
            vt_print(Vt100.set_auto_wrap(False))
            vt_print(Vt100.set_show_cursor(False))
            vt_print(Vt100.save_cursor())

            # Wait for user interaction
            while not self.done and ret_val != Keyboard.VK_ENTER:
                # Menu Renderization {
                if self.re_render:
                    self._render(nav_color)
                # } Menu Renderization

                # Navigation input {
                ret_val = self._nav_input()
                # } Navigation input

        vt_print('%HOM%%ED2%%MOD(0)%')  # Clean screen before exiting
        sysout(Vt100.set_show_cursor(True))

        return self.all_fields if ret_val == Keyboard.VK_ENTER else []

    def _render(self, nav_color: VtColors) -> None:
        icon = ''
        # Restore the cursor to the home position
        vt_print(Vt100.restore_cursor())
        sysout('%NC%')
        set_enable_echo()

        for idx, field in enumerate(self.all_fields):
            field_size = len(str(field.value))
            if self.tab_index != idx:
                MInputUtils.mi_print(self.max_label_length, camelcase(field.label))
            else:
                MInputUtils.mi_print(self.max_label_length, camelcase(field.label), MenuInput.SELECTED_BG)
                # Buffering the all positions to avoid calling get_cursor_pos
                f_pos = get_cursor_position() if self.all_pos[idx] == (0, 0) else self.all_pos[idx]
                if f_pos:
                    self.cur_row = f_pos[0]
                    self.cur_col = f_pos[1] + field_size
                    self.all_pos[idx] = f_pos
                # Keep the selected field on hand
                self.cur_field = field

            # Choose the icon to display
            if field.itype == InputType.TEXT:
                icon = FormIcons.EDITABLE
                MInputUtils.mi_print(self.max_value_length, field.value)
            elif field.itype == InputType.PASSWORD:
                icon = FormIcons.HIDDEN
                MInputUtils.mi_print(self.max_value_length, '*' * field_size)
            elif field.itype == InputType.CHECKBOX:
                icon = FormIcons.MARKED
                if field.value:
                    MInputUtils.mi_print(self.max_value_length - 1, ' ', str(FormIcons.CHECK_SQUARE))
                else:
                    MInputUtils.mi_print(self.max_value_length - 1, ' ', str(FormIcons.UNCHECK_SQUARE))
            elif field.itype == InputType.SELECT:
                icon = FormIcons.SELECTABLE
                field_size = 1
                if field.value:
                    mat = re.search(r'.*\|?<(.+)>\|?.*', field.value)
                    if mat:
                        sel_value = mat.group(1)
                        MInputUtils.mi_print(
                            self.max_value_length, f'{sel_value}')
                    else:
                        sel_value = field.value.split('|')[0]
                        MInputUtils.mi_print(
                            self.max_value_length, f'{sel_value}')
            elif field.itype == InputType.MASKED:
                icon = FormIcons.MASKED
                value, mask = MInputUtils.unpack_masked(str(field.value))
                MInputUtils.mi_print(self.max_value_length, MInputUtils.over_masked(value, mask))

            if field.access_type == AccessType.READ_ONLY:
                icon = FormIcons.LOCKED

            # Remaining/max characters
            padding = 1 - len(str(self.max_detail_length / 2))
            fmt = "{:<3}{:>" + str(padding) + "}/{:<" + str(padding) + "} %MOD(0)%"
            if field.itype == InputType.SELECT:
                idx, _ = MInputUtils.get_selected(field.value)
                sysout(fmt.format(icon, idx + 1 if idx >= 0 else 1, len(field.value.split('|'))))
            elif field.itype == InputType.MASKED:
                value, mask = MInputUtils.unpack_masked(str(field.value))
                sysout(fmt.format(icon, len(value), field.max_length))
            else:
                sysout(fmt.format(icon, field_size, field.max_length))

        sysout('\n')
        sysout(MenuInput.NAV_FMT.format(nav_color.placeholder()), end='')
        self.re_render = False

    def _nav_input(self) -> chr:
        length = len(self.all_fields)
        keypress = Keyboard.read_keystroke()

        if not keypress:
            return None

        if keypress == Keyboard.VK_ESC:
            self.done = True
            sysout('\n%NC%')
        else:
            if keypress == Keyboard.VK_TAB:  # Handle TAB
                self.tab_index = min(length - 1, self.tab_index + 1)
            elif keypress == Keyboard.VK_SHIFT_TAB:  # Handle Shift + TAB
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
            elif keypress == Keyboard.VK_UP:  # Cursor up
                if self.tab_index - 1 >= 0:
                    self.tab_index -= 1
            elif keypress == Keyboard.VK_DOWN:  # Cursor down
                if self.tab_index + 1 < length:
                    self.tab_index += 1
            elif keypress == Keyboard.VK_ENTER:  # Validate & Save form and exit
                for idx in range(0, length):
                    field = self.all_fields[idx]
                    if field.itype == InputType.SELECT:
                        _, field.value = MInputUtils.get_selected(field.value)
                    else:
                        if not field.validate(field.value):
                            keypress = None
                            self._display_error(
                                f"Field \"{camelcase(field.label)}\" is not valid => \"{field.validator}\" !"
                            )
                            break
                        if field.itype == InputType.MASKED:
                            field.value = field.value.split('|')[0]

        self.re_render = True
        return keypress

    def _handle_input(self, keypress: chr):
        if self.cur_field.itype == InputType.CHECKBOX:
            if keypress == Keyboard.VK_SPACE:
                if not self.cur_field.can_write():
                    self._display_error('This field is read only !')
                elif not self.cur_field.value:
                    self.cur_field.value = 1
                else:
                    self.cur_field.value = 0
        elif self.cur_field.itype == InputType.SELECT:
            if keypress == Keyboard.VK_SPACE:
                if not self.cur_field.can_write():
                    self._display_error('This field is read only !')
                elif self.cur_field.value:
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
                    self.cur_field.value += keypress.value
                else:
                    self._display_error(
                        f"This {self.cur_field.itype} field only accept {self.cur_field.validator} !"
                    )

    def _handle_backspace(self):
        if self.cur_field.itype == InputType.MASKED:
            value, mask = MInputUtils.unpack_masked(str(self.cur_field.value))
            value = value[:-1]
            while mask[len(value)-1] not in ['#', '@', '*']:
                value = value[:-1]
            self.cur_field.value = f"{value}|{mask}"
        elif self.cur_field.itype not in [InputType.CHECKBOX, InputType.SELECT]:
            if self.cur_field.can_write() and len(self.cur_field.value) >= 1:
                self.cur_field.value = self.cur_field.value[:-1]
            elif not self.cur_field.can_write():
                self._display_error('This field is read only !')

    def _display_error(self, err_msg) -> None:
        err_offset = 12 + self.max_detail_length
        set_enable_echo(False)
        err_pos = self.max_label_length + self.max_value_length + err_offset
        vt_print(f"%CUP({self.cur_row};{err_pos})%")
        sysout(f"%RED% {FormIcons.ERROR}  {err_msg}", end='')
        time.sleep(max(2, int(len(err_msg) / 20)))
        set_enable_echo()
        vt_print(f"%CUP({self.cur_row};{err_pos})%%EL0%")  # Remove the message after the timeout
