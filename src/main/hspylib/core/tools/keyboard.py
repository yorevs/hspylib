import getkey
from typing import Any
from hspylib.core.enum.enumeration import Enumeration


class Keyboard(Enumeration):
    # Control keys
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
    # Letters
    VK_A = 'a'
    VK_B = 'b'
    VK_C = 'c'
    VK_D = 'd'
    VK_E = 'e'
    VK_F = 'f'
    VK_G = 'g'
    VK_H = 'h'
    VK_I = 'i'
    VK_J = 'j'
    VK_K = 'k'
    VK_L = 'l'
    VK_M = 'm'
    VK_N = 'n'
    VK_O = 'o'
    VK_P = 'p'
    VK_Q = 'q'
    VK_R = 'r'
    VK_S = 's'
    VK_T = 't'
    VK_U = 'u'
    VK_V = 'v'
    VK_W = 'w'
    VK_X = 'x'
    VK_Y = 'y'
    VK_Z = 'z'
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
    def read_keystroke(cls) -> Any:
        try:
            keystroke = getkey.getkey()
            if keystroke:
                return cls.of_value(keystroke, ignore_case=True)
            else:
                return cls.ESC
        except KeyboardInterrupt:
            return cls.ESC

    def isdigit(self):
        return self.value.isdigit()
