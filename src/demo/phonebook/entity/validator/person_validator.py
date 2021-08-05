#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   hspylib.demo.phonebook.entity.validator
      @file: person_validator.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

from typing import List, Tuple
from hspylib.core.tools.constants import RE_EMAIL_W3C
from hspylib.core.tools.preconditions import check_argument, check_state
from hspylib.core.tools.validator import Validator
from phonebook.entity.Person import Person
from phonebook.entity.validator.contact_validator import ContactValidator



class PersonValidator(ContactValidator):

    def __call__(self, *persons: Person, **kwargs) -> Tuple[bool, List[dict]]:
        errors = []
        check_argument(len(persons) == 1, f"Exactly one person can be validated at a time. Given: {len(persons)}")
        check_state(isinstance(persons[0], Person), "Only Person can be validated")
        self.assert_valid(errors, self.validate_name(persons[0].name))
        self.assert_valid(errors, self.validate_age(str(persons[0].age)))
        self.assert_valid(errors, self.validate_phone(persons[0].phone))
        self.assert_valid(errors, self.validate_email(persons[0].email))
        self.assert_valid(errors, self.validate_address(persons[0].address))
        self.assert_valid(errors, self.validate_complement(persons[0].complement))

        return len(errors) == 0, errors

    @staticmethod
    def validate_age(age: str) -> (bool, str):
        return Validator.is_integer(age, min_value=10, max_value=115), "Invalid age"

    @staticmethod
    def validate_email(email: str) -> (bool, str):
        return Validator \
                   .matches(email, RE_EMAIL_W3C), "Invalid email"
