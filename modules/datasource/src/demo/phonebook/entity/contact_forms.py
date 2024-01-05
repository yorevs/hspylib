#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib-Datasource
   @package: phonebook.entity
      @file: contact_forms.py
   @created: Thu, 22 Dec 2022
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright·(c)·2024,·HSPyLib
"""
from clitt.core.tui.minput.input_validator import InputValidator
from clitt.core.tui.minput.minput import MenuInput, minput
from hspylib.core.namespace import Namespace
from typing import Optional


class ContactForms:
    @staticmethod
    def person_form(
        name: str = None, age: int = None, phone: str = None, email: str = None, address: str = None, cpl: str = None
    ) -> Optional[Namespace]:
        # fmt: off
        form_fields = MenuInput.builder() \
            .field() \
                .label("Name") \
                .validator(InputValidator.words()) \
                .min_max_length(2, 60) \
                .value(name) \
                .build() \
            .field() \
                .label("Age") \
                .validator(InputValidator.numbers()) \
                .min_max_length(1, 3) \
                .value(age) \
                .build() \
            .field() \
                .label("Phone") \
                .validator(InputValidator.anything()) \
                .value(phone) \
                .build() \
            .field() \
                .label("Email") \
                .validator(InputValidator.anything()) \
                .value(email) \
                .build() \
            .field() \
                .label("Address") \
                .validator(InputValidator.anything()) \
                .value(address) \
                .build() \
            .field() \
                .label("Complement") \
                .validator(InputValidator.anything()) \
                .min_max_length(0, 60) \
                .value(cpl) \
                .build() \
            .build()
        # fmt: on
        return minput(form_fields, "Please fill the person form below")

    @staticmethod
    def company_form(
        name: str = None, cnpj: str = None, phone: str = None, website: str = None, address: str = None, cpl: str = None
    ) -> Namespace:
        # fmt: off
        form_fields = MenuInput.builder() \
            .field() \
                .label("Name") \
                .validator(InputValidator.words()) \
                .min_max_length(2, 60) \
                .value(name) \
                .build() \
                .field() \
            .label("CNPJ") \
                .itype("masked") \
                .value(f"{cnpj}|##.###.###/0001-##") \
                .build() \
                .field() \
            .label("Phone") \
                .validator(InputValidator.anything()) \
                .value(phone) \
                .build() \
                .field() \
            .label("WebSite") \
                .validator(InputValidator.anything()) \
                .value(website) \
                .min_max_length(6, 60) \
                .build() \
                .field() \
            .label("Address") \
                .validator(InputValidator.anything()) \
                .value(address) \
                .build() \
                .field() \
            .label("Complement") \
                .validator(InputValidator.anything()) \
                .min_max_length(0, 60) \
                .value(cpl) \
                .build() \
            .build()
        # fmt: on
        return minput(form_fields, "Please fill the person form below")
