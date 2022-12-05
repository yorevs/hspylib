#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   demo.phonebook.entity.validator
      @file: contact_validator.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

from typing import List, Tuple, TypeVar, Union

from hspylib.core.constants import RE_COMMON_2_30_NAME, RE_PHONE_NUMBER
from hspylib.core.tools.validator import Validator

from phonebook.entity.Company import Company
from phonebook.entity.Person import Person

Contact = TypeVar('Contact', bound=Union[Person, Company])


class ContactValidator(Validator):

    def __call__(self, *contacts: Contact, **kwargs) -> Tuple[bool, List[dict]]:
        errors = []
        for contact in contacts:
            self.assert_valid(errors, self.validate_name(contact.name))
            self.assert_valid(errors, self.validate_phone(contact.phone))
            self.assert_valid(errors, self.validate_address(contact.address))
            self.assert_valid(errors, self.validate_complement(contact.complement))

        return len(errors) == 0, errors

    @staticmethod
    def validate_name(name: str) -> (bool, str):
        return Validator \
                   .matches(name, RE_COMMON_2_30_NAME), "Invalid name"

    @staticmethod
    def validate_phone(phone: str) -> (bool, str):
        return Validator \
                   .matches(phone, RE_PHONE_NUMBER), "Invalid phone"

    @staticmethod
    def validate_address(address: str) -> (bool, str):
        return Validator.is_not_blank(address), "Invalid password"

    @staticmethod
    def validate_complement(complement: str) -> (bool, str):
        return Validator.is_not_blank(complement), "Invalid complement"
