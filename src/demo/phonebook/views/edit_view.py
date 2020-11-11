from hspylib.ui.cli.menu_utils import MenuUtils

from hspylib.core.meta.singleton import Singleton
from hspylib.core.tools.commons import sysout


class EditView(metaclass=Singleton):

    def __init__(self):
        pass

    def person(self) -> None:
        sysout("EDIT PERSON")
        MenuUtils.wait_enter()

    def company(self) -> None:
        sysout("EDIT COMPANY")
        MenuUtils.wait_enter()
