#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: main.tools
      @file: keyboard.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

import select
import string
import sys
from typing import Optional

import getkey

from hspylib.core.enums.enumeration import Enumeration
from hspylib.core.exception.exceptions import KeyboardInputError
from hspylib.modules.cli.vt100.vt_utils import require_terminal

require_terminal()


class Keyboard(Enumeration):
    """TODO"""

    # Control keys
    VK_NONE = ''
    VK_ESC = getkey.keys.ESC
    VK_UP = getkey.keys.UP
    VK_DOWN = getkey.keys.DOWN
    VK_LEFT = getkey.keys.LEFT
    VK_RIGHT = getkey.keys.RIGHT
    VK_BACKSPACE = getkey.keys.BACKSPACE
    VK_INSERT = getkey.keys.INSERT
    VK_DELETE = getkey.keys.DELETE
    VK_ENTER = getkey.keys.ENTER
    VK_TAB = '\t'
    VK_SPACE = getkey.keys.SPACE
    VK_HOME = getkey.keys.HOME
    VK_END = getkey.keys.END
    VK_PAGE_UP = getkey.keys.PAGE_UP
    VK_PAGE_DOWN = getkey.keys.PAGE_DOWN
    VK_SHIFT_TAB = '\x1b[Z'
    # Letters
    VK_a = 'a'
    VK_A = 'A'
    VK_b = 'b'
    VK_B = 'B'
    VK_c = 'c'
    VK_C = 'C'
    VK_d = 'd'
    VK_D = 'D'
    VK_e = 'e'
    VK_E = 'E'
    VK_f = 'f'
    VK_F = 'F'
    VK_g = 'g'
    VK_G = 'G'
    VK_h = 'h'
    VK_H = 'H'
    VK_i = 'i'
    VK_I = 'I'
    VK_j = 'j'
    VK_J = 'J'
    VK_k = 'k'
    VK_K = 'K'
    VK_l = 'l'
    VK_L = 'L'
    VK_m = 'm'
    VK_M = 'M'
    VK_n = 'n'
    VK_N = 'N'
    VK_o = 'o'
    VK_O = 'O'
    VK_p = 'p'
    VK_P = 'P'
    VK_q = 'q'
    VK_Q = 'Q'
    VK_r = 'r'
    VK_R = 'R'
    VK_s = 's'
    VK_S = 'S'
    VK_t = 't'
    VK_T = 'T'
    VK_u = 'u'
    VK_U = 'U'
    VK_v = 'v'
    VK_V = 'V'
    VK_w = 'w'
    VK_W = 'W'
    VK_x = 'x'
    VK_X = 'X'
    VK_y = 'y'
    VK_Y = 'Y'
    VK_z = 'z'
    VK_Z = 'Z'
    # Numbers
    VK_ZERO = '0'
    VK_ONE = '1'
    VK_TWO = '2'
    VK_THREE = '3'
    VK_FOUR = '4'
    VK_FIVE = '5'
    VK_SIX = '6'
    VK_SEVEN = '7'
    VK_EIGHT = '8'
    VK_NINE = '9'
    # Punctuation
    VK_BACKTICK = '`'
    VK_TILDE = '~'
    VK_EXCLAMATION_MARK = '!'
    VK_AT = '@'
    VK_SHARP = '#'
    VK_DOLLAR = '$'
    VK_PERCENTAGE = '%'
    VK_CIRCUMFLEX = '^'
    VK_AMPERSAND = '&'
    VK_ASTERISK = '*'
    VK_OPEN_PARENTHESIS = '('
    VK_CLOSE_PARENTHESIS = ')'
    VK_MINUS = '-'
    VK_UNDERSCORE = '_'
    VK_PLUS = '+'
    VK_EQUALS = '='
    VK_LEFT_BRACKET = '['
    VK_RIGHT_BRACKET = ']'
    VK_LEFT_BRACE = '{'
    VK_RIGHT_BRACE = '}'
    VK_PIPE = '|'
    VK_BACK_SLASH = '\\'
    VK_BACK_COLON = ':'
    VK_BACK_SEMI_COLON = ';'
    VK_QUOTE = '\''
    VK_DOUBLE_QUOTE = '"'
    VK_LOWER = '<'
    VK_GREATER = '>'
    VK_COMMA = ','
    VK_PERIOD = '.'
    VK_SLASH = '/'
    VK_QUESTION_MARK = '?'

    @staticmethod
    def kbhit() -> bool:
        """TODO"""
        dr, _, _ = select.select([sys.stdin], [], [], 0)
        return dr != []

    @staticmethod
    def getch() -> str:
        """TODO"""
        return sys.stdin.read(1)

    @classmethod
    def read_keystroke(cls, blocking: bool = True, ignore_error_keys: bool = True) -> Optional['Keyboard']:
        """TODO"""
        try:
            keystroke = getkey.getkey(blocking)
            if keystroke:
                return cls.of_value(keystroke)
        except (KeyboardInterrupt, AssertionError) as err:
            if not ignore_error_keys:
                raise KeyboardInputError(f"Invalid keystroke => {str(err)}") from err
        finally:
            sys.stdin.flush()

        return None

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return str(self)

    def isdigit(self) -> bool:
        """TODO"""
        return str(self.value).isdigit()

    def isalpha(self) -> bool:
        """TODO"""
        return str(self.value).isalpha()

    def isalnum(self) -> bool:
        """TODO"""
        return str(self.value).isalnum()

    def ispunct(self) -> bool:
        """TODO"""
        return all(ch in string.punctuation for ch in str(self.value))
