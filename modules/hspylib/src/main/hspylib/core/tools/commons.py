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

   Copyright 2021, HSPyLib team
"""
import inspect
import logging as log
import os
import pathlib
import re
import sys
from datetime import datetime, timedelta
from typing import Any, List, Optional, Tuple, Type, Union

from hspylib.core.tools.constants import DATE_TIME_FORMAT, TRUE_VALUES
from hspylib.core.tools.validator import Validator
from hspylib.modules.cli.vt100.vt_codes import VtCodes
from hspylib.modules.cli.vt100.vt_colors import VtColors

# pylint: disable=consider-using-f-string
LOG_FMT = '{} {} {} {}{} {} '.format(
    '%(asctime)s',
    '[%(threadName)-10.10s]',
    '%(levelname)-5.5s',
    '%(filename)s::',
    '%(funcName)s(@Line:%(lineno)d)',
    '%(message)s'
)


def _reset_logger():
    """TODO"""
    # Remove handlers if there is any.
    root = log.getLogger()
    if root.handlers:
        for handler in root.handlers:
            root.removeHandler(handler)


def log_init(
    log_file: str,
    create_new: bool = True,
    mode: str = 'a',
    level: int = log.DEBUG,
    filename: str = LOG_FMT) -> bool:
    """Initialize the system logger
    :param log_file: TODO
    :param create_new:  TODO
    :param mode:  TODO
    :param level:  TODO
    :param filename:  TODO
    """
    # if someone tried to log something before log_init is called, Python creates a default handler that is going to
    # mess our logs.
    _reset_logger()

    create = bool(create_new or not os.path.exists(log_file))
    with open(log_file, 'w' if create else 'a', encoding="utf8"):
        os.utime(log_file, None)
        log.basicConfig(
            filename=log_file,
            format=filename,
            level=level,
            filemode=mode)
        log.info(
            "Logger init. filename=%s level=%s mode=%s append=%s", os.path.basename(log_file), level, mode, not create)

    return os.path.exists(log_file)


def is_debugging():
    """TODO"""
    for frame in inspect.stack():
        if frame[1].endswith("pydevd.py"):
            return True
    return False


def now() -> str:
    """TODO"""
    return datetime.now().strftime(DATE_TIME_FORMAT)


def now_ms() -> int:
    """TODO"""
    return int(datetime.now().timestamp())


def read_version(version_filepath: str = ".version") -> Tuple[int, int, int]:
    """Retrieve the version from the version file in the form: Tuple[major,minor,build]"""
    try:
        log.info("Reading version from %s", version_filepath)
        with open(version_filepath, encoding="utf8") as fh_version:
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
    """TODO
    :param clazz: TODO
    """
    instance = clazz()
    return tuple(vars(instance).keys()) if clazz else None


def class_attribute_values(instance: dict) -> Optional[Tuple]:
    """TODO
    :param instance: TODO
    """
    return tuple(instance.values()) if instance else None


def new_dynamic_object(type_name: str, inherited_type: Any = object):
    """TODO
    :param: type_name: TODO
    :param: inherited_type: TODO
    """

    return type(type_name, (inherited_type,), {})()


def split_and_filter(input_str: str, regex_filter: str = '.*', delimiter: str = '\n') -> List[str]:
    """Split the string using the delimiter and filter using the specified regex filter
    :param input_str: The string to be split
    :param regex_filter: The regex to filter the string
    :param delimiter: The delimiter according which to split the string
    """
    regex = re.compile(regex_filter)
    result_list = list(filter(regex.search, input_str.split(delimiter)))

    return result_list


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


def search_dict(root_element: dict, search_path: str, parent_key='', sep='.') -> Optional[Any]:
    """
    TODO
    :param root_element:
    :param search_path:
    :param parent_key:
    :param sep:
    :return:
    """
    found = search_path == parent_key
    el = None
    if not found and isinstance(root_element, dict):
        for key, value in root_element.items():
            if found:
                break
            el_path = parent_key + sep + key if parent_key else key
            if search_path == el_path:
                found, el = True, value
                break
            if isinstance(value, dict):
                found, el = search_dict(value, search_path, el_path, sep=sep)
            elif isinstance(value, list):
                for next_val in value:
                    found, el = search_dict(next_val, search_path, el_path, sep=sep)
            # Skip if the element is a leaf

    return found, el


def get_or_default(options: Union[tuple, list], index: int, default_value=None) -> Optional[Any]:
    """Retrieve an item from the options list or default_value if index is out of range
    :param options: The available list of options
    :param index: The index of the item
    :param default_value: The default value if the index is out of range
    """
    return options[index] if index < len(options) else default_value


def get_by_key_or_default(options: dict, key: str, default_value=None) -> Optional[Any]:
    """Retrieve an item from the options list or default_value if key was not found
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
    if string is None:
        return False
    if true_values is None:
        true_values = TRUE_VALUES
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
        raise FileNotFoundError(f'File was not found on the system: {filename}')

    return False


def file_is_not_empty(filename: str) -> bool:
    """TODO
    :param filename:
    """
    return os.path.exists(filename) and os.stat(filename).st_size > 0


def touch_file(filename: str, encoding: str = 'utf-8') -> None:
    """TODO
    :param filename:
    :param encoding:
    """
    with open(filename, 'a', encoding=encoding):
        os.utime(filename, None)


def human_readable_bytes(size_in_bytes: int) -> Tuple[str, str]:
    """TODO
    :param size_in_bytes:
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
    """TODO
    :param time_microseconds:
    """
    delta = timedelta(microseconds=time_microseconds)
    total_seconds = delta.seconds
    seconds = total_seconds % 60
    minutes = total_seconds / 60 % 60
    hours = total_seconds / 3600
    microseconds = delta.microseconds
    # Using format: HH:MM:SS.uuuuuu
    str_line = f"{hours:02d}:{minutes:02d}:{seconds:02d}.{microseconds:06d}"

    return str_line


def build_url(url_or_part: str) -> str:
    """TODO
    :param url_or_part:
    """
    if re.match(r'https?://.*', url_or_part):
        return url_or_part

    return f"http://{url_or_part}"
