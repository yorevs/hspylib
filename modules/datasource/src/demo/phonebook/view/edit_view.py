#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib-Datasource
   @package: phonebook.view
      @file: edit_view.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright·(c)·2024,·HSPyLib
"""
from clitt.core.tui.menu.tui_menu import TUIMenu
from clitt.core.tui.menu.tui_menu_ui import TUIMenuUi
from clitt.core.tui.menu.tui_menu_view import TUIMenuView
from datasource.identity import Identity
from hspylib.core.tools.commons import syserr
from phonebook.entity.contact_forms import ContactForms
from phonebook.service.company_service import CompanyService
from phonebook.service.person_service import PersonService


class EditView(TUIMenuView):
    def __init__(self, parent: TUIMenu) -> None:
        super().__init__(parent)
        self.person_service = PersonService()
        self.company_service = CompanyService()

    def person(self) -> None:
        if not (uuid := self.prompt("uuid")):
            return
        if not (found := self.person_service.get(Identity(uuid))):
            syserr(f"Person does not exist: uuid={uuid.uuid}")
            self.wait_keystroke()
        else:
            form = ContactForms.person_form(
                found.name, found.age, found.phone, found.email, found.address, found.complement
            )
            if form:
                found.name = form.name
                found.age = form.age
                found.phone = form.phone
                found.email = form.email
                found.address = form.address
                found.complement = form.complement
                self.person_service.save(found)
                TUIMenuUi.render_app_title()
                self.wait_keystroke("Person successfully saved!%EOL%")

    def company(self) -> None:
        if not (uuid := self.prompt("uuid")):
            return
        if not (found := self.company_service.get(Identity(uuid))):
            syserr(f"Company does not exist: uuid={uuid.uuid}")
            self.wait_keystroke()
        else:
            form = ContactForms.company_form(
                found.name, found.cnpj, found.phone, found.website, found.address, found.complement
            )
            if form:
                found.name = form.name
                found.cnpj = form.cnpj
                found.phone = form.phone
                found.website = form.website
                found.address = form.address
                found.complement = form.complement
                self.company_service.save(found)
                TUIMenuUi.render_app_title()
                self.wait_keystroke("Company successfully saved!%EOL%")
