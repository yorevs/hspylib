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

from typing import List, Tuple
from hspylib.core.tools.constants import RE_COMMON_2_30_NAME, RE_PHONE_NUMBER
from hspylib.core.tools.preconditions import check_argument, check_state
from hspylib.core.tools.validator import Validator
from phonebook.entity.Contact import Contact


class ContactValidator(Validator):

    def __call__(self, *contacts: Contact, **kwargs) -> Tuple[bool, List[dict]]:
        errors = []
        check_argument(len(contacts) == 1, f"Exactly one contact can be validated at a time. Given: {len(contacts)}")
        check_state(isinstance(contacts[0], Contact), "Only Contact can be validated")
        self.assert_valid(errors, self.validate_name(contacts[0].name))
        self.assert_valid(errors, self.validate_phone(contacts[0].phone))
        self.assert_valid(errors, self.validate_address(contacts[0].address))
        self.assert_valid(errors, self.validate_complement(contacts[0].complement))

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
