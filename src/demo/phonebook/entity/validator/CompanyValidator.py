from typing import List

from hspylib.core.tools.validator import Validator
from phonebook.entity.Person import Person


class CompanyValidator(Validator):

    def __call__(self, *persons, **kwargs) -> List[dict]:
        errors = []
        assert len(persons) == 1, "One person exactly is required to validate"
        assert isinstance(persons[0], Person), "Can only validate Person entities"

        return errors

    @staticmethod
    def validate_website(website: str) -> bool:
        return Validator \
            .matches(website, Validator.RegexCommons.URL)
