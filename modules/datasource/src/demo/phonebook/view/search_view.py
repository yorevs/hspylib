#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: demo.phonebook.view
      @file: search_view.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

from typing import List

from hspylib.core.namespace import Namespace
from hspylib.modules.cli.tui.menu.tui_menu import TUIMenu
from hspylib.modules.cli.tui.menu.tui_menu_utils import TUIMenuUtils
from hspylib.modules.cli.tui.menu.tui_menu_view import TUIMenuView
from hspylib.modules.cli.tui.table.table_renderer import TableRenderer

from datasource.crud_entity import CrudEntity
from phonebook.entity.company import Company
from phonebook.entity.person import Person
from phonebook.service.company_service import CompanyService
from phonebook.service.person_service import PersonService


class SearchView(TUIMenuView):
    def __init__(self, parent: TUIMenu) -> None:
        super().__init__(parent)
        self.person_service = PersonService()
        self.company_service = CompanyService()

    def by_name(self) -> None:
        contact = TUIMenuUtils.prompt('Person or Company name', dest='name')
        if contact:
            filters = Namespace(uuid=f"name='{contact.name}'")
            all_persons = self.person_service.list(filters=filters)
            all_companies = self.company_service.list(filters=filters)
            self.display_contacts(all_persons, all_companies)

    def by_uuid(self) -> None:
        contact = TUIMenuUtils.prompt('Person or Company uuid', dest='uuid')
        if contact:
            filters = Namespace(uuid=f"uuid='{contact.uuid}'")
            all_persons = self.person_service.list(filters=filters)
            all_companies = self.company_service.list(filters=filters)
            self.display_contacts(all_persons, all_companies)

    def list_all(self) -> None:
        all_persons = self.person_service.list()
        all_companies = self.company_service.list()
        self.display_contacts(all_persons, all_companies)

    @staticmethod
    def display_contacts(persons: List[Person], companies: List[Company]) -> None:
        TUIMenuUtils.render_app_title()
        if persons:
            SearchView.display_table(
                list(map(str.upper, Person.columns())), list(map(lambda p: p.values, persons)), "PERSONS"
            )
            TUIMenuUtils.wait_keystroke()
        if companies:
            SearchView.display_table(
                list(map(str.upper, Company.columns())), list(map(lambda c: c.values, companies)), "COMPANIES"
            )
            TUIMenuUtils.wait_keystroke()
        if not persons and not companies:
            TUIMenuUtils.wait_keystroke("-=- No results to be displayed -=-%EOL%")

    @staticmethod
    def display_table(headers: List[str], entities: List[CrudEntity], title: str) -> None:
        tr = TableRenderer(headers, entities, title)
        tr.adjust_sizes_by_largest_cell()
        tr.render()
