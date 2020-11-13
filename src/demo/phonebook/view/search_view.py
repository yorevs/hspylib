from typing import List

from hspylib.core.model.entity import Entity
from hspylib.ui.cli.table_renderer import TableRenderer

from hspylib.ui.cli.menu_utils import MenuUtils

from hspylib.core.meta.singleton import Singleton
from hspylib.core.tools.commons import sysout
from phonebook.entity.Person import Person
from phonebook.services.company_service import CompanyService
from phonebook.services.person_service import PersonService


class SearchView(metaclass=Singleton):

    def __init__(self):
        self.person_service = PersonService()
        self.company_service = CompanyService()

    def by_name(self) -> None:
        sysout("\n%YELLOW%SEARCH BY NAME\n")
        name = MenuUtils.prompt('Person or Company name')
        all_persons = self.person_service.find_all(filters='name={}'.format(name))
        all_companies = self.company_service.find_all(filters='name={}'.format(name))
        self.display_contacts(all_persons, all_companies)
        MenuUtils.wait_enter()

    def by_uuid(self) -> None:
        sysout("\n%YELLOW%SEARCH BY UUID\n")
        name = MenuUtils.prompt('Person or Company uuid')
        all_persons = self.person_service.find_all(filters='uuid={}'.format(name))
        all_companies = self.company_service.find_all(filters='uuid={}'.format(name))
        self.display_contacts(all_persons, all_companies)
        MenuUtils.wait_enter()

    def list_all(self) -> None:
        sysout("\n%YELLOW%LIST ALL ENTRIES\n")
        all_persons = self.person_service.find_all()
        all_companies = self.company_service.find_all()
        if len(all_persons) > 0 or len(all_companies) > 0:
            self.display_contacts(all_persons, all_companies)
        else:
            sysout('-=- No results to be displayed -=-')
            MenuUtils.wait_enter()

    @staticmethod
    def display_contacts(persons, companies):

        SearchView.display_table(
            ["UUID", "NAME", "AGE", "PHONE", "EMAIL", "ADDRESS", "CPL"], persons, 'PERSONS')
        SearchView.display_table(
            ["UUID", "NAME", "PHONE", "WEBSITE", "ADDRESS", "CPL"], companies, 'COMPANIES')

    @staticmethod
    def display_table(headers: List[str], entities: List[Entity], title: str):
        tr = TableRenderer(headers, [c.to_values() for c in entities], title)
        tr.adjust_sizes_by_largest_cell()
        tr.render()
        MenuUtils.wait_enter()
