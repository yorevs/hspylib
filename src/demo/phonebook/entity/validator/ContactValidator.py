from typing import List

from hspylib.core.tools.validator import Validator
from phonebook.entity.Person import Person


class ContactValidator(Validator):

    def __call__(self, *persons, **kwargs) -> List[dict]:
        errors = []
        assert len(persons) == 1, "One person exactly is required to validate"
        assert isinstance(persons[0], Person), "Can only validate Person entities"

        return errors

    @staticmethod
    def validate_name(name: str) -> bool:
        return Validator \
            .matches(name, Validator.RegexCommons.COMMON_3_30_NAME)

    @staticmethod
    def validate_phone(phone: str) -> bool:
        return Validator \
            .matches(phone, Validator.RegexCommons.PHONE_NUMBER)
