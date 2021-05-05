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

from hspylib.core.tools.commons import sysout
from hspylib.core.tools.keyboard import Keyboard
from hspylib.modules.cli.icons.font_awesome.form_icons import FormIcons
from hspylib.modules.cli.menu.menu_utils import MenuUtils
from hspylib.modules.cli.vt100.vt_100 import Vt100
from hspylib.modules.cli.vt100.vt_codes import vt_print
from hspylib.modules.cli.vt100.vt_colors import VtColors
from hspylib.modules.cli.vt100.vt_utils import get_cursor_position, set_enable_echo


def minput(
        form_fields: List[Any],
        title: str = 'Please fill all fields of the form fields below',
        title_color: VtColors = VtColors.ORANGE,
        nav_color: VtColors = VtColors.YELLOW) -> Any:
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
    __mi_modes__ = ['input', 'password', 'checkbox']
    __mi_kinds__ = ['letter', 'number', 'word', 'any']
    __mi_access_types__ = ['read-only', 'read-write']
    
    SELECTED_BG = '%MOD(44)%'
    
    @staticmethod
    class Field:
        def __init__(
                self,
                label: str = None,
                mode: str = 'input',
                kind: str = 'any',
                min_length: int = 0,
                max_length: int = 30,
                access_type: str = 'read-write',
                value: Any = None):
            
            self.label = label
            self.mode = mode
            self.kind = kind
            self.min_length = min_length
            self.max_length = max_length
            self.access_type = access_type
            self.value = value
        
        def __str__(self) -> str:
            return str(self.__dict__)
        
        def can_write(self) -> bool:
            return self.access_type == 'read-write'
        
        def val_regex(self, min_length: int, max_length: int) -> str:
            if self.kind == 'letter':
                regex = r'^[a-zA-Z]{' + str(min_length) + ',' + str(max_length) + '}$'
            elif self.kind == 'number':
                regex = r'^[0-9]{' + str(min_length) + ',' + str(max_length) + '}$'
            elif self.kind == 'word':
                regex = r'^[a-zA-Z0-9 _]{' + str(min_length) + ',' + str(max_length) + '}$'
            else:
                regex = r'.{' + str(min_length) + ',' + str(max_length) + '}$'
            
            return regex
    
    @staticmethod
    class FormBuilder:
        def __init__(self):
            self.fields = []
        
        def field(self) -> Any:
            return MenuInput.FieldBuilder(self)
        
        def build(self) -> list:
            return self.fields
    
    @staticmethod
    class FieldBuilder:
        def __init__(self, parent: Any):
            self.parent = parent
            self.field = MenuInput.Field()
        
        def label(self, label: str) -> Any:
            self.field.label = label
            return self
        
        def mode(self, mode: str) -> Any:
            assert mode in MenuInput.__mi_modes__, \
                f"Not a valid mode: {mode}. Valid modes are: {str(MenuInput.__mi_modes__)}"
            self.field.mode = mode
            return self
        
        def kind(self, kind: str) -> Any:
            assert kind in MenuInput.__mi_kinds__, \
                f"Not a valid kind: {kind}. Valid kinds are: {str(MenuInput.__mi_kinds__)}"
            self.field.kind = kind
            
            return self
        
        def min_max_length(self, min_length: int, max_length: int) -> Any:
            assert max_length >= min_length, f"Not a valid field length: ({min_length}-{max_length})"
            assert max_length > 0 and min_length > 0, f"Not a valid field length: ({min_length}-{max_length})"
            self.field.min_length = min_length
            self.field.max_length = max_length
            return self
        
        def access_type(self, access_type: str) -> Any:
            assert access_type in MenuInput.__mi_access_types__, \
                f"Not a valid access type {access_type}. Valid access types are: {str(MenuInput.__mi_access_types__)}"
            self.field.access_type = access_type
            return self
        
        def value(self, value: Any) -> Any:
            re_valid = self.field.val_regex(0, len(str(value)))
            if value:
                assert re.match(re_valid, value), \
                    f"Not a valid value: \"{value}\". Valid regex is \"{re_valid}\""
            self.field.value = value
            return self
        
        def build(self) -> Any:
            if self.field.mode == "checkbox":
                self.field.value = self.field.value if self.field.value in ['0', '1'] else 0
                self.field.min_length = self.field.max_length = 1
            self.field.label = self.field.label or 'Field'
            self.field.access_type = self.field.access_type or 'read-write'
            self.field.min_length = self.field.min_length or 1
            self.field.max_length = self.field.max_length or 30
            self.field.kind = self.field.kind or 'any'
            self.field.kind = self.field.kind or 'input'
            self.field.value = self.field.value or ''
            self.parent.fields.append(self.field)
            return self.parent
    
    @staticmethod
    def __detail_len__(field: Any) -> int:
        max_len = len(str(field.max_length))
        return 1 + (2 * max_len)
    
    @classmethod
    def mi_print(cls, size: int, text: str, prepend: str = None, end: str = '') -> None:
        fmt = ('{}' if prepend else '') + "{:<" + str(size) + "} : "
        if prepend:
            vt_print(fmt.format(prepend, text), end=end)
        else:
            vt_print(fmt.format(text), end=end)
    
    @classmethod
    def builder(cls) -> Any:
        return cls.FormBuilder()
    
    def __init__(self, all_fields: List[Any]):
        self.all_fields = all_fields
        self.all_pos = [(0, 0) for _ in all_fields]
        self.cur_field = None
        self.cur_row = 0
        self.cur_col = 0
        self.tab_index = 0
        self.err_msg = ''
        self.max_label_length = max([len(field.label) for field in all_fields])
        self.max_value_length = max([field.max_length for field in all_fields])
        self.max_detail_length = max([self.__detail_len__(field) for field in all_fields])
        self.done = None
        self.re_render = True
    
    def input(
            self,
            title: str = 'Please fill all fields of the form fields below',
            title_color: VtColors = VtColors.ORANGE,
            nav_color: VtColors = VtColors.YELLOW) -> List[Any]:
        
        ret_val = None
        length = len(self.all_fields)
        signal.signal(signal.SIGINT, MenuUtils.exit_app)
        signal.signal(signal.SIGHUP, MenuUtils.exit_app)
        
        if length > 0:
            sysout(f"%ED2%%HOM%{title_color.placeholder()}{title}")
            vt_print(Vt100.set_auto_wrap(False))
            vt_print('%HOM%%CUD(1)%%ED0%')
            vt_print(Vt100.save_cursor())
            
            # Wait for user interaction
            while not self.done and ret_val != Keyboard.VK_ENTER:
                # Menu Renderization {
                if self.re_render:
                    self.__render__(nav_color)
                # } Menu Renderization
                
                vt_print(Vt100.set_show_cursor(True))
                
                # Position the cursor to edit the current field
                if self.cur_field.mode != 'checkbox':
                    vt_print(f"%CUP({self.cur_row};{self.cur_col})%")
                else:
                    vt_print(f"%CUP({self.cur_row};{self.max_label_length + 6})%")
                
                # Navigation input {
                ret_val = self.__nav_input__()
                self.re_render = True
                # } Navigation input
        
        vt_print('%HOM%%ED2%%MOD(0)%')
        
        return self.all_fields if ret_val == Keyboard.VK_ENTER else []
    
    def __render__(self, nav_color: VtColors) -> None:
        icon = ''
        vt_print(Vt100.set_show_cursor(False))
        # Restore the cursor to the home position
        vt_print(Vt100.restore_cursor())
        sysout('%NC%')
        set_enable_echo()
        vt_print(Vt100.set_show_cursor(False))
        
        for idx, field in enumerate(self.all_fields):
            field_size = len(str(field.value))
            if self.tab_index != idx:
                MenuInput.mi_print(self.max_label_length, field.label)
            else:
                MenuInput.mi_print(self.max_label_length, field.label, MenuInput.SELECTED_BG)
                # Buffering the all positions to avoid calling get_cursor_pos
                f_pos = get_cursor_position() if self.all_pos[idx] == (0, 0) else self.all_pos[idx]
                if f_pos:
                    self.cur_row = f_pos[0]
                    self.cur_col = f_pos[1] + field_size
                    self.all_pos[idx] = f_pos
                # Keep the selected field on hand
                self.cur_field = field
            
            # Choose the icon to display
            if field.mode == "input":
                icon = FormIcons.EDITABLE
                MenuInput.mi_print(self.max_value_length, field.value)
            elif field.mode == "password":
                icon = FormIcons.HIDDEN
                MenuInput.mi_print(self.max_value_length, '*' * field_size)
            elif field.mode == "checkbox":
                icon = FormIcons.EDITABLE
                if field.value:
                    MenuInput.mi_print(self.max_value_length - 1, ' ', str(FormIcons.CHECK_SQUARE))
                else:
                    MenuInput.mi_print(self.max_value_length - 1, ' ', str(FormIcons.UNCHECK_SQUARE))
            if field.access_type == 'read-only':
                icon = FormIcons.LOCKED
            
            # Remaining/max characters
            padding = 1 - len(str(self.max_detail_length / 2))
            fmt = "{:<3}{:>" + str(padding) + "}/{:<" + str(padding) + "} %MOD(0)%"
            sysout(fmt.format(icon, field_size, field.max_length))
            
            # Display any previously set error message
            if self.tab_index == idx and self.err_msg:
                self.__display_error__()
                return
        
        sysout('\n')
        sysout(
            f"{nav_color.placeholder()}[Enter] Submit  [\u2191\u2193] Navigate  [Tab] Next  [Esc] Quit %EL0%", end='')
        self.re_render = False
    
    def __display_error__(self) -> None:
        err_offset = 12 + self.max_detail_length
        set_enable_echo(False)
        err_pos = self.max_label_length + self.max_value_length + err_offset
        vt_print(f"%CUP({self.cur_row};{err_pos})%")
        sysout(f"%RED% {FormIcons.ERROR}  {self.err_msg}", end='')
        dismiss_timeout = 1 + (len(self.err_msg) / 25)
        time.sleep(dismiss_timeout)
        # Remove the message after the timeout
        set_enable_echo()
        vt_print(f"%CUP({self.cur_row};{err_pos})%%EL0%")
        self.err_msg = ''
    
    def __nav_input__(self) -> chr:
        length = len(self.all_fields)
        keypress = Keyboard.read_keystroke()
        
        if not keypress:
            return None
        
        if keypress == Keyboard.VK_ESC:
            self.done = True
            sysout('\n%NC%')
        else:
            if keypress == Keyboard.VK_TAB:  # Handle TAB
                # Validate and move next. First case statement because next one also captures it
                min_len = self.cur_field.min_length
                if min_len <= len(str(self.cur_field.value)):
                    if self.tab_index + 1 < length:
                        self.tab_index += 1
                    else:
                        self.tab_index = 0
                else:
                    self.err_msg = f"This field does not match the minimum length of {min_len}"
            elif keypress == Keyboard.VK_BACKSPACE:  # Handle backspace
                if self.cur_field.can_write() and len(self.cur_field.value) >= 1:
                    self.cur_field.value = self.cur_field.value[:-1]
                elif self.cur_field.access_type == 'read-only':
                    self.err_msg = 'This field is read only !'
            elif keypress.isalnum() or keypress.ispunct() or keypress == Keyboard.VK_SPACE:  # Handle an input
                if not self.cur_field.can_write():
                    self.err_msg = 'This field is read only !'
                else:
                    if self.cur_field.mode == "checkbox":
                        if keypress == Keyboard.VK_SPACE:
                            if not self.cur_field.value:
                                self.cur_field.value = 1
                            else:
                                self.cur_field.value = 0
                    else:
                        if len(str(self.cur_field.value)) < self.cur_field.max_length:
                            if re.match(self.cur_field.val_regex(1, self.cur_field.max_length), keypress.value):
                                # Append value to the current field if the value matches the input type
                                self.cur_field.value += keypress.value
                            else:
                                self.err_msg = f"This {self.cur_field.mode} field only accept {self.cur_field.kind}s !"
            elif keypress == Keyboard.VK_UP:  # Cursor up
                if self.tab_index - 1 >= 0:
                    self.tab_index -= 1
            elif keypress == Keyboard.VK_DOWN:  # Cursor down
                if self.tab_index + 1 < length:
                    self.tab_index += 1
            elif keypress == Keyboard.VK_ENTER:  # Validate & Save the form and exit
                for idx in range(0, length):
                    field = self.all_fields[idx]
                    val_regex = field.val_regex(field.min_length, field.max_length)
                    if not re.match(val_regex, str(field.value)):
                        self.err_msg = f"Field \"{field.label}\" is not valid => \"{val_regex}\" !"
                        keypress = None
                        self.__display_error__()
                        break
        
        return keypress
