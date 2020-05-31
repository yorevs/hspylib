import logging as log
import os
import sys
from typing import Type

LOG_FMT = '{} {} {} {}{} {} '.format(
    '%(asctime)s',
    '[%(threadName)-10.10s]',
    '%(levelname)-5.5s',
    '%(name)s::',
    '%(funcName)s(@Line:%(lineno)d)',
    '%(message)s'
)


def log_init(log_file: str, level: int = log.INFO, log_fmt: str = LOG_FMT):
    with open(log_file, 'w'):
        os.utime(log_file, None)
    f_mode = "a"
    log.basicConfig(
        filename=log_file,
        format=log_fmt,
        level=level,
        filemode=f_mode)

    return log


# @purpose: Print the unicode string
def sysout(string, end='\n', encoding='utf-8'):
    sys.stdout.write(string.encode(encoding).decode('unicode-escape')+end)


# @purpose: Print the unicode string
def syserr(string, end='\n', encoding='utf-8'):
    sys.stderr.write(string.encode(encoding).decode('unicode-escape')+end)


def class_attribute_names(clazz: Type) -> tuple:
    return tuple(vars(clazz()).keys()) if clazz else None


def class_attribute_values(instance: dict) -> tuple:
    return tuple(instance.values()) if object else None
