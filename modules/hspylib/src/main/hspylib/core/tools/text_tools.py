#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib
   @package: hspylib.core.tools
      @file: text_tools.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright·(c)·2024,·HSPyLib
"""
import hashlib

from hspylib.core.enums.charset import Charset
from hspylib.core.tools.dict_tools import get_or_default
from typing import Any, List, Optional, Tuple

import os
import random
import re
import string


def elide_text(text: str, width: int, elide_with: str = "...") -> str:
    """Return a copy of the string eliding the text case the string is bigger than the specified length.
    :param text: The text to be elided,
    :param width: The text maximum width before eliding.
    :param elide_with: A 3 chars string used to indicate text continuity, usually an 'ellipsis'.
    """
    elide_with = elide_with[:3]
    return text if len(text) <= width else text[: width - len(elide_with)] + elide_with


def cut(text: str, field: int, separator: str = " ") -> Tuple[Optional[str], tuple]:
    """Return a new string cut out from the given text.
    :param text: The provided text.
    :param field: The field to be cut, specified by a sequential number.
    :param separator: Th Field delimiter character used to cut the string.
    """
    result = tuple(re.split(rf"{separator}+", text))
    return get_or_default(result, field), result[:field]


def random_string(choices: List[str], length: int, weights: List[int] = None) -> str:
    """Return a new random string matching choices and length.
    :param choices: The available choices.
    :param length: The required length of the string.
    :param weights: The relative weights or cumulative weights.
    """
    return "".join(random.choices(choices, weights or [1] * len(choices), k=length))


def justified_left(text: str, width: int, fill: str = " ") -> str:
    """Return a copy of the text justified left.
    :param text: The provided text.
    :param width: The justification width.
    :param fill: The character used to fill in the gaps.
    """
    return text.ljust(width, fill)


def justified_center(text: str, width: int, fill: str = " ") -> str:
    """Return a copy of the text justified center.
    :param text: The provided text.
    :param width: The justification width.
    :param fill: The character used to fill in the gaps.
    """
    return text.center(width, fill)


def justified_right(text: str, width: int, fill: str = " ") -> str:
    """Return a copy of the text justified right.
    :param text: The provided text.
    :param width: The justification width.
    :param fill: The character used to fill in the gaps.
    """
    return text.rjust(width, fill)


def uppercase(text: str) -> str:
    """Return a copy of the text converted to upper case.
    :param text: The text to be converted.
    """
    return text.upper()


def lowercase(text: str) -> str:
    """Return a copy of the text converted to lower case.
    :param text: The text to be converted.
    """
    return text.lower()


def camelcase(text: str, separator: str = " |-|_", capitalized: bool = False) -> str:
    """Return a copy of the text converted to camel case.
    Ref:https://en.wikipedia.org/wiki/Letter_case :: Camel case
    :param text: The text to be converted.
    :param separator: The word separator character.
    :param capitalized: Whether to capitalize the words or not.
    """
    s = re.sub(rf"({separator})+", " ", text)
    s = s.title()
    text = re.sub(rf"({separator})+", "", s)
    fnc = getattr(text[0], "lower" if not capitalized else "upper")
    return "".join([fnc(), text[1:]])


def snakecase(text: str, separator: str = " |-|_", screaming: bool = False) -> str:
    """Return a copy of the string converted to snake case.
    Ref:https://en.wikipedia.org/wiki/Letter_case :: Snake case
    :param text: The text to be converted.
    :param separator: The word separator character.
    :param screaming: Whether to upper case the words or not.
    """
    s = re.sub("([A-Z][a-z]+)", r" \1", re.sub("([A-Z]+)", r" \1", re.sub(separator, " ", text)))
    text = "_".join(s.split())
    fnc = getattr(text, "lower" if not screaming else "upper")
    return fnc()


def kebabcase(text: str, separator: str = " |-|_", train: bool = False) -> str:
    """Return a copy of the string converted to kebab case.
    Ref:https://en.wikipedia.org/wiki/Letter_case :: Kebab case
    :param text: The text to be converted.
    :param separator: The word separator character.
    :param train: Whether to upper case the words or not.
    """
    s = re.sub("([A-Z][a-z]+)", r" \1", re.sub("([A-Z]+)", r" \1", re.sub(separator, " ", text)))
    text = "-".join(s.split())
    fnc = getattr(text, "lower" if not train else "upper")
    return fnc()


def titlecase(text: str, separator: str = " |-|_", skip_length: int = 0) -> str:
    """Return a copy of the string converted to title case.
    Ref:https://en.wikipedia.org/wiki/Letter_case :: Title case
    :param text: The text to be converted.
    :param separator: The word separator character.
    :param skip_length: Whether to skip words with lesser lengths than this.
    """
    s = re.sub(rf"({separator})+", " ", text)
    s = " ".join([string.capwords(word) if len(word) > skip_length else word.lower() for word in s.split(" ")])
    return s


def environ_name(property_name: str) -> str:
    """Retrieve the environment name of the specified property name.
    :param property_name: the name of the property using space, dot or dash notations.
    """
    return re.sub("[ -.]", "_", property_name).upper()


def strip_escapes(text: str) -> str:
    """Return a copy of the string stripping out all ansi escape 'ESC[' codes from it.
    Ref:https://stackoverflow.com/questions/14693701/how-can-i-remove-the-ansi-escape-sequences-from-a-string-in-python
    :param text: The text to be stripped.
    """
    ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
    return ansi_escape.sub("", text)


def strip_linebreaks(text: str, re_exp: str = r"(\n|\r|\n\r)+") -> str:
    """Return a copy of the string stripping out all line breaks from it.
    :param text: The text to be stripped.
    :param re_exp: The regex expression used to strip the line breaks.
    """
    return re.sub(re.compile(rf"{re_exp}"), "", text)


def strip_extra_spaces(text: str, re_exp: str = r"\s+", trim: bool = False) -> str:
    """Return a copy of the string stripping out all components spaces 2+ from it.
    :param text: The text to be stripped.
    :param re_exp: The regex expression used to strip the spaces.
    :param trim: Whether to also, trim the string after stripping.
    """
    s = re.sub(re.compile(rf"{re_exp}"), " ", text)
    return s if not trim else s.strip()


def split_filter(text: str, regex_filter: str = ".*", delimiter: str = os.linesep) -> List[str]:
    """Split the string using the delimiter and filter using the specified regex filter
    :param text: The string to be split
    :param regex_filter: The regex to filter the string
    :param delimiter: The delimiter according which to split the string
    :return:
    """
    return list(filter(re.compile(regex_filter).search, text.split(delimiter)))


def json_stringify(json_text: str) -> str:
    """Return a copy of the json text stripping any line breaks or formatting from it and also quoting any existing
    double quotes.
    :param json_text: The text to be converted.
    """
    return strip_extra_spaces(strip_linebreaks(json_text)).replace('"', '\\"')


def eol(current_index: int, split_len: int, line_sep: str = os.linesep, word_sep: str = " ") -> str:
    """Given the line separator character (hit) or an empty string (miss) according to the splitting length and
    current index.
    :param current_index: TODO
    :param split_len: TODO
    :param line_sep: TODO
    :param word_sep: TODO
    """
    return line_sep if (current_index + 1) % split_len == 0 else word_sep


def ensure_endswith(text: str, end_str: str) -> str:
    """Ensure the text ends with the given 'end' string.
    :param text: The provided text.
    :param end_str: The string to be ensured at the end.
    """
    return text if text.endswith(end_str) else text + end_str


def ensure_startswith(text: str, start_str: str) -> str:
    """Ensure the text starts with the given 'start' string.
    :param text: The provided text.
    :param start_str: The string to be ensured at the beginning.
    """
    return text if text.startswith(start_str) else start_str + text


def quote(value: Any) -> str:
    """Quote or double quote the value according to the value type.
    :param value: The value to be quoted.
    """
    return (
        str(value)
        if not isinstance(value, str)
        else f'"{value}"' if value.startswith("'") and value.endswith("'") else f"'{value}'"
    )


def last_index_of(text: str, substring: str) -> int:
    """Return the last index of substring or -1 if substring was not found in text.
    :param text: The provided text.
    :param substring: The substring to find.
    """
    try:
        return text.rindex(substring)
    except ValueError:
        pass
    return -1


def xstr(obj: Any) -> str:
    """Return a string representation of the object. Returns an empty string if the object is None."""
    return str(obj) if obj is not None else ""


def hash_text(text: str) -> str:
    """Create a hash string based on the provided text.
    :param: text the text to be hashed.
    """
    return hashlib.md5(text.encode(Charset.UTF_8.val)).hexdigest()
