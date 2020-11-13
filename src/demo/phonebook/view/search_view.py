from hspylib.ui.cli.menu_utils import MenuUtils

from hspylib.core.meta.singleton import Singleton
from hspylib.core.tools.commons import sysout
from phonebook.services.company_service import CompanyService
from phonebook.services.person_service import PersonService


class SearchView(metaclass=Singleton):

    def __init__(self):
        self.person_service = PersonService()
        self.company_service = CompanyService()

    def by_name(self) -> None:
        sysout("Search by name")
        name = MenuUtils.prompt('Person or Company name: ')
        all_persons = self.person_service.find_all(filters='name={}'.format(name))
        all_companies = self.company_service.find_all(filters='name={}'.format(name))
        self.display_list(all_persons, all_companies)
        MenuUtils.wait_enter()

    def by_uuid(self) -> None:
        sysout("Search by uuid")
        name = MenuUtils.prompt('Person or Company uuid: ')
        all_persons = self.person_service.find_all(filters='uuid={}'.format(name))
        all_companies = self.company_service.find_all(filters='uuid={}'.format(name))
        self.display_list(all_persons, all_companies)
        MenuUtils.wait_enter()

    def list_all(self) -> None:
        sysout("List all entries")
        all_persons = self.person_service.find_all()
        all_companies = self.company_service.find_all()
        self.display_list(all_persons, all_companies)
        MenuUtils.wait_enter()

    def display_list(self, *lists):
        for lst in lists:
            for record in lst:
                sysout(str(record))
