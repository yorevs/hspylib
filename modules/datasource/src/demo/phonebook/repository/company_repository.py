#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib-Datasource
   @package: phonebook.repository
      @file: company_repository.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright·(c)·2024,·HSPyLib
"""
from datasource.db_configuration import DBConfiguration
from datasource.sqlite.sqlite_repository import SQLiteRepository
from phonebook.entity.company import Company


class CompanyRepository(SQLiteRepository[Company]):
    def __init__(self, config: DBConfiguration):
        super().__init__(config)

    def table_name(self) -> str:
        return "COMPANIES"

    def to_entity_type(self, entity_dict: dict | tuple) -> Company:
        return Company.from_tuple(entity_dict)
