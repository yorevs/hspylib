import signal
import time
from abc import ABC
from typing import Any, Optional, Callable

from hspylib.core.exception.input_aborted_error import InputAbortedError
from hspylib.core.tools.commons import sysout
from hspylib.core.tools.validator import Validator
from hspylib.ui.cli.vt100.vt_colors import VtColors


class MenuUtils(ABC):

    @staticmethod
    def exit_app(
            exit_code: int = signal.SIGHUP,
            frame=None,
            exit_msg: str = "Bye") -> None:

        sysout(str(frame) if frame else '', end='')
        sysout('{}\n{}'.format('\033[2J\033[H', exit_msg))
        sysout('')
        exit(exit_code if exit_code else 0)

    @staticmethod
    def print_error(
            message: str,
            argument: str = None,
            wait_interval: int = 2) -> None:

        sysout("%RED%### Error: {} {}".format(message, '"{}"'.format(argument) if argument else ''))
        time.sleep(wait_interval)
        sysout('\033[2A\033[J', end='')

    @staticmethod
    def print_warning(
            message: str,
            argument: str = None,
            wait_interval: int = 2) -> None:

        sysout(f"%YELLOW%### Warn: {message} \"{argument}\"\033[0;0;0m")
        time.sleep(wait_interval)
        sysout('\033[2A\033[J', end='')

    @staticmethod
    def prompt(
            prompt_msg: str = '',
            validator: Callable = None,
            default_value: Any = None,
            any_key: bool = False,
            on_blank_abort: bool = True,
            end: str = ': ') -> Optional[Any]:

        valid = False
        input_data = None

        while not valid:
            try:
                colorized = VtColors.colorize(
                    '%GREEN%{}{}{}%NC%'.format(
                        prompt_msg,
                        '[{}]'.format(default_value) if default_value else '',
                        end)
                )
                input_data = input(colorized)
                if not validator:
                    valid = True
                elif default_value:
                    return default_value
                elif any_key:
                    return None
                elif Validator.is_not_blank(input_data):
                    valid, msg = validator(input_data)
                    if not valid:
                        MenuUtils.print_error("{}: ".format(msg), input_data)
                else:
                    if not on_blank_abort:
                        MenuUtils.print_error("Input can't be empty: ", input_data)
                    else:
                        raise InputAbortedError()
            except EOFError as err:
                MenuUtils.print_error("Input failed: ", str(err))
                break

        return input_data

    @staticmethod
    def wait_enter(wait_msg: str = '%YELLOW%Press [Enter] to continue ...') -> None:
        sysout('')
        MenuUtils.prompt(wait_msg, any_key=True, end='')

    @staticmethod
    def title(title_str: str, color: VtColors = VtColors.YELLOW) -> None:
        erase_back = '\033[2J\033[H'
        sysout("{}\n{}{}\n".format(erase_back, color.placeholder(), title_str))
