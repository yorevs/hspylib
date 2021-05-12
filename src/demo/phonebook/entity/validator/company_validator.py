#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.demo.phonebook.entity.validator
      @file: company_validator.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

from typing import List, Tuple

from hspylib.core.tools.regex_constants import RegexConstants
from hspylib.core.tools.validator import Validator
from phonebook.entity.Company import Company
from phonebook.entity.validator.contact_validator import ContactValidator


class CompanyValidator(ContactValidator):
    
    def __call__(self, *companies: Company, **kwargs) -> Tuple[bool, List[dict]]:
        errors = []
        assert len(companies) == 1, "Exactly one company can be validated at a time. Given: {}".format(len(companies))
        assert isinstance(companies[0], Company), "Only companies can be validated"
        self.assert_valid(errors, self.validate_name(companies[0].name))
        self.assert_valid(errors, self.validate_phone(companies[0].phone))
        self.assert_valid(errors, self.validate_website(companies[0].website))
        self.assert_valid(errors, self.validate_address(companies[0].address))
        self.assert_valid(errors, self.validate_complement(companies[0].complement))
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_website(website: str) -> (bool, str):
        return Validator \
                   .matches(website, RegexConstants.URL), "Invalid website"
