from hspylib.core.meta.singleton import Singleton
from hspylib.core.tools.commons import sysout
from hspylib.ui.cli.menu_utils import MenuUtils
from phonebook.entities.Company import Company
from phonebook.entities.Person import Person
from phonebook.services.person_service import PersonService


class CreateView(metaclass=Singleton):

    def __init__(self):
        self.person_service = PersonService()

    def person(self) -> None:
        sysout("\nCREATE PERSON\n")
        person = Person()
        person.name = MenuUtils.prompt('Name: ')
        person.age = MenuUtils.prompt('Age: ')
        person.phone = MenuUtils.prompt('Phone: ')
        person.email = MenuUtils.prompt('Email: ')
        person.address = MenuUtils.prompt('Address: ')
        person.complement = MenuUtils.prompt('Complement: ')
        self.person_service.save(person)
        MenuUtils.wait_enter()

    def company(self) -> None:
        sysout("CREATE COMPANY")
        company = Company()
        company.name = MenuUtils.prompt('Name: ')
        company.phone = MenuUtils.prompt('Phone: ')
        company.website = MenuUtils.prompt('WebSite: ')
        company.address = MenuUtils.prompt('Address: ')
        company.complement = MenuUtils.prompt('Complement: ')
        MenuUtils.wait_enter()
