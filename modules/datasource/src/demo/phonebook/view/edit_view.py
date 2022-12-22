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
from hspylib.modules.cli.tui.menu.tui_menu_utils import TUIMenuUtils
from hspylib.modules.cli.tui.menu.tui_menu_view import TUIMenuView
from hspylib.core.tools.commons import syserr, sysout

from phonebook.entity.contact_forms import ContactForms
from phonebook.service.company_service import CompanyService
from phonebook.service.person_service import PersonService


class EditView(TUIMenuView):
    def __init__(self) -> None:
        self.person_service = PersonService()
        self.company_service = CompanyService()

    def person(self) -> None:
        uuid = TUIMenuUtils.prompt("uuid")
        if not uuid:
            return
        found = self.person_service.get(uuid)
        if not found:
            syserr("Person does not exist", uuid)
            TUIMenuUtils.wait_keystroke()
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
                TUIMenuUtils.render_app_title()
                sysout("Person successfully saved!%EOL%")
                TUIMenuUtils.wait_keystroke()

    def company(self) -> None:
        uuid = TUIMenuUtils.prompt("uuid")
        if not uuid:
            return
        found = self.company_service.get(uuid)
        if not found:
            syserr("Company does not exist", uuid)
            TUIMenuUtils.wait_keystroke()
        else:
            form = ContactForms.company_form(
                found.name, found.age, found.phone, found.email, found.address, found.complement)
            if form:
                found.name = form.name
                found.phone = form.phone
                found.website = form.website
                found.address = form.address
                found.complement = form.complement
                self.company_service.save(found)
                TUIMenuUtils.render_app_title()
                sysout("Company successfully saved!%EOL%")
                TUIMenuUtils.wait_keystroke()
