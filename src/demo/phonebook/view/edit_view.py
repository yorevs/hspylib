from hspylib.ui.cli.menu_utils import MenuUtils

from hspylib.core.meta.singleton import Singleton
from hspylib.core.tools.commons import sysout
from phonebook.services.company_service import CompanyService
from phonebook.services.person_service import PersonService


class EditView(metaclass=Singleton):

    def __init__(self):
        self.person_service = PersonService()
        self.company_service = CompanyService()

    def person(self) -> None:
        sysout("EDIT PERSON")
        uuid = MenuUtils.prompt('Enter uuid: ')
        found = self.person_service.find_one(uuid)
        if not found:
            MenuUtils.print_error("Person does not exist", uuid)
        else:
            found.name = MenuUtils.prompt('Name[{}]: '.format(found.name))
            found.age = MenuUtils.prompt('Age[{}]: '.format(found.age))
            found.phone = MenuUtils.prompt('Phone[{}]: '.format(found.phone))
            found.email = MenuUtils.prompt('Email[{}]: '.format(found.email))
            found.address = MenuUtils.prompt('Address[{}]: '.format(found.address))
            found.complement = MenuUtils.prompt('Complement[{}]: '.format(found.complement))
            self.person_service.save(found)

        MenuUtils.wait_enter()

    def company(self) -> None:
        sysout("EDIT COMPANY")
        uuid = MenuUtils.prompt('Enter uuid: ')
        found = self.company_service.find_one(uuid)
        if not found:
            MenuUtils.print_error("Company does not exist", uuid)
        else:
            found.name = MenuUtils.prompt('Name[{}]: '.format(found.name))
            found.phone = MenuUtils.prompt('Phone[{}]: '.format(found.phone))
            found.website = MenuUtils.prompt('WebSite[{}]: '.format(found.website))
            found.address = MenuUtils.prompt('Address[{}]: '.format(found.address))
            found.complement = MenuUtils.prompt('Complement[{}]: '.format(found.complement))
            self.company_service.save(found)

        MenuUtils.wait_enter()
