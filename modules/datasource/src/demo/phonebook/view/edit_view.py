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
from hspylib.core.metaclass.singleton import Singleton
from hspylib.modules.cli.tui.menu.menu_utils import MenuUtils

from phonebook.entity.validator.contact_validator import ContactValidator
from phonebook.service.company_service import CompanyService
from phonebook.service.person_service import PersonService


class EditView(metaclass=Singleton):
    def __init__(self) -> None:
        self.person_service = PersonService()
        self.company_service = CompanyService()

    def person(self) -> None:
        uuid = MenuUtils.prompt("Enter uid", ContactValidator.validate_name)
        found = self.person_service.get(uuid)
        if not found:
            MenuUtils.print_error("Person does not exist", uuid)
        else:
            found.name = MenuUtils.prompt("Name", ContactValidator.validate_name)
            found.age = MenuUtils.prompt("Age", ContactValidator.validate_name)
            found.phone = MenuUtils.prompt("Phone", ContactValidator.validate_name)
            found.email = MenuUtils.prompt("Email", ContactValidator.validate_name)
            found.address = MenuUtils.prompt("Address", ContactValidator.validate_name)
            found.complement = MenuUtils.prompt("Complement", ContactValidator.validate_name)
            self.person_service.save(found)
            MenuUtils.wait_enter()

    def company(self) -> None:
        uuid = MenuUtils.prompt("Enter uid", ContactValidator.validate_name)
        found = self.company_service.get(uuid)
        if not found:
            MenuUtils.print_error("Company does not exist", uuid)
        else:
            found.name = MenuUtils.prompt("Name", ContactValidator.validate_name)
            found.phone = MenuUtils.prompt("Phone", ContactValidator.validate_name)
            found.website = MenuUtils.prompt("WebSite", ContactValidator.validate_name)
            found.address = MenuUtils.prompt("Address", ContactValidator.validate_name)
            found.complement = MenuUtils.prompt("Complement", ContactValidator.validate_name)
            self.company_service.save(found)
            MenuUtils.wait_enter()
