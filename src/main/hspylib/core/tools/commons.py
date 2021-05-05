#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.main.hspylib.core.tools
      @file: commons.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

import logging as log
import os
import pathlib
import re
import sys
from typing import Any, List, Optional, Tuple, Type

from hspylib.core.tools.validator import Validator
from hspylib.modules.cli.vt100.vt_codes import VtCodes
from hspylib.modules.cli.vt100.vt_colors import VtColors

LOG_FMT = '{} {} {} {}{} {} '.format(
    '%(asctime)s',
    '[%(threadName)-10.10s]',
    '%(levelname)-5.5s',
    '%(filename)s::',
    '%(funcName)s(@Line:%(lineno)d)',
    '%(message)s'
)


def log_init(
        log_file: str,
        create_new: bool = True,
        f_mode: str = 'a',
        level: int = log.DEBUG,
        log_fmt: str = LOG_FMT) -> log:
    """Initialize the system logger
    :param log_file: TODO
    :param create_new:  TODO
    :param f_mode:  TODO
    :param level:  TODO
    :param log_fmt:  TODO
    """
    with open(log_file, 'w' if create_new else 'a'):
        os.utime(log_file, None)
    
    log.basicConfig(
        filename=log_file,
        format=log_fmt,
        level=level,
        filemode=f_mode)
    
    return log


def read_version(version_filepath: str = ".version") -> Tuple:
    """Retrieve the version from the version file in the form: Tuple[major,minor,build]"""
    try:
        log.info(f"Reading version from {version_filepath}")
        with open(version_filepath) as fh_version:
            ver = tuple(map(str.strip, fh_version.read().split('.')))
            return ver if ver else (0, 0, 0)
    except FileNotFoundError:
        return 0, 0, 0


def dirname(filepath: str) -> str:
    """Retrieve the directory of the specified filepath"""
    return os.path.dirname(os.path.realpath(filepath))


def run_dir() -> str:
    """Retrieve the application's root directory"""
    return sys.path[0]


def get_path(filepath: str) -> pathlib.Path:
    return pathlib.Path(filepath).parent


def environ_name(property_name: str) -> str:
    """Retrieve the environment name of the specified property name
    :param property_name: the name of the property using space, dot or dash notations
    """
    return re.sub('[ -.]', '_', property_name).upper()


def sysout(string: str, end: str = '\n') -> None:
    """Print the unicode input_string decoding vt100 placeholders
    :param string: values to be printed to sys.stdout
    :param end: string appended after the last value, default a newline
    """
    if Validator.is_not_blank(string):
        msg = VtColors.colorize(VtCodes.decode(f"{string}"))
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
    """TODO
    :param clazz: TODO
    """
    return tuple(vars(clazz()).keys()) if clazz else None


def class_attribute_values(instance: dict) -> Optional[Tuple]:
    """TODO
    :param instance: TODO
    """
    return tuple(instance.values()) if instance else None


def split_and_filter(input_str: str, regex_filter: str = '.*', delimiter: str = '\n') -> List[str]:
    """Split the string using the delimiter and filter using the specified regex filter
    :param input_str: The string to be split
    :param regex_filter: The regex to filter the string
    :param delimiter: The delimiter according which to split the string
    """
    regex = re.compile(regex_filter)
    result_list = list(filter(regex.search, input_str.split(delimiter)))
    
    return result_list


def get_or_default(options: tuple, index: int, default_value=None) -> Optional[Any]:
    """Retrieve an item from the options list or None if index is out of range
    :param options: The available list of options
    :param index: The index of the item
    :param default_value: The default value if the index is out of range
    """
    return options[index] if index < len(options) else default_value


def get_by_key_or_default(options: dict, key: str, default_value=None) -> Optional[Any]:
    """Retrieve an item from the options list or None if key was not found
    :param options: The available list of options
    :param key: The key of the item
    :param default_value: The default value if the index is not found
    """
    return options[key] if key in options else default_value


def str_to_bool(string: str, true_values: List[str] = None) -> bool:
    """Convert a string to boolean
    :param string: The string to be converted
    :param true_values: The list of strings that will become True value
    """
    if true_values is None:
        true_values = [
            'true', 'on', 'yes', '1', 'y'
        ]
    return string.lower() in true_values if string else False


def safe_del_file(filename: str, on_not_found_except: bool = False) -> bool:
    """TODO
    :param filename:
    :param on_not_found_except:
    """
    if os.path.exists(filename):
        os.remove(filename)
        return True
    
    if on_not_found_except:
        raise FileNotFoundError('File was not found on the system: {}'.format(filename))
    
    return False


def file_is_not_empty(filename: str) -> bool:
    """TODO
    :param filename:
    """
    return os.path.exists(filename) and os.stat(filename).st_size > 0


def touch_file(filename: str) -> None:
    """TODO
    :param filename:
    """
    with open(filename, 'a'):
        os.utime(filename, None)


def flatten_dict(dictionary: dict, parent_key='', sep='.') -> dict:
    """TODO
    :param dictionary:
    :param parent_key:
    :param sep:
    :return:
    """
    flat_dict = {}
    for key, value in dictionary.items():
        new_key = parent_key + sep + key if parent_key else key
        if isinstance(value, dict):
            flat_dict.update(flatten_dict(value, new_key, sep=sep).items())
        else:
            flat_dict.update({new_key: value})
    
    return flat_dict
