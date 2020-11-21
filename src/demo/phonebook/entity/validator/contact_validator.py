from typing import List, Tuple

from hspylib.core.tools.regex_commons import RegexCommons
from hspylib.core.tools.validator import Validator
from phonebook.entity.contact import Contact
from phonebook.entity.person import Person


class ContactValidator(Validator):

    def __call__(self, *contacts: Contact, **kwargs) -> Tuple[bool, List[dict]]:
        errors = []
        assert len(contacts) == 1, "Exactly one contact can be validated at a time. Given: {}".format(len(contacts))
        assert isinstance(contacts[0], Person), "Only contacts can be validated"
        self.assert_valid(errors, self.validate_name(contacts[0].name))
        self.assert_valid(errors, self.validate_phone(contacts[0].phone))
        self.assert_valid(errors, self.validate_address(contacts[0].address))
        self.assert_valid(errors, self.validate_complement(contacts[0].complement))

        return len(errors) == 0, errors

    @staticmethod
    def validate_name(name: str) -> (bool, str):
        return Validator \
            .matches(name, RegexCommons.COMMON_3_30_NAME), "Invalid name"

    @staticmethod
    def validate_phone(phone: str) -> (bool, str):
        return Validator \
            .matches(phone, RegexCommons.PHONE_NUMBER), "Invalid phone"

    @staticmethod
    def validate_address(address: str) -> (bool, str):
        return Validator.is_not_blank(address), "Invalid password"

    @staticmethod
    def validate_complement(complement: str) -> (bool, str):
        return Validator.is_not_blank(complement), "Invalid complement"
