from typing import List, Tuple

from hspylib.core.tools.validator import Validator
from phonebook.entity.Company import Company
from phonebook.entity.validator.ContactValidator import ContactValidator


class CompanyValidator(ContactValidator):

    def __call__(self, *companies, **kwargs) -> Tuple[bool, List[dict]]:
        errors = []
        assert len(companies) == 1, "Only one company can be validated at a time"
        assert isinstance(companies[0], Company), "Only companies can be validated"
        assert self.validate_website(companies[0].website), "Invalid website: {}".format(companies[0].website)
        super().__call__(companies, kwargs)

        return len(errors) == 0, errors

    @staticmethod
    def validate_website(website: str) -> (bool, str):
        return Validator \
            .matches(website, Validator.RegexCommons.URL), "Invalid website"
