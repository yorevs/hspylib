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
from hspylib.core.tools.commons import syserr

from phonebook.entity.contact_forms import ContactForms
from phonebook.service.company_service import CompanyService
from phonebook.service.person_service import PersonService


class EditView(metaclass=Singleton):
    def __init__(self) -> None:
        self.person_service = PersonService()
        self.company_service = CompanyService()

    def person(self) -> None:
        uuid = MenuUtils.prompt("uuid")
        if not uuid:
            return
        found = self.person_service.get(uuid)
        if not found:
            syserr("Person does not exist", uuid)
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

    def company(self) -> None:
        uuid = MenuUtils.prompt("uuid")
        if not uuid:
            return
        found = self.company_service.get(uuid)
        if not found:
            syserr("Company does not exist", uuid)
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
