import logging as log
import os
import re
import sys
import termios
import tty
from typing import Type, List, Tuple, Any, Optional

from hspylib.core.tools.validator import Validator
from hspylib.ui.cli.vt100.vt_codes import VtCodes
from hspylib.ui.cli.vt100.vt_colors import VtColors

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


def __version__(version_filepath: str = ".version") -> Optional[Tuple]:
    """Retrieve the version from the version file in the form: Tuple[major,minor,build]"""
    try:
        with open(version_filepath) as fh_version:
            return tuple(map(str.strip, fh_version.read().split('.')))
    except FileNotFoundError:
        return None


def __curdir__(filepath: str) -> str:
    """Retrieve the application directory"""
    return os.path.dirname(os.path.realpath(filepath))


def environ_name(property_name: str) -> str:
    """Retrieve the environment name of the specified property name"""
    return re.sub('[ -.]', '_', property_name).upper()


def sysout(string: str, end: str = '\n') -> None:
    """Print the unicode input_string decoding vt100 placeholders"""
    if Validator.is_not_blank(string):
        msg = VtColors.colorize(VtCodes.decode(f"{string}"))
        print(msg, file=sys.stdout, flush=True, end=end)


def syserr(string: str, end: str = '\n') -> None:
    """Print the unicode input_string decoding vt100 placeholders"""
    if Validator.is_not_blank(string):
        msg = VtColors.colorize(VtCodes.decode(f"%RED%{string}%NC%"))
        print(msg, file=sys.stderr, flush=True, end=end)


def class_attribute_names(clazz: Type) -> tuple:
    """TODO
    :param clazz:
    """
    return tuple(vars(clazz()).keys()) if clazz else None


def class_attribute_values(instance: dict) -> tuple:
    """TODO
    :param instance:
    """
    return tuple(instance.values()) if object else None


def split_and_filter(input_str: str, regex_filter: str = '.*', delimiter: str = '\n') -> List[str]:
    """TODO
    :param input_str:
    :param regex_filter:
    :param delimiter:
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
    else:
        if on_not_found_except:
            raise FileNotFoundError('File was not found on the system: {}'.format(filename))
        else:
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


def screen_size() -> Optional[List[str]]:
    """TODO
    """

    if sys.stdout.isatty():
        return os.popen('stty size').read().split()
    else:
        return None


def set_enable_echo(enable: bool = True) -> None:
    """
    TODO
    :param enable:
    :return:
    """
    if sys.stdout.isatty():
        os.popen(f"stty {'echo -raw' if enable else 'raw -echo min 0'}").read()


def get_cursor_position() -> Optional[Tuple[int, int]]:
    """ Get the terminal cursor position
    Solution taken from:
    - https://stackoverflow.com/questions/46651602/determine-the-terminal-cursor-position-with-an-ansi-sequence-in-python-3
    :return:
    """
    if sys.stdout.isatty():
        buf = ""
        stdin = sys.stdin.fileno()
        attrs = termios.tcgetattr(stdin)

        try:
            tty.setcbreak(stdin, termios.TCSANOW)
            sys.stdout.write("\x1b[6n")
            sys.stdout.flush()
            while True:
                buf += sys.stdin.read(1)
                if buf[-1] == "R":
                    break
        finally:
            termios.tcsetattr(stdin, termios.TCSANOW, attrs)
        try:
            matches = re.match(r"^\x1b\[(\d*);(\d*)R", buf)
            groups = matches.groups()
        except AttributeError:
            return None

        return int(groups[0]), int(groups[1])
    else:
        return None
