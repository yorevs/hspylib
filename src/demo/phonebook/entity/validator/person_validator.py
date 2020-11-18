from typing import List, Tuple

from hspylib.core.tools.validator import Validator
from phonebook.entity.person import Person
from phonebook.entity.validator.contact_validator import ContactValidator


class PersonValidator(ContactValidator):

    def __call__(self, *persons, **kwargs) -> Tuple[bool, List[dict]]:
        errors = []
        assert len(persons) == 1, "Only one person can be validated at a time"
        assert isinstance(persons[0], Person), "Only persons can be validated"
        assert self.validate_age(persons[0].age), "Invalid age: {}".format(persons[0].age)
        assert self.validate_email(persons[0].email), "Invalid age: {}".format(persons[0].email)
        super().__call__(persons, kwargs)

        return len(errors) == 0, errors

    @staticmethod
    def validate_age(age: str) -> (bool, str):
        return Validator.is_integer(age, min_value=10, max_value=115), "Invalid age"

    @staticmethod
    def validate_email(email: str) -> (bool, str):
        return Validator \
            .matches(email, PersonValidator.RegexCommons.EMAIL_W3C), "Invalid email"
