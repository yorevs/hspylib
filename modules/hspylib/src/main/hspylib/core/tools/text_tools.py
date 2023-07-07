#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib
   @package: hspylib.core.tools
      @file: text_tools.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""
from hspylib.core.tools.dict_tools import get_or_default
from typing import Any, List, Optional, Tuple

import os
import random
import re
import string


def elide_text(text: str, width: int, elide_with: str = "...") -> str:
    """Return a copy of the string eliding the text case the string is bigger than the specified length.
    :param text: TODO
    :param width: TODO
    :param elide_with: TODO
    """
    return text if len(text) <= width else text[: width - len(elide_with)] + elide_with


def cut(text: str, field: int, separator: str = " ") -> Tuple[Optional[str], tuple]:
    """Return a new string cut out from the given text.
    :param text: TODO
    :param field: TODO
    :param separator: TODO
    """
    result = tuple(re.split(rf"{separator}+", text))
    return get_or_default(result, field), result[:field]


def random_string(choices: List[str], length: int, weights: List[int] = None) -> str:
    """Return a new random string matching choices and length.
    :param choices: TODO
    :param length: TODO
    :param weights: TODO
    """
    return "".join(random.choices(choices, weights or [1] * len(choices), k=length))


def justified_left(text: str, width: int, fill: str = " ") -> str:
    """Return a copy of the string justified left.
    :param text: TODO
    :param width: TODO
    :param fill: TODO
    """
    return text.ljust(width, fill)


def justified_center(text: str, width: int, fill: str = " ") -> str:
    """Return a copy of the string justified center.
    :param text: TODO
    :param width: TODO
    :param fill: TODO
    """
    return text.center(width, fill)


def justified_right(text: str, width: int, fill: str = " ") -> str:
    """Return a copy of the string justified right.
    :param text: TODO
    :param width: TODO
    :param fill: TODO
    """
    return text.rjust(width, fill)


def uppercase(text: str) -> str:
    """Return a copy of the string converted to upper case.
    :param text: TODO
    """
    return text.upper()


def lowercase(text: str) -> str:
    """Return a copy of the string converted to lower case.
    :param text: TODO
    """
    return text.lower()


def camelcase(text: str, separator: str = " |-|_", upper: bool = False) -> str:
    """Return a copy of the string converted to camel case.
    Ref:https://en.wikipedia.org/wiki/Letter_case :: Camel case
    :param text: TODO
    :param separator: TODO
    :param upper: TODO
    """
    s = re.sub(rf"({separator})+", " ", text)
    s = s.title()
    s = re.sub(rf"({separator})+", "", s)
    fnc = getattr(s[0], "lower" if not upper else "upper")
    return "".join([fnc(), s[1:]])


def snakecase(text: str, separator: str = "-", screaming: bool = False) -> str:
    """Return a copy of the string converted to snake case.
    Ref:https://en.wikipedia.org/wiki/Letter_case :: Snake case
    :param text: TODO
    :param separator: TODO
    :param screaming: TODO
    """
    s = re.sub("([A-Z][a-z]+)", r" \1", re.sub("([A-Z]+)", r" \1", text.replace(separator, " ")))
    text = "_".join(s.split())
    fnc = getattr(text, "lower" if not screaming else "upper")
    return fnc()


def kebabcase(text: str, separator: str = " |-|_", train: bool = False) -> str:
    """Return a copy of the string converted to kebab case.
    Ref:https://en.wikipedia.org/wiki/Letter_case :: Kebab case
    :param text: TODO
    :param separator: TODO
    :param train: TODO
    """
    s = re.sub("([A-Z][a-z]+)", r" \1", re.sub("([A-Z]+)", r" \1", text.replace(separator, " ")))
    text = "-".join(s.split())
    fnc = getattr(text, "lower" if not train else "upper")
    return fnc()


def titlecase(text: str, separator: str = " |-|_", skip_length: int = 0) -> str:
    """Return a copy of the string converted to title case.
    Ref:https://en.wikipedia.org/wiki/Letter_case :: Title case
    :param text: TODO
    :param separator: TODO
    :param skip_length: TODO
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
    :param text: TODO
    """
    ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
    return ansi_escape.sub("", text)


def strip_linebreaks(text: str, re_exp: str = r"(\n|\r|\n\r)+") -> str:
    """Return a copy of the string stripping out all line breaks from it.
    :param text: TODO
    :param re_exp: TODO
    """
    return re.sub(re.compile(rf"{re_exp}"), "", text)


def strip_extra_spaces(text: str, re_exp: str = r"\s+", trim: bool = False) -> str:
    """Return a copy of the string stripping out all components spaces 2+ from it.
    :param text: TODO
    :param re_exp: TODO
    :param trim: TODO
    """
    s = re.sub(re.compile(rf"{re_exp}"), " ", text)
    return s if not trim else s.strip()


def split_and_filter(text: str, regex_filter: str = ".*", delimiter: str = os.linesep) -> List[str]:
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
    :param json_text: TODO
    """
    return strip_extra_spaces(strip_linebreaks(json_text)).replace('"', '\\"')


def eol(current_index: int, split_len: int, line_sep: str = os.linesep, word_sep: str = " ") -> str:
    """Give the line separator character (hit) or an empty string (miss) according to the splitting length and
    current index.
    :param current_index: TODO
    :param split_len: TODO
    :param line_sep: TODO
    :param word_sep: TODO
    """
    return line_sep if (current_index + 1) % split_len == 0 else word_sep


def ensure_endswith(text: str, end_str: str) -> str:
    """Ensure the string ends with the given end string.
    :param text: TODO
    :param end_str: TODO
    """
    return text if text.endswith(end_str) else text + end_str


def ensure_startswith(text: str, start_str: str) -> str:
    """Ensure the string starts with the given start string.
    :param text: TODO
    :param start_str: TODO
    """
    return text if text.startswith(start_str) else start_str + text


def quote(value: Any) -> str:
    """Quote or double quote the value according to the value type.
    :param value: TODO
    """
    return (
        str(value)
        if not isinstance(value, str)
        else f'"{value}"'
        if value.startswith("'") and value.endswith("'")
        else f"'{value}'"
    )


def last_index_of(text: str, substring: str) -> int:
    """Return the last index of substring or -1 if substring was not found in text.
    :param text: TODO
    :param substring: TODO
    """
    try:
        return text.rindex(substring)
    except ValueError:
        pass
    return -1


def xstr(obj: Any) -> str:
    """TODO"""
    if obj is None:
        return ""
    return str(obj)
