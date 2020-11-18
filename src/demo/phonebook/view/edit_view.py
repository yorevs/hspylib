from hspylib.core.crud.crud_service import CrudService
from hspylib.core.exception.InputAbortedError import InputAbortedError
from hspylib.core.meta.singleton import Singleton
from hspylib.core.tools.validator import Validator
from hspylib.ui.cli.menu_utils import MenuUtils
from phonebook.entity.Company import Company
from phonebook.entity.Person import Person
from phonebook.entity.validator.CompanyValidator import CompanyValidator
from phonebook.entity.validator.ContactValidator import ContactValidator
from phonebook.entity.validator.PersonValidator import PersonValidator
from phonebook.repository.company_repository import CompanyRepository
from phonebook.repository.person_repository import PersonRepository


class EditView(metaclass=Singleton):

    def __init__(self):
        self.person_service = CrudService[Person](PersonRepository())
        self.company_service = CrudService[Company](CompanyRepository())

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
                found.address = MenuUtils.prompt('Address', Validator.is_not_blank, found.address)
                found.complement = MenuUtils.prompt('Complement', Validator.is_not_blank, found.complement)
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
                found.address = MenuUtils.prompt('Address',  Validator.is_not_blank, found.address)
                found.complement = MenuUtils.prompt('Complement', Validator.is_not_blank, found.complement)
                self.company_service.save(found)
            except InputAbortedError:
                return MenuUtils.wait_enter('Operation aborted. Press [Enter]...')

            MenuUtils.wait_enter()
