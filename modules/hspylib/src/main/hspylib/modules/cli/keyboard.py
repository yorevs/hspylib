#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib
   @package: hspylib.modules.cli
      @file: keyboard.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright·(c)·2024,·HSPyLib
"""
from hspylib.core.enums.enumeration import Enumeration
from hspylib.core.exception.exceptions import KeyboardInputError
from typing import List, Optional

import getkey
import os
import select
import string
import sys
import termios


# pylint: disable=multiple-statements
class Keyboard(Enumeration):
    """Provides keyboard interaction with the terminal."""

    # fmt: off

    # 'Esc' keys
    VK_NONE         = '';                     VK_DISABLED = ''
    VK_ESC          = getkey.keys.ESC

    # 'Enter' keys
    VK_ENTER        = os.linesep;             VK_CRLF       = '\r\n'
    VK_CR           = '\r';                   VK_LF         = '\n'

    # Navigation keys
    VK_UP           = getkey.keys.UP;         VK_DELETE     = getkey.keys.DELETE
    VK_DOWN         = getkey.keys.DOWN;       VK_SPACE      = getkey.keys.SPACE
    VK_LEFT         = getkey.keys.LEFT;       VK_HOME       = getkey.keys.HOME
    VK_RIGHT        = getkey.keys.RIGHT;      VK_END        = getkey.keys.END
    VK_BACKSPACE    = getkey.keys.BACKSPACE;  VK_PAGE_UP    = getkey.keys.PAGE_UP
    VK_INSERT       = getkey.keys.INSERT;     VK_PAGE_DOWN  = getkey.keys.PAGE_DOWN
    VK_TAB          = '\t';                   VK_SHIFT_TAB  = '\x1b[Z'

    # Control/Command keys
    VK_CTRL_A       = '\x01';       VK_CTRL_B = '\x02';       VK_CTRL_C = '\x03';      VK_CTRL_D = '\x04'
    VK_CTRL_E       = '\x05';       VK_CTRL_F = '\x06';       VK_CTRL_G = '\x07';      VK_CTRL_H = '\x08'
    VK_CTRL_I       = '\t';         VK_CTRL_J = '\n';         VK_CTRL_K = '\x0b';      VK_CTRL_L = '\x0c'
    VK_CTRL_M       = '\r';         VK_CTRL_N = '\x0e';       VK_CTRL_O = '\x0f';      VK_CTRL_P = '\x10'
    VK_CTRL_Q       = '\x11';       VK_CTRL_R = '\x12';       VK_CTRL_S = '\x13';      VK_CTRL_T = '\x14'
    VK_CTRL_U       = '\x15';       VK_CTRL_V = '\x16';       VK_CTRL_W = '\x17';      VK_CTRL_X = '\x18'
    VK_CTRL_Y       = '\x19';       VK_CTRL_Z = '\x1a'

    # Function keys
    VK_F1   = getkey.keys.F1;   VK_F2 = getkey.keys.F2;     VK_F3 = getkey.keys.F3
    VK_F4   = getkey.keys.F4;   VK_F5 = getkey.keys.F5;     VK_F6 = getkey.keys.F6
    VK_F7   = getkey.keys.F1;   VK_F8 = getkey.keys.F8;     VK_F9 = getkey.keys.F9
    VK_F10  = getkey.keys.F10;  VK_F11 = getkey.keys.F11;   VK_F12 = getkey.keys.F12

    # Letters
    VK_a = 'a'; VK_i = 'i'; VK_q = 'q'; VK_y = 'y'
    VK_A = 'A'; VK_I = 'I'; VK_Q = 'Q'; VK_Y = 'Y'
    VK_b = 'b'; VK_j = 'j'; VK_r = 'r'; VK_z = 'z'
    VK_B = 'B'; VK_J = 'J'; VK_R = 'R'; VK_Z = 'Z'
    VK_c = 'c'; VK_k = 'k'; VK_s = 's'
    VK_C = 'C'; VK_K = 'K'; VK_S = 'S'
    VK_d = 'd'; VK_l = 'l'; VK_t = 't'
    VK_D = 'D'; VK_L = 'L'; VK_T = 'T'
    VK_e = 'e'; VK_m = 'm'; VK_u = 'u'
    VK_E = 'E'; VK_M = 'M'; VK_U = 'U'
    VK_f = 'f'; VK_n = 'n'; VK_v = 'v'
    VK_F = 'F'; VK_N = 'N'; VK_V = 'V'
    VK_g = 'g'; VK_o = 'o'; VK_w = 'w'
    VK_G = 'G'; VK_O = 'O'; VK_W = 'W'
    VK_h = 'h'; VK_p = 'p'; VK_x = 'x'
    VK_H = 'H'; VK_P = 'P'; VK_X = 'X'

    # Numbers
    VK_ZERO          = '0'; VK_FIVE  = '5'
    VK_ONE           = '1'; VK_SIX   = '6'
    VK_TWO           = '2'; VK_SEVEN = '7'
    VK_THREE         = '3'; VK_EIGHT = '8'
    VK_FOUR          = '4'; VK_NINE  = '9'

    # Punctuation
    VK_BACKTICK      = '`'; VK_OPEN_PARENTHESIS  = '('; VK_PIPE              = '|'
    VK_TILDE         = '~'; VK_CLOSE_PARENTHESIS = ')'; VK_BACK_SLASH        = '\\'
    VK_EXCL_MARK     = '!'; VK_MINUS             = '-'; VK_BACK_COLON        = ':'
    VK_AT            = '@'; VK_UNDERSCORE        = '_'; VK_BACK_SEMI_COLON   = ';'
    VK_SHARP         = '#'; VK_PLUS              = '+'; VK_QUOTE             = '\''
    VK_DOLLAR        = '$'; VK_EQUALS            = '='; VK_DOUBLE_QUOTE      = '"'
    VK_PERCENTAGE    = '%'; VK_LEFT_BRACKET      = '['; VK_LOWER             = '<'
    VK_CIRCUMFLEX    = '^'; VK_RIGHT_BRACKET     = ']'; VK_GREATER           = '>'
    VK_AMPERSAND     = '&'; VK_LEFT_BRACE        = '{'; VK_COMMA             = ','
    VK_ASTERISK      = '*'; VK_RIGHT_BRACE       = '}'; VK_PERIOD            = '.'
    VK_SLASH         = '/'; VK_QUESTION_MARK     = '?'; VK_CUSTOM            = None

    # fmt: on

    @staticmethod
    def kbhit(wait: bool = False, timeout: float = 0) -> bool:
        """Return whether there was an ENTER keyboard press."""
        while dr_list := select.select([sys.stdin], [], [], timeout):
            if not wait:
                return dr_list[0] != []
            elif dr_list[0]:
                return True

    @classmethod
    def wait_keystroke(cls, blocking: bool = True, ignore_error_keys: bool = False) -> Optional["Keyboard"]:
        """Wait until a keypress is detected."""
        keystroke = None
        try:
            keystroke = getkey.getkey(blocking)
            return cls.of_value(keystroke)
        except AssertionError as err:
            if not ignore_error_keys:
                raise KeyboardInputError(f"Invalid keystroke '{keystroke}'") from err
        except TypeError:
            return Keyboard.custom(keystroke)
        except termios.error as err:
            raise KeyboardInputError("keyboard:: Requires a terminal (TTY)") from err
        finally:
            sys.stdin.flush()

        return None

    @classmethod
    def getch(cls, n: int = 1) -> List["Keyboard"]:
        """Read and return (a) character(s) from a keyboard press.
        Method will return after ENTER is pressed.
        """
        return list(map(cls.of_value, sys.stdin.read(n)))

    @classmethod
    def digits(cls) -> List["Keyboard"]:
        """Return all Keyboard digits."""
        return list(map(cls.of_value, filter(lambda v: str(v).isdigit(), cls.values())))

    @classmethod
    def letters(cls) -> List["Keyboard"]:
        """Return all Keyboard letters."""
        return list(map(cls.of_value, filter(lambda v: str(v).isalpha(), cls.values())))

    @classmethod
    def line_separators(cls) -> List["Keyboard"]:
        """Return all line feed separators."""
        return [cls.VK_ENTER, cls.VK_CRLF, cls.VK_CRLF, cls.VK_CR]

    @classmethod
    def break_keys(cls) -> List["Keyboard"]:
        """Return all line feed separators."""
        return [cls.VK_ESC, cls.VK_ENTER, cls.VK_CRLF, cls.VK_CRLF, cls.VK_CR]

    @classmethod
    def custom(cls, value):
        member = Keyboard.VK_CUSTOM
        member._value_ = value
        return member

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return str(self)

    @property
    def val(self) -> str:
        return str(self.value)

    def isdigit(self) -> bool:
        """Return True if the keystroke is a digit string, False otherwise."""
        return str(self.value).isdigit()

    def isalpha(self) -> bool:
        """Return True if the keystroke is alphabetic string, False otherwise."""
        return str(self.value).isalpha()

    def isalnum(self) -> bool:
        """Return True if the keystroke is alpha-numeric string, False otherwise."""
        return str(self.value).isalnum()

    def ispunct(self) -> bool:
        """Return True if the keystroke is a punctuation string, False otherwise."""
        return all(ch in string.punctuation for ch in str(self.value))

    def isEnter(self) -> bool:
        return self in [self.VK_ENTER, self.VK_CRLF, self.VK_CR, self.VK_LF]
