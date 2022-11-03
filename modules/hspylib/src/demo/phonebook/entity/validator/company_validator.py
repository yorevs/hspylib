#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   demo.phonebook.entity.validator
      @file: company_validator.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

from typing import List, Tuple

from hspylib.core.constants import RE_URL, RE_CNPJ
from hspylib.core.preconditions import check_argument, check_state
from hspylib.core.tools.validator import Validator
from phonebook.entity.Company import Company
from phonebook.entity.validator.contact_validator import ContactValidator


class CompanyValidator(ContactValidator):

    def __call__(self, *companies: Company, **kwargs) -> Tuple[bool, List[dict]]:
        errors = []
        check_argument(len(companies) == 1, f"Exactly one company can be validated at a time. Given: {len(companies)}")
        check_state(isinstance(companies[0], Company), "Only Company can be validated")
        self.assert_valid(errors, self.validate_name(companies[0].name))
        self.assert_valid(errors, self.validate_cnpj(companies[0].cnpj))
        self.assert_valid(errors, self.validate_phone(companies[0].phone))
        self.assert_valid(errors, self.validate_website(companies[0].website))
        self.assert_valid(errors, self.validate_address(companies[0].address))
        self.assert_valid(errors, self.validate_complement(companies[0].complement))

        return len(errors) == 0, errors

    @staticmethod
    def validate_website(website: str) -> (bool, str):
        return Validator \
                   .matches(website, RE_URL), "Invalid website"

    @staticmethod
    def validate_cnpj(website: str) -> (bool, str):
        return Validator \
                   .matches(website, RE_CNPJ), "Invalid CNPJ"
