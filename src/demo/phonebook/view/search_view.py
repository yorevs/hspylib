#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.demo.phonebook.view
      @file: search_view.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

from typing import List

from hspylib.core.exception.exceptions import InputAbortedError
from hspylib.core.meta.singleton import Singleton
from hspylib.core.model.entity import Entity
from hspylib.core.tools.commons import sysout
from hspylib.modules.cli.menu.menu_utils import MenuUtils
from hspylib.modules.cli.tables.table_renderer import TableRenderer
from phonebook.service.company_service import CompanyService
from phonebook.service.person_service import PersonService


class SearchView(metaclass=Singleton):

    def __init__(self):
        self.person_service = PersonService()
        self.company_service = CompanyService()

    def by_name(self) -> None:
        MenuUtils.title('SEARCH BY NAME')
        try:
            name = MenuUtils.prompt('Person or Company name')
            all_persons = self.person_service.list(filters='name={}'.format(name))
            all_companies = self.company_service.list(filters='name={}'.format(name))
            self.display_contacts(all_persons, all_companies)
        except InputAbortedError:
            pass

    def by_uuid(self) -> None:
        MenuUtils.title('SEARCH BY UUID')
        try:
            name = MenuUtils.prompt('Person or Company uuid')
            all_persons = self.person_service.list(filters='uuid={}'.format(name))
            all_companies = self.company_service.list(filters='uuid={}'.format(name))
            self.display_contacts(all_persons, all_companies)
        except InputAbortedError:
            pass

    def list_all(self) -> None:
        all_persons = self.person_service.list()
        all_companies = self.company_service.list()
        self.display_contacts(all_persons, all_companies)

    @staticmethod
    def display_contacts(persons, companies) -> None:
        if len(persons) > 0 or len(companies) > 0:
            SearchView.display_table(
                ["UUID", "NAME", "PHONE", "ADDRESS", "CPL", "AGE", "EMAIL"], persons, 'PERSONS')
            SearchView.display_table(
                ["UUID", "NAME", "PHONE", "ADDRESS", "CPL", "WEBSITE"], companies, 'COMPANIES')
        else:
            sysout('-=- No results to be displayed -=-')
            MenuUtils.wait_enter()

    @staticmethod
    def display_table(headers: List[str], entities: List[Entity], title: str) -> None:
        MenuUtils.title('LISTING ALL {}'.format(title))
        tr = TableRenderer(headers, [c.to_values() for c in entities], title)
        tr.adjust_sizes_by_largest_cell()
        tr.render()
        MenuUtils.wait_enter()
