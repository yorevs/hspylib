#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   demo.phonebook.view
      @file: edit_view.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
from hspylib.core.exception.exceptions import InputAbortedError
from hspylib.core.metaclass.singleton import Singleton
from hspylib.modules.cli.tui.menu.menu_utils import MenuUtils

from phonebook.entity.validator.company_validator import CompanyValidator
from phonebook.entity.validator.contact_validator import ContactValidator
from phonebook.entity.validator.person_validator import PersonValidator
from phonebook.service.company_service import CompanyService
from phonebook.service.person_service import PersonService


class EditView(metaclass=Singleton):

    def __init__(self) -> None:
        self.person_service = PersonService()
        self.company_service = CompanyService()

    def person(self) -> None:
        MenuUtils.title('EDIT PERSON')
        uuid = MenuUtils.prompt('Enter uid')
        found = self.person_service.get(uuid)
        if not found:
            MenuUtils.print_error("Person does not exist", uuid)
        else:
            try:
                found.name = MenuUtils.prompt('Name', ContactValidator.validate_name, found.name)
                found.age = MenuUtils.prompt('Age', PersonValidator.validate_age, found.age)
                found.phone = MenuUtils.prompt('Phone', ContactValidator.validate_phone, found.phone)
                found.email = MenuUtils.prompt('Email', PersonValidator.validate_email, found.email)
                found.address = MenuUtils.prompt(
                    'Address', on_blank_abort=False, validator=ContactValidator.validate_address)
                found.complement = MenuUtils.prompt(
                    'Complement', on_blank_abort=False, validator=ContactValidator.validate_complement)
                self.person_service.save(found)
            except InputAbortedError:
                MenuUtils.wait_enter('Operation aborted. Press [Enter]...')

            MenuUtils.wait_enter()

    def company(self) -> None:
        MenuUtils.title('EDIT COMPANY')
        uuid = MenuUtils.prompt('Enter uid')
        found = self.company_service.get(uuid)
        if not found:
            MenuUtils.print_error("Company does not exist", uuid)
        else:
            try:
                found.name = MenuUtils.prompt('Name', ContactValidator.validate_name, found.name)
                found.phone = MenuUtils.prompt('Phone', ContactValidator.validate_phone, found.phone)
                found.website = MenuUtils.prompt('WebSite', CompanyValidator.validate_website, found.website)
                found.address = MenuUtils.prompt(
                    'Address', on_blank_abort=False, validator=ContactValidator.validate_address)
                found.complement = MenuUtils.prompt(
                    'Complement', on_blank_abort=False, validator=ContactValidator.validate_complement)
                self.company_service.save(found)
            except InputAbortedError:
                MenuUtils.wait_enter('Operation aborted. Press [Enter]...')

            MenuUtils.wait_enter()
