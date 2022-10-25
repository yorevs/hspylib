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

   Copyright 2022, HSPyLib team
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
    """Provides keyboard interaction with the terminal."""

    # @formatter:off

    # Control keys
    VK_NONE         = ''

    VK_ESC          = getkey.keys.ESC; VK_ENTER         = getkey.keys.ENTER
    VK_UP           = getkey.keys.UP; VK_TAB            = '\t'
    VK_DOWN         = getkey.keys.DOWN; VK_SPACE        = getkey.keys.SPACE
    VK_LEFT         = getkey.keys.LEFT; VK_HOME         = getkey.keys.HOME
    VK_RIGHT        = getkey.keys.RIGHT; VK_END         = getkey.keys.END
    VK_BACKSPACE    = getkey.keys.BACKSPACE; VK_PAGE_UP = getkey.keys.PAGE_UP
    VK_INSERT       = getkey.keys.INSERT; VK_PAGE_DOWN  = getkey.keys.PAGE_DOWN
    VK_DELETE       = getkey.keys.DELETE; VK_SHIFT_TAB  = '\x1b[Z'

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
    VK_ZERO     = '0'; VK_FIVE  = '5'
    VK_ONE      = '1'; VK_SIX   = '6'
    VK_TWO      = '2'; VK_SEVEN = '7'
    VK_THREE    = '3'; VK_EIGHT = '8'
    VK_FOUR     = '4'; VK_NINE  = '9'

    # Punctuation
    VK_BACKTICK     = '`'; VK_OPEN_PARENTHESIS  = '('; VK_PIPE              = '|'
    VK_TILDE        = '~'; VK_CLOSE_PARENTHESIS = ')'; VK_BACK_SLASH        = '\\'
    VK_EXCL_MARK    = '!'; VK_MINUS             = '-'; VK_BACK_COLON        = ':'
    VK_AT           = '@'; VK_UNDERSCORE        = '_'; VK_BACK_SEMI_COLON   = ';'
    VK_SHARP        = '#'; VK_PLUS              = '+'; VK_QUOTE             = '\''
    VK_DOLLAR       = '$'; VK_EQUALS            = '='; VK_DOUBLE_QUOTE      = '"'
    VK_PERCENTAGE   = '%'; VK_LEFT_BRACKET      = '['; VK_LOWER             = '<'
    VK_CIRCUMFLEX   = '^'; VK_RIGHT_BRACKET     = ']'; VK_GREATER           = '>'
    VK_AMPERSAND    = '&'; VK_LEFT_BRACE        = '{'; VK_COMMA             = ','
    VK_ASTERISK     = '*'; VK_RIGHT_BRACE       = '}'; VK_PERIOD            = '.'
    VK_SLASH        = '/'; VK_QUESTION_MARK     = '?'

    # @formatter:on

    @staticmethod
    def kbhit() -> bool:
        """Return when the is any keyboard press."""
        dr, _, _ = select.select([sys.stdin], [], [], 0)
        return dr != []

    @staticmethod
    def getch() -> 'Keyboard':
        """Read and return a character from a keyboard press."""
        return Keyboard.of_value(sys.stdin.read(1))

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

if __name__ == '__main__':
    print('Press', Keyboard.kbhit())
