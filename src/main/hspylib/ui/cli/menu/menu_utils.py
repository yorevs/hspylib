import signal
import time
from abc import ABC
from typing import Any, Optional, Callable

from hspylib.core.exception.input_aborted_error import InputAbortedError
from hspylib.core.tools.commons import sysout, syserr
from hspylib.core.tools.validator import Validator
from hspylib.ui.cli.vt100.vt_colors import VtColors


class MenuUtils(ABC):

    @staticmethod
    def exit_app(
            exit_code: int = signal.SIGHUP,
            frame=None,
            exit_msg: str = "Done.") -> None:

        sysout(str(frame) if frame else '', end='')
        sysout(f"%VT_ED2%%VT_HOM%\n{exit_msg}\n")
        exit(exit_code if exit_code else 0)

    @staticmethod
    def print_error(
            message: str,
            argument: Any = None,
            wait_interval: int = 2,
            color: VtColors = VtColors.RED) -> None:

        syserr(f"{color.placeholder()}### Error: {message} \"{argument or ''}\"%NC%")
        time.sleep(wait_interval)
        sysout('%VT_CUU(2)%%VT_ED0%', end='')

    @staticmethod
    def print_warning(
            message: str,
            argument: str = None,
            wait_interval: int = 2,
            color: VtColors = VtColors.YELLOW) -> None:

        sysout(f"{color.placeholder()}### Warn: {message} \"{argument or ''}\"%NC%")
        time.sleep(wait_interval)
        sysout('%VT_CUU(2)%%VT_ED0%', end='')

    @staticmethod
    def prompt(
            prompt_msg: str = '',
            validator: Callable = None,
            default_value: Any = None,
            any_key: bool = False,
            on_blank_abort: bool = True,
            color: VtColors = VtColors.GREEN,
            end: str = ': ') -> Optional[Any]:

        valid = False
        input_data = None

        while not valid:
            try:
                colorized = VtColors.colorize(
                    '{}{}{}{}{}'.format(
                        color.placeholder(),
                        prompt_msg,
                        '[{}]'.format(default_value) if default_value else '',
                        end, VtColors.NC.placeholder())
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
    def wait_enter(
            wait_msg: str = 'Press [Enter] to continue ...',
            color: VtColors = VtColors.YELLOW) -> None:
        MenuUtils.prompt(wait_msg, any_key=True, color=color, end='')

    @staticmethod
    def title(title_str: str, color: VtColors = VtColors.YELLOW) -> None:
        sysout(f"%VT_ED2%%VT_HOM%\n{color.placeholder()}{title_str}\n")
