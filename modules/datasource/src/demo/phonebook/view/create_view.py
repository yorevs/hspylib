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
from hspylib.modules.cli.tui.menu.menu_utils import MenuUtils

from datasource.identity import Identity
from phonebook.entity.Company import Company
from phonebook.entity.Person import Person
from phonebook.entity.validator.company_validator import CompanyValidator
from phonebook.entity.validator.contact_validator import ContactValidator
from phonebook.entity.validator.person_validator import PersonValidator
from phonebook.service.company_service import CompanyService
from phonebook.service.person_service import PersonService


class CreateView(metaclass=Singleton):

    def __init__(self) -> None:
        self.person_service = PersonService()
        self.company_service = CompanyService()

    def person(self) -> None:
        MenuUtils.title('CREATE PERSON')
        person = Person(Identity.auto())
        try:
            person.uuid = person.identity.values
            person.name = MenuUtils.prompt('Name', ContactValidator.validate_name)
            person.age = MenuUtils.prompt('Age', PersonValidator.validate_age)
            person.phone = MenuUtils.prompt('Phone', ContactValidator.validate_phone)
            person.email = MenuUtils.prompt('Email', PersonValidator.validate_email)
            person.address = MenuUtils.prompt(
                'Address', on_blank_abort=False, validator=ContactValidator.validate_address)
            person.complement = MenuUtils.prompt(
                'Complement', on_blank_abort=False, validator=ContactValidator.validate_complement)
            self.person_service.save(person)
        except InputAbortedError:
            MenuUtils.wait_enter('Operation aborted. Press [Enter]...')

        MenuUtils.wait_enter()

    def company(self) -> None:
        MenuUtils.title('CREATE COMPANY')
        company = Company(Identity.auto())
        try:
            company.uuid = company.identity.values
            company.name = MenuUtils.prompt('Name', ContactValidator.validate_name)
            company.cnpj = MenuUtils.prompt('CNPJ', CompanyValidator.validate_cnpj)
            company.phone = MenuUtils.prompt('Phone', ContactValidator.validate_phone)
            company.website = MenuUtils.prompt('WebSite', CompanyValidator.validate_website)
            company.address = MenuUtils.prompt(
                'Address', on_blank_abort=False, validator=ContactValidator.validate_address)
            company.complement = MenuUtils.prompt(
                'Complement', on_blank_abort=False, validator=ContactValidator.validate_complement)
            self.company_service.save(company)
        except InputAbortedError:
            MenuUtils.wait_enter('Operation aborted. Press [Enter]...')

        MenuUtils.wait_enter()
