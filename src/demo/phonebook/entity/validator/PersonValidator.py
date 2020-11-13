from typing import List

from hspylib.core.tools.validator import Validator
from phonebook.entity.Person import Person


class PersonValidator(Validator):

    def __call__(self, *persons, **kwargs) -> List[dict]:
        errors = []
        assert len(persons) == 1, "One person exactly is required to validate"
        assert isinstance(persons[0], Person), "Can only validate Person entities"

        return errors

    @staticmethod
    def validate_age(age: str) -> bool:
        return Validator.is_integer(age, min_value=10, max_value=115)

    @staticmethod
    def validate_email(email: str) -> bool:
        return Validator \
            .matches(email, PersonValidator.RegexCommons.EMAIL_W3C)
