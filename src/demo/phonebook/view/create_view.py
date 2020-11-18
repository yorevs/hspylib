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


class CreateView(metaclass=Singleton):

    def __init__(self):
        self.person_service = CrudService(PersonRepository())
        self.company_service = CrudService(CompanyRepository())

    def person(self) -> None:
        MenuUtils.title('CREATE PERSON')
        person = Person()
        try:
            person.name = MenuUtils.prompt('Name', ContactValidator.validate_name)
            person.age = MenuUtils.prompt('Age', PersonValidator.validate_age)
            person.phone = MenuUtils.prompt('Phone', ContactValidator.validate_phone)
            person.email = MenuUtils.prompt('Email', PersonValidator.validate_email)
            person.address = MenuUtils.prompt('Address', Validator.is_not_blank)
            person.complement = MenuUtils.prompt('Complement', Validator.is_not_blank)
            self.person_service.save(person)
        except InputAbortedError:
            return MenuUtils.wait_enter('Operation aborted. Press [Enter]...')

        MenuUtils.wait_enter()

    def company(self) -> None:
        MenuUtils.title('CREATE COMPANY')
        company = Company()
        try:
            company.name = MenuUtils.prompt('Name', ContactValidator.validate_name)
            company.phone = MenuUtils.prompt('Phone', ContactValidator.validate_phone)
            company.website = MenuUtils.prompt('WebSite', CompanyValidator.validate_website)
            company.address = MenuUtils.prompt('Address', Validator.is_not_blank)
            company.complement = MenuUtils.prompt('Complement', Validator.is_not_blank)
            self.company_service.save(company)
        except InputAbortedError:
            return MenuUtils.wait_enter('Operation aborted. Press [Enter]...')

        MenuUtils.wait_enter()
