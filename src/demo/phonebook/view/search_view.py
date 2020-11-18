from typing import List

from hspylib.core.crud.crud_service import CrudService
from hspylib.core.exception.InputAbortedError import InputAbortedError
from hspylib.core.meta.singleton import Singleton
from hspylib.core.model.entity import Entity
from hspylib.core.tools.commons import sysout
from hspylib.ui.cli.menu_utils import MenuUtils
from hspylib.ui.cli.table_renderer import TableRenderer
from phonebook.entity.Company import Company
from phonebook.entity.Person import Person
from phonebook.repository.company_repository import CompanyRepository
from phonebook.repository.person_repository import PersonRepository


class SearchView(metaclass=Singleton):

    def __init__(self):
        self.person_service = CrudService[Person](PersonRepository())
        self.company_service = CrudService[Company](CompanyRepository())

    def by_name(self) -> None:
        MenuUtils.title('SEARCH BY NAME')
        try:
            name = MenuUtils.prompt('Person or Company name')
            all_persons = self.person_service.list(filters='name={}'.format(name))
            all_companies = self.company_service.list(filters='name={}'.format(name))
            self.display_contacts(all_persons, all_companies)
        except InputAbortedError:
            pass

    def by_uuid(self) -> None:
        MenuUtils.title('SEARCH BY UUID')
        try:
            name = MenuUtils.prompt('Person or Company uuid')
            all_persons = self.person_service.list(filters='uuid={}'.format(name))
            all_companies = self.company_service.list(filters='uuid={}'.format(name))
            self.display_contacts(all_persons, all_companies)
        except InputAbortedError:
            pass

    def list_all(self) -> None:
        all_persons = self.person_service.list()
        all_companies = self.company_service.list()
        self.display_contacts(all_persons, all_companies)

    @staticmethod
    def display_contacts(persons, companies):

        if len(persons) > 0 or len(companies) > 0:
            SearchView.display_table(
                ["UUID", "NAME", "AGE", "PHONE", "EMAIL", "ADDRESS", "CPL"], persons, 'PERSONS')
            SearchView.display_table(
                ["UUID", "NAME", "PHONE", "WEBSITE", "ADDRESS", "CPL"], companies, 'COMPANIES')
        else:
            sysout('-=- No results to be displayed -=-')
            MenuUtils.wait_enter()

    @staticmethod
    def display_table(headers: List[str], entities: List[Entity], title: str):
        MenuUtils.title('LISTING ALL {}'.format(title))
        tr = TableRenderer(headers, [c.to_values() for c in entities], title)
        tr.adjust_sizes_by_largest_cell()
        tr.render()
        MenuUtils.wait_enter()
