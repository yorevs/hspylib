#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.main.hspylib.core.tools
      @file: keyboard.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

import string
import sys
from typing import Any, Optional

import getkey

from hspylib.core.enum.enumeration import Enumeration
from hspylib.core.tools.commons import syserr

assert sys.stdin.isatty(), 'This module requires a terminal (TTY)'


class Keyboard(Enumeration):
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
    # @formatter:off
    VK_a = 'a'; VK_A = 'A'
    VK_b = 'b'; VK_B = 'B'
    VK_c = 'c'; VK_C = 'C'
    VK_d = 'd'; VK_D = 'D'
    VK_e = 'e'; VK_E = 'E'
    VK_f = 'f'; VK_F = 'F'
    VK_g = 'g'; VK_G = 'G'
    VK_h = 'h'; VK_H = 'H'
    VK_i = 'i'; VK_I = 'I'
    VK_j = 'j'; VK_J = 'J'
    VK_k = 'k'; VK_K = 'K'
    VK_l = 'l'; VK_L = 'L'
    VK_m = 'm'; VK_M = 'M'
    VK_n = 'n'; VK_N = 'N'
    VK_o = 'o'; VK_O = 'O'
    VK_p = 'p'; VK_P = 'P'
    VK_q = 'q'; VK_Q = 'Q'
    VK_r = 'r'; VK_R = 'R'
    VK_s = 's'; VK_S = 'S'
    VK_t = 't'; VK_T = 'T'
    VK_u = 'u'; VK_U = 'U'
    VK_v = 'v'; VK_V = 'V'
    VK_w = 'w'; VK_W = 'W'
    VK_x = 'x'; VK_X = 'X'
    VK_y = 'y'; VK_Y = 'Y'
    VK_z = 'z'; VK_Z = 'Z'
    # @formatter:on
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

    @classmethod
    def read_keystroke(cls) -> Optional[Any]:
        try:
            keystroke = getkey.getkey()
            if keystroke:
                return cls.of_value(keystroke)
            else:
                return None
        except KeyboardInterrupt as err:
            syserr(str(err))
        except AssertionError:
            pass

        return None

    def isdigit(self) -> bool:
        return str(self.value).isdigit()

    def isalpha(self) -> bool:
        return str(self.value).isalpha()

    def isalnum(self) -> bool:
        return str(self.value).isalnum()

    def ispunct(self) -> bool:
        return all(ch in string.punctuation for ch in str(self.value))
