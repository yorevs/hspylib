from typing import List, Tuple

from hspylib.core.tools.validator import Validator
from phonebook.entity.Person import Person


class ContactValidator(Validator):

    def __call__(self, *contacts, **kwargs) -> Tuple[bool, List[dict]]:
        errors = []
        assert len(contacts) == 1, "Only one contact can be validated at a time"
        assert isinstance(contacts[0], Person), "Only contacts can be validated"
        assert self.validate_name(contacts[0].name), "Invalid name: {}".format(contacts[0].name)
        assert self.validate_phone(contacts[0].phone), "Invalid phone: {}".format(contacts[0].phone)

        return len(errors) == 0, errors

    @staticmethod
    def validate_name(name: str) -> (bool, str):
        return Validator \
            .matches(name, Validator.RegexCommons.COMMON_3_30_NAME), "Invalid name"

    @staticmethod
    def validate_phone(phone: str) -> (bool, str):
        return Validator \
            .matches(phone, Validator.RegexCommons.PHONE_NUMBER), "Invalid phone"

    @staticmethod
    def validate_address(address: str) -> (bool, str):
        return Validator.is_not_blank(address), "Invalid address"

    @staticmethod
    def validate_complement(complement: str) -> (bool, str):
        return Validator.is_not_blank(complement), "Invalid complement"
