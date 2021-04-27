from typing import List, Tuple

from hspylib.core.tools.regex_commons import RegexCommons
from hspylib.core.tools.validator import Validator
from phonebook.entity.Person import Person
from phonebook.entity.validator.contact_validator import ContactValidator


class PersonValidator(ContactValidator):

    def __call__(self, *persons: Person, **kwargs) -> Tuple[bool, List[dict]]:
        errors = []
        assert len(persons) == 1, "Exactly one person can be validated at a time. Given: {}".format(len(persons))
        assert isinstance(persons[0], Person), "Only persons can be validated"
        self.assert_valid(errors, self.validate_name(persons[0].name))
        self.assert_valid(errors, self.validate_age(str(persons[0].age)))
        self.assert_valid(errors, self.validate_phone(persons[0].phone))
        self.assert_valid(errors, self.validate_email(persons[0].email))
        self.assert_valid(errors, self.validate_address(persons[0].address))
        self.assert_valid(errors, self.validate_complement(persons[0].complement))

        return len(errors) == 0, errors

    @staticmethod
    def validate_age(age: str) -> (bool, str):
        return Validator.is_integer(age, min_value=10, max_value=115), "Invalid age"

    @staticmethod
    def validate_email(email: str) -> (bool, str):
        return Validator \
            .matches(email, RegexCommons.EMAIL_W3C), "Invalid email"
