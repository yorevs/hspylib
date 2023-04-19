#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib-Datasource
   @package: phonebook.view
      @file: edit_view.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""
from clitt.core.tui.menu.tui_menu import TUIMenu
from clitt.core.tui.menu.tui_menu_ui import TUIMenuUi
from clitt.core.tui.menu.tui_menu_view import TUIMenuView
from clitt.core.tui.minput.input_validator import InputValidator
from clitt.core.tui.minput.minput import MenuInput, minput
from hspylib.core.namespace import Namespace
from hspylib.core.tools.commons import syserr

from datasource.identity import Identity
from phonebook.entity.contact_forms import ContactForms
from phonebook.service.company_service import CompanyService
from phonebook.service.person_service import PersonService


class EditView(TUIMenuView):

    @classmethod
    def prompt(
        cls,
        label: str,
        dest: str = None,
        min_length: int = 1,
        max_length: int = 32) -> Namespace:
        # fmt: off
        form_fields = MenuInput.builder() \
            .field() \
                .label(label) \
                .dest(dest or label) \
                .validator(InputValidator.words(min_length, max_length)) \
                .min_max_length(min_length, max_length) \
                .build() \
            .build()
        # fmt: on
        ret_val = minput(form_fields)
        TUIMenuUi.render_app_title()
        return ret_val

    def __init__(self, parent: TUIMenu) -> None:
        super().__init__(parent)
        self.person_service = PersonService()
        self.company_service = CompanyService()

    def person(self) -> None:
        uuid = self.prompt("uuid")
        if not uuid:
            return
        found = self.person_service.get(Identity(uuid))
        if not found:
            syserr(f"Person does not exist: uuid={uuid.uuid}")
            TUIMenu.wait_keystroke()
        else:
            form = ContactForms.person_form(
                found.name, found.age, found.phone, found.email, found.address, found.complement)
            if form:
                found.name = form.name
                found.age = form.age
                found.phone = form.phone
                found.email = form.email
                found.address = form.address
                found.complement = form.complement
                self.person_service.save(found)
                TUIMenuUi.render_app_title()
                TUIMenu.wait_keystroke("Person successfully saved!%EOL%")

    def company(self) -> None:
        uuid = self.prompt("uuid")
        if not uuid:
            return
        found = self.company_service.get(Identity(uuid))
        if not found:
            syserr(f"Company does not exist: uuid={uuid.uuid}")
            TUIMenu.wait_keystroke()
        else:
            form = ContactForms.company_form(
                found.name, found.cnpj, found.phone, found.website, found.address, found.complement)
            if form:
                found.name = form.name
                found.cnpj = form.cnpj
                found.phone = form.phone
                found.website = form.website
                found.address = form.address
                found.complement = form.complement
                self.company_service.save(found)
                TUIMenuUi.render_app_title()
                TUIMenu.wait_keystroke("Company successfully saved!%EOL%")
