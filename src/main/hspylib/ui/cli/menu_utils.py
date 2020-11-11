import signal
import time
from abc import ABC
from typing import Any

from hspylib.core.tools.commons import sysout


class MenuUtils(ABC):
    @classmethod
    def exit_app(cls, exit_code: int = signal.SIGHUP, exit_msg: str = "Bye", frame=None) -> None:
        sysout(frame if frame else '', end='')
        sysout('{}\n{}'.format('\033[2J\033[H', exit_msg))
        sysout('')
        exit(exit_code if exit_code else 0)

    @staticmethod
    def print_error(message: str, argument: str = None, wait_interval: int = 2) -> None:
        sysout(f"\033[0;31m### Error: {message} \"{argument}\"\033[0;0;0m")
        time.sleep(wait_interval)
        sysout('\033[2A\033[J', end='')

    @staticmethod
    def print_warning(message: str, argument: str = None, wait_interval: int = 2) -> None:
        sysout(f"\033[0;93m### Warn: {message} \"{argument}\"\033[0;0;0m")
        time.sleep(wait_interval)
        sysout('\033[2A\033[J', end='')

    @staticmethod
    def prompt(prompt_msg: str = '$ ', end: str = '', clear: bool = False) -> Any:
        try:
            if clear:
                sysout('\033[2J\033[H', end='')
            input_data = input('{}{}'.format(prompt_msg, end))
            return input_data
        except EOFError:
            return None

    @staticmethod
    def wait_enter() -> None:
        sysout('')
        MenuUtils.prompt('Press \033[0;32m[Enter]\033[0;0;0m to continue ...')
