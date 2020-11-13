from hspylib.core.meta.singleton import Singleton
from hspylib.core.tools.commons import sysout
from hspylib.core.tools.validator import Validator
from hspylib.ui.cli.menu_utils import MenuUtils
from phonebook.entity.Company import Company
from phonebook.entity.Person import Person
from phonebook.entity.validator.CompanyValidator import CompanyValidator
from phonebook.entity.validator.ContactValidator import ContactValidator
from phonebook.entity.validator.PersonValidator import PersonValidator
from phonebook.services.company_service import CompanyService
from phonebook.services.person_service import PersonService


class CreateView(metaclass=Singleton):

    def __init__(self):
        self.person_service = PersonService()
        self.company_service = CompanyService()

    def person(self) -> None:
        sysout("\n%YELLOW%CREATE PERSON\n")
        person = Person()
        person.name = MenuUtils.prompt('Name', ContactValidator.validate_name)
        person.age = MenuUtils.prompt('Age', PersonValidator.validate_age)
        person.phone = MenuUtils.prompt('Phone', ContactValidator.validate_phone)
        person.email = MenuUtils.prompt('Email', PersonValidator.validate_email)
        person.address = MenuUtils.prompt('Address', Validator.is_not_blank)
        person.complement = MenuUtils.prompt('Complement', Validator.is_not_blank)
        self.person_service.save(person)
        MenuUtils.wait_enter()

    def company(self) -> None:
        sysout("\n%YELLOW%CREATE COMPANY\n")
        company = Company()
        company.name = MenuUtils.prompt('Name', ContactValidator.validate_name)
        company.phone = MenuUtils.prompt('Phone', ContactValidator.validate_phone)
        company.website = MenuUtils.prompt('WebSite', CompanyValidator.validate_website)
        company.address = MenuUtils.prompt('Address', Validator.is_not_blank)
        company.complement = MenuUtils.prompt('Complement', Validator.is_not_blank)
        self.company_service.save(company)
        MenuUtils.wait_enter()
