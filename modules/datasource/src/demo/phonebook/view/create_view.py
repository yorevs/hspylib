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
from hspylib.core.metaclass.singleton import Singleton
from hspylib.core.namespace import Namespace
from hspylib.modules.cli.tui.minput.input_validator import InputValidator
from hspylib.modules.cli.tui.minput.minput import minput, MenuInput
from hspylib.modules.cli.tui.menu.menu_utils import MenuUtils
from hspylib.modules.cli.vt100.vt_utils import clear_screen

from datasource.identity import Identity
from phonebook.entity.Company import Company
from phonebook.entity.Person import Person
from phonebook.entity.validator.contact_validator import ContactValidator
from phonebook.service.company_service import CompanyService
from phonebook.service.person_service import PersonService


class CreateView(metaclass=Singleton):
    """ TODO"""

    @staticmethod
    def person_form() -> Namespace:
        # fmt: off
        form_fields = MenuInput.builder() \
            .field() \
                .label("Name") \
                .validator(InputValidator.letters()) \
                .build() \
            .field() \
                .label("Age") \
                .validator(InputValidator.numbers()) \
                .build() \
            .field() \
                .label("Phone") \
                .validator(InputValidator.anything()) \
                .build() \
            .field() \
                .label("Email") \
                .validator(InputValidator.anything()) \
                .build() \
            .field() \
                .label("Address") \
                .validator(InputValidator.anything()) \
                .build() \
            .field() \
                .label("Complement") \
                .validator(InputValidator.numbers()) \
                .build() \
            .build()
        # fmt: on
        return minput(form_fields, 'Please fill the person form below')

    @staticmethod
    def company_form() -> Namespace:
        # fmt: off
        form_fields = MenuInput.builder() \
            .field() \
                .label("Name") \
                .validator(InputValidator.letters()) \
                .build() \
                .field() \
            .label("CNPJ") \
                .validator(InputValidator.anything()) \
                .build() \
                .field() \
            .label("Phone") \
                .validator(InputValidator.anything()) \
                .build() \
                .field() \
            .label("WebSite") \
                .validator(InputValidator.anything()) \
                .build() \
                .field() \
            .label("Address") \
                .validator(InputValidator.anything()) \
                .build() \
                .field() \
            .label("Complement") \
                .validator(InputValidator.numbers()) \
                .build() \
            .build()
        # fmt: on
        return minput(form_fields, 'Please fill the person form below')

    def __init__(self) -> None:
        self.person_service = PersonService()
        self.company_service = CompanyService()

    def person(self) -> None:
        form = self.person_form()
        if form:
            person = Person(Identity.auto())
            person.name = form.name
            person.age = form.age
            person.phone = form.phone
            person.email = form.email
            person.address = form.address
            person.complement = form.complement
            self.person_service.save(person)

    def company(self) -> None:
        form = self.company_form()
        if form:
            company = Company(Identity.auto())
            company.uuid = form.uuid
            company.name = form.name
            company.cnpj = form.cnpj
            company.phone = form.phone
            company.website = form.website
            company.address = form.address
            company.complement = form.complement
            self.company_service.save(company)
