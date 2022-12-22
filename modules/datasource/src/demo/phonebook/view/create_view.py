#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib-Datasource
   @package: phonebook.view
      @file: create_view.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
from hspylib.modules.cli.tui.menu.tui_menu import TUIMenu
from hspylib.modules.cli.tui.menu.tui_menu_utils import TUIMenuUtils
from hspylib.modules.cli.tui.menu.tui_menu_view import TUIMenuView

from datasource.identity import Identity
from phonebook.entity.company import Company
from phonebook.entity.contact_forms import ContactForms
from phonebook.entity.person import Person
from phonebook.service.company_service import CompanyService
from phonebook.service.person_service import PersonService


class CreateView(TUIMenuView):
    """ TODO"""

    def __init__(self, parent: TUIMenu) -> None:
        super().__init__(parent)
        self.person_service = PersonService()
        self.company_service = CompanyService()

    def person(self) -> None:
        form = ContactForms.person_form()
        if form:
            person = Person(Identity.auto(field_name='uuid'))
            person.name = form.name
            person.age = form.age
            person.phone = form.phone
            person.email = form.email
            person.address = form.address
            person.complement = form.complement
            self.person_service.save(person)
            TUIMenuUtils.render_app_title()
            TUIMenuUtils.wait_keystroke("Person successfully saved!%EOL%")

    def company(self) -> None:
        form = ContactForms.company_form()
        if form:
            company = Company(Identity.auto(field_name='uuid'))
            company.uuid = form.uuid
            company.name = form.name
            company.cnpj = form.cnpj
            company.phone = form.phone
            company.website = form.website
            company.address = form.address
            company.complement = form.complement
            self.company_service.save(company)
            TUIMenuUtils.render_app_title()
            TUIMenuUtils.wait_keystroke("Company successfully saved!%EOL%")
