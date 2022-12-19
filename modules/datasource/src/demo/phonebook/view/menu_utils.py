from hspylib.core.tools.commons import sysout
from hspylib.modules.cli.keyboard import Keyboard


class MenuUtils:
    @classmethod
    def title(cls, param):
        pass

    @classmethod
    def prompt(cls, param, name):
        pass

    @classmethod
    def wait_enter(cls, wait_message: str = None):
        sysout(wait_message)
        Keyboard.wait_keystroke()

    @classmethod
    def print_error(cls, param, uuid):
        pass
