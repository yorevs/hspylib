#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   demo.phonebook.view
      @file: search_view.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

from typing import List

from hspylib.core.datasource.crud_entity import CrudEntity
from hspylib.core.exception.exceptions import InputAbortedError
from hspylib.core.metaclass.singleton import Singleton
from hspylib.core.tools.commons import sysout
from hspylib.core.tools.namespace import Namespace
from hspylib.modules.cli.tui.menu.menu_utils import MenuUtils
from hspylib.modules.cli.tui.table.table_renderer import TableRenderer
from phonebook.entity.Company import Company
from phonebook.entity.Person import Person
from phonebook.service.company_service import CompanyService
from phonebook.service.person_service import PersonService


class SearchView(metaclass=Singleton):

    def __init__(self) -> None:
        self.person_service = PersonService()
        self.company_service = CompanyService()

    def by_name(self) -> None:
        MenuUtils.title('SEARCH BY NAME')
        try:
            filters = Namespace(name=MenuUtils.prompt('Person or Company name'))
            all_persons = self.person_service.list(filters=filters)
            all_companies = self.company_service.list(filters=filters)
            self.display_contacts(all_persons, all_companies)
        except InputAbortedError:
            pass

    def by_uuid(self) -> None:
        MenuUtils.title('SEARCH BY UUID')
        try:
            filters = Namespace(uuid=MenuUtils.prompt('Person or Company uuid'))
            all_persons = self.person_service.list(filters=filters)
            all_companies = self.company_service.list(filters=filters)
            self.display_contacts(all_persons, all_companies)
        except InputAbortedError:
            pass

    def list_all(self) -> None:
        all_persons = self.person_service.list()
        all_companies = self.company_service.list()
        self.display_contacts(all_persons, all_companies)

    @staticmethod
    def display_contacts(persons: List[Person], companies: List[Company]) -> None:
        if persons or companies:
            SearchView.display_table(
                list(map(str.upper, Person.columns())), list(map(lambda p: p.values, persons)), 'PERSONS')
            SearchView.display_table(
                list(map(str.upper, Company.columns())), list(map(lambda c: c.values, companies)), 'COMPANIES')
        else:
            sysout('-=- No results to be displayed -=-')
            MenuUtils.wait_enter()

    @staticmethod
    def display_table(headers: List[str], entities: List[CrudEntity], title: str) -> None:
        MenuUtils.title(f"LISTING ALL {title}")
        tr = TableRenderer(headers, entities, title)
        tr.adjust_sizes_by_largest_cell()
        tr.render()
        MenuUtils.wait_enter()
