from hspylib.ui.cli.menu_utils import MenuUtils

from hspylib.core.meta.singleton import Singleton
from hspylib.core.tools.commons import sysout


class SearchView(metaclass=Singleton):

    def __init__(self):
        pass

    def by_name(self) -> None:
        sysout("Search by name")
        MenuUtils.wait_enter()

    def by_uuid(self) -> None:
        sysout("Search by uuid")
        MenuUtils.wait_enter()

    def list_all(self) -> None:
        sysout("List all entries")
        MenuUtils.wait_enter()
