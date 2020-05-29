import logging as log
import os

DEFAULT_LOG_FMT = '{} {} {} {}{} {} '.format(
    '%(asctime)s',
    '[%(threadName)-10.10s]',
    '%(levelname)-5.5s',
    '%(name)s::',
    '%(funcName)s(@Line:%(lineno)d)',
    '%(message)s'
)


def log_init(log_file: str, level: int = log.INFO, log_fmt: str = DEFAULT_LOG_FMT):
    with open(log_file, 'w'):
        os.utime(log_file, None)
    f_mode = "a"
    log.basicConfig(
        filename=log_file,
        format=log_fmt,
        level=level,
        filemode=f_mode)

    return log
