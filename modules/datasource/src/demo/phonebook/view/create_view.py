#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   demo.phonebook.view
      @file: create_view.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
from hspylib.core.exception.exceptions import InputAbortedError
from hspylib.core.metaclass.singleton import Singleton

from datasource.identity import Identity
from phonebook.entity.Company import Company
from phonebook.entity.Person import Person
from phonebook.entity.validator.contact_validator import ContactValidator
from phonebook.service.company_service import CompanyService
from phonebook.service.person_service import PersonService
from phonebook.view.menu_utils import MenuUtils


class CreateView(metaclass=Singleton):
    def __init__(self) -> None:
        self.person_service = PersonService()
        self.company_service = CompanyService()

    def person(self) -> None:
        MenuUtils.title("CREATE PERSON")
        person = Person(Identity.auto())
        try:
            person.uuid = person.identity.values
            person.name = MenuUtils.prompt("Name", ContactValidator.validate_name)
            person.age = MenuUtils.prompt("Age", ContactValidator.validate_name)
            person.phone = MenuUtils.prompt("Phone", ContactValidator.validate_name)
            person.email = MenuUtils.prompt("Email", ContactValidator.validate_name)
            person.address = MenuUtils.prompt("Address", ContactValidator.validate_name)
            person.complement = MenuUtils.prompt("Complement", ContactValidator.validate_name)
            self.person_service.save(person)
        except InputAbortedError:
            pass

    def company(self) -> None:
        MenuUtils.title("CREATE COMPANY")
        company = Company(Identity.auto())
        try:
            company.uuid = company.identity.values
            company.name = MenuUtils.prompt("Name", ContactValidator.validate_name)
            company.cnpj = MenuUtils.prompt("CNPJ", ContactValidator.validate_name)
            company.phone = MenuUtils.prompt("Phone", ContactValidator.validate_name)
            company.website = MenuUtils.prompt("WebSite", ContactValidator.validate_name)
            company.address = MenuUtils.prompt("Address", ContactValidator.validate_name)
            company.complement = MenuUtils.prompt("Complement", ContactValidator.validate_name)
            self.company_service.save(company)
        except InputAbortedError:
            pass
