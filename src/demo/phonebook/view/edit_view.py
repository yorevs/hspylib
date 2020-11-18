from hspylib.core.exception.InputAbortedError import InputAbortedError
from hspylib.core.meta.singleton import Singleton
from hspylib.ui.cli.menu_utils import MenuUtils
from phonebook.entity.validator.CompanyValidator import CompanyValidator
from phonebook.entity.validator.ContactValidator import ContactValidator
from phonebook.entity.validator.PersonValidator import PersonValidator
from phonebook.service.CompanyService import CompanyService
from phonebook.service.PersonService import PersonService


class EditView(metaclass=Singleton):

    def __init__(self):
        self.person_service = PersonService()
        self.company_service = CompanyService()

    def person(self) -> None:
        MenuUtils.title('EDIT PERSON')
        uuid = MenuUtils.prompt('Enter uuid')
        found = self.person_service.get(uuid)
        if not found:
            MenuUtils.print_error("Person does not exist", uuid)
        else:
            try:
                found.name = MenuUtils.prompt('Name', ContactValidator.validate_name, found.name)
                found.age = MenuUtils.prompt('Age', PersonValidator.validate_age, found.age)
                found.phone = MenuUtils.prompt('Phone', ContactValidator.validate_phone, found.phone)
                found.email = MenuUtils.prompt('Email', PersonValidator.validate_email, found.email)
                found.address = MenuUtils.prompt(
                    'Address', on_blank_abort=False, validator=ContactValidator.validate_address)
                found.complement = MenuUtils.prompt(
                    'Complement', on_blank_abort=False, validator=ContactValidator.validate_complement)
                self.person_service.save(found)
            except InputAbortedError:
                return MenuUtils.wait_enter('Operation aborted. Press [Enter]...')

            MenuUtils.wait_enter()

    def company(self) -> None:
        MenuUtils.title('EDIT COMPANY')
        uuid = MenuUtils.prompt('Enter uuid')
        found = self.company_service.get(uuid)
        if not found:
            MenuUtils.print_error("Company does not exist", uuid)
        else:
            try:
                found.name = MenuUtils.prompt('Name', ContactValidator.validate_name, found.name)
                found.phone = MenuUtils.prompt('Phone', ContactValidator.validate_phone, found.phone)
                found.website = MenuUtils.prompt('WebSite', CompanyValidator.validate_website, found.website)
                found.address = MenuUtils.prompt(
                    'Address', on_blank_abort=False, validator=ContactValidator.validate_address)
                found.complement = MenuUtils.prompt(
                    'Complement', on_blank_abort=False, validator=ContactValidator.validate_complement)
                self.company_service.save(found)
            except InputAbortedError:
                return MenuUtils.wait_enter('Operation aborted. Press [Enter]...')

            MenuUtils.wait_enter()
