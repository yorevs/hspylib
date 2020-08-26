import signal
import time
from abc import ABC


class MenuUtils(ABC):
    @classmethod
    def exit_app(cls, exit_code: int = signal.SIGHUP, frame=None) -> None:
        print('{}\n{}'.format('\033[2J\033[H', 'Bye'))
        print('')
        exit(exit_code if exit_code else 0)

    @staticmethod
    def print_error(message: str, argument: str = None, wait_interval: int = 2):
        print(f"\033[0;31m### Error: {message} \"{argument}\"\033[0;0;0m")
        time.sleep(wait_interval)
        print('\033[2A\033[J', end='')

    @staticmethod
    def print_warning(message: str, argument: str = None, wait_interval: int = 2):
        print(f"\033[0;93m### Warn: {message} \"{argument}\"\033[0;0;0m")
        time.sleep(wait_interval)
        print('\033[2A\033[J', end='')

    @staticmethod
    def prompt(prompt_msg: str = '$ ', end: str = '', clear: bool = False):
        try:
            if clear:
                print('\033[2J\033[H', end='')
            input_data = input('{}{}'.format(prompt_msg, end))
            return input_data
        except EOFError:
            return None

    @staticmethod
    def wait_enter():
        print('')
        MenuUtils.prompt('Press \033[0;32m[Enter]\033[0;0;0m to continue ...')
