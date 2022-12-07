#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: main.tools
      @file: commons.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
import inspect
import logging as log
import os
import pathlib
import sys
from datetime import timedelta
from typing import Optional, Set, Tuple, Type
from urllib.parse import urlparse

from hspylib.core.constants import TRUE_VALUES
from hspylib.core.enums.charset import Charset
from hspylib.core.tools.validator import Validator
from hspylib.modules.cli.vt100.vt_codes import VtCodes
from hspylib.modules.cli.vt100.vt_colors import VtColors

# pylint: disable=consider-using-f-string
FILE_LOG_FMT = '{}\t{} {} {} {} {} '.format(
    '%(asctime)s',
    '%(levelname)-5.5s',
    '%(filename)s::',
    '%(message)s',
    '%(funcName)s(@Line:%(lineno)d) -',
    '%(threadName)-12.12s',
)

CONSOLE_LOG_FMT = '{}\t{} {} {} {} '.format(
    '%(levelname)-5.5s',
    '%(message)s',
    '%(funcName)s(@Line:%(lineno)d)',
    '%(asctime)s -',
    '%(threadName)-12.12s'
)


def log_init(
    filename: Optional[str] = None,
    filemode: str = 'a',
    level: int = log.DEBUG,
    log_format: str = FILE_LOG_FMT,
    clear_handlers: bool = True,
    console_enable: bool = False,
    file_enable: bool = True) -> bool:
    """Initialize the system logger"""

    if file_enable and not os.path.exists(filename):
        touch_file(filename)

    # if someone tried to log something before log_init is called, Python creates a default handler that is going to
    # mess our logs. Remove handlers if there is any.
    root, handlers = log.getLogger(), set()

    if clear_handlers:
        if root.handlers:
            for handler in root.handlers:
                handler.close()
                root.removeHandler(handler)

    if file_enable:
        file_formatter = log.Formatter(log_format)
        file_handler = log.FileHandler(filename=filename, mode=filemode)
        file_handler.setFormatter(file_formatter)
        handlers.add(file_handler)

    if console_enable:
        console_formatter = log.Formatter(CONSOLE_LOG_FMT, "%Y-%m-%d %H:%M:%S")
        console_handler = log.StreamHandler(sys.stdout)
        console_handler.setFormatter(console_formatter)
        handlers.add(console_handler)

    log.basicConfig(level=level, handlers=handlers)

    return file_enable if os.path.exists(filename or '') else console_enable


def is_debugging() -> bool:
    """Whether the program is running under debug mode."""
    for frame in inspect.stack():
        if frame[1].endswith("pydevd.py"):
            return True
    return False


def dirname(filepath: str) -> str:
    """Retrieve the directory of the specified filepath"""
    return os.path.dirname(os.path.realpath(filepath))


def run_dir() -> str:
    """Retrieve the application's root directory"""
    return sys.path[0]


def get_path(filepath: str) -> pathlib.Path:
    """Retrieve the Path of the file"""
    return pathlib.Path(filepath).parent


def sysout(string: str, end: str = '\n') -> None:
    """Print the unicode input_string decoding vt100 placeholders
    :param string: values to be printed to sys.stdout
    :param end: string appended after the last value, default a newline
    """
    if Validator.is_not_blank(string):
        msg = VtColors.colorize(VtCodes.decode(f"{string}%NC%"))
        print(msg, file=sys.stdout, flush=True, end=end)


def syserr(string: str, end: str = '\n') -> None:
    """Print the unicode input_string decoding vt100 placeholders
    :param string: values to be printed to sys.stderr
    :param end: string appended after the last value, default a newline
    """
    if Validator.is_not_blank(string):
        msg = VtColors.colorize(VtCodes.decode(f"%RED%{string}%NC%"))
        print(msg, file=sys.stderr, flush=True, end=end)


def class_attribute_names(clazz: Type) -> Optional[Tuple]:
    """Retrieve all attribute names of the class
    :param clazz: The class to retrieve the attribute names
    """
    return tuple(vars(clazz()).keys()) if clazz else None


def class_attribute_values(instance: dict) -> Optional[Tuple]:
    """Retrieve all attribute values of the class
    :param instance: The class to retrieve the attribute values
    """
    return tuple(instance.values()) if instance else None


def str_to_bool(string: str, true_values: Set[str] = None) -> bool:
    """Convert a string to boolean
    :param string: The string to be converted
    :param true_values: The list of strings that will become True value
    """
    return string is not None and string.lower() in (true_values or TRUE_VALUES)


def safe_delete_file(filename: str, on_not_found_except: bool = False) -> bool:
    """Delete the file specified by filename. If the file is not found, raises an exception if on_not_found_except is
    True; otherwise return False.
    :param filename: the name of the file to be checked
    :param on_not_found_except: boolean parameter to raise an exception if the file is not found.
    """
    if os.path.exists(filename):
        os.remove(filename)
    else:
        if on_not_found_except:
            raise FileNotFoundError(f'File was not found on the system: {filename}')
        return False

    return True


def file_is_not_empty(filename: str) -> bool:
    """Check whether the file is empty or not.
    :param filename: the name of the file to be modified. If the file does not exist; return False
    """
    return os.path.exists(filename) and os.stat(filename).st_size > 0


def touch_file(filename: str, encoding: str = Charset.UTF_8.val) -> None:
    """Change file modification time
    :param filename: the name of the file to be modified
    :param encoding: the file encoding
    """
    with open(filename, 'a', encoding=encoding):
        os.utime(filename, None)


def human_readable_bytes(size_in_bytes: int) -> Tuple[str, str]:
    """Return a Human readable bytes and unit
    :param size_in_bytes: the size to be formatted
    """

    byte_size = float(size_in_bytes)
    kb, mb, gb, tb = 2 ** 10, 2 ** 20, 2 ** 30, 2 ** 40

    if 0 <= byte_size <= kb:
        ret_val = f'{byte_size:3.2f}'
        ret_unit = '[B]'
    elif kb < byte_size <= mb:
        ret_val = f'{byte_size / kb:3.2f}'
        ret_unit = '[Kb]'
    elif mb < byte_size <= gb:
        ret_val = f'{byte_size / mb:3.2f}'
        ret_unit = '[Mb]'
    elif gb < byte_size <= tb:
        ret_val = f'{byte_size / gb:3.2f}'
        ret_unit = '[Gb]'
    else:
        ret_val = f'{byte_size / tb:3.2f}'
        ret_unit = '[Tb]'

    return ret_val, ret_unit


def human_readable_time(time_microseconds: int) -> str:
    """Return a Human readable formatted time
    :param time_microseconds: the time to be formatted
    """
    delta = timedelta(microseconds=time_microseconds)
    total_seconds = delta.seconds
    seconds = total_seconds % 60
    minutes = total_seconds / 60 % 60
    hours = total_seconds / 3600
    microseconds = delta.microseconds
    # Using format: HH:MM:SS.uuuuuu
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{microseconds:06d}"


def build_url(base_url: str, scheme: str = 'http') -> str:
    """TODO"""
    p_url = urlparse(base_url)
    if not p_url.scheme:
        base_url = p_url._replace(scheme=scheme).geturl()

    return base_url
