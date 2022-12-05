#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   demo.phonebook.repository
      @file: company_repository.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
from datasource.db_configuration import DBConfiguration
from datasource.sqlite.sqlite_repository import SQLiteRepository
from phonebook.entity.Company import Company


class CompanyRepository(SQLiteRepository[Company]):

    def __init__(self, config: DBConfiguration):
        super().__init__(config)

    def table_name(self) -> str:
        return 'COMPANIES'

    def to_entity_type(self, entity_dict: dict | tuple) -> Company:
        return Company.from_tuple(entity_dict)
