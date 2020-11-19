import logging as log
import os
import re
import sys
from typing import Type, List, Tuple, Any, Optional

from hspylib.core.enum.charset import Charset
from hspylib.core.tools.validator import Validator
from hspylib.ui.cli.vt100.vt_colors import VtColors

LOG_FMT = '{} {} {} {}{} {} '.format(
    '%(asctime)s',
    '[%(threadName)-10.10s]',
    '%(levelname)-5.5s',
    '%(filename)s::',
    '%(funcName)s(@Line:%(lineno)d)',
    '%(message)s'
)


# @purpose: Initialize the system logger
def log_init(
        log_file: str,
        create_new: bool = True,
        f_mode: str = 'a',
        level: int = log.DEBUG,
        log_fmt: str = LOG_FMT):
    with open(log_file, 'w' if create_new else 'a'):
        os.utime(log_file, None)

    log.basicConfig(
        filename=log_file,
        format=log_fmt,
        level=level,
        filemode=f_mode)

    return log


# @purpose: Print the unicode input_string
def sysout(string: str, end: str = '\n', encoding: Charset = Charset.UTF_8) -> None:
    if Validator.is_not_blank(string):
        sys.stdout.write(
            VtColors.colorize(string.encode(str(encoding)).decode('unicode-escape') + end))


# @purpose: Print the unicode input_string
def syserr(string: str, end: str = '\n', encoding: Charset = Charset.UTF_8) -> None:
    if Validator.is_not_blank(string):
        sys.stderr.write(
            VtColors.colorize(string.encode(str(encoding)).decode('unicode-escape') + end))


def class_attribute_names(clazz: Type) -> tuple:
    return tuple(vars(clazz()).keys()) if clazz else None


def class_attribute_values(instance: dict) -> tuple:
    return tuple(instance.values()) if object else None


def split_and_filter(input_str: str, regex_filter: str = '.*', delimiter: str = '\n') -> List[str]:
    regex = re.compile(regex_filter)
    result_list = list(filter(regex.search, input_str.split(delimiter)))

    return result_list


def get_or_default(options: Tuple, index: int, default_value=None) -> Optional[Any]:
    """Retrieve an item from the options list or None if index is out of range
    :param options: The available list of options
    :param index: The index of the item
    :param default_value: The default value if the index is out of range
    """
    return options[index] if index < len(options) else default_value


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
    if os.path.exists(filename):
        os.remove(filename)
        return True
    else:
        if on_not_found_except:
            raise FileNotFoundError('File was not found on the system: {}'.format(filename))
        else:
            return False


def file_is_not_empty(filename: str) -> bool:
    return os.path.exists(filename) and os.stat(filename).st_size > 0


def touch_file(filename: str) -> None:
    with open(filename, 'a'):
        os.utime(filename, None)
