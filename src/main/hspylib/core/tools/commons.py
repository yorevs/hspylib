import logging as log
import os
import re
import sys
from typing import Type, List

from hspylib.core.enum.charset import Charset

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
def sysout(string, end='\n', encoding=Charset.UTF_8):
    sys.stdout.write(string.encode(encoding).decode('unicode-escape') + end)


# @purpose: Print the unicode string
def syserr(string, end='\n', encoding=Charset.UTF_8):
    sys.stderr.write(string.encode(encoding).decode('unicode-escape') + end)


def class_attribute_names(clazz: Type) -> tuple:
    return tuple(vars(clazz()).keys()) if clazz else None


def class_attribute_values(instance: dict) -> tuple:
    return tuple(instance.values()) if object else None


def split_and_filter(input_str: str, regex_filter: str = '.*', delimiter: str = '\n') -> List[str]:
    regex = re.compile(regex_filter)
    result_list = list(filter(regex.search, input_str.split(delimiter)))

    return result_list
