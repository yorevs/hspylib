import logging as log
import os
import re
import sys
from typing import Type, List, Tuple

from hspylib.core.enum.charset import Charset

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


# @purpose: Print the unicode string
def sysout(string: str, end: str = '\n', encoding: Charset = Charset.UTF_8):
    sys.stdout.write(string.encode(str(encoding)).decode('unicode-escape') + end)


# @purpose: Print the unicode string
def syserr(string: str, end: str = '\n', encoding: Charset = Charset.UTF_8):
    sys.stderr.write(string.encode(str(encoding)).decode('unicode-escape') + end)


def class_attribute_names(clazz: Type) -> tuple:
    return tuple(vars(clazz()).keys()) if clazz else None


def class_attribute_values(instance: dict) -> tuple:
    return tuple(instance.values()) if object else None


def split_and_filter(input_str: str, regex_filter: str = '.*', delimiter: str = '\n') -> List[str]:
    regex = re.compile(regex_filter)
    result_list = list(filter(regex.search, input_str.split(delimiter)))

    return result_list


def get_or_default(array: Tuple, index: int, default_value=None):
    return array[index] if index < len(array) else default_value


def str_to_bool(string: str, true_values=None) -> bool:
    if true_values is None:
        true_values = ['true', 'on', 'yes', '1', 'y']
    return string.lower() in true_values if string else False
