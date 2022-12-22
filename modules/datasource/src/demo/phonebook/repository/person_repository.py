#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @Package: demo.phonebook.repository
      @file: person_repository.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
from datasource.db_configuration import DBConfiguration
from datasource.sqlite.sqlite_repository import SQLiteRepository
from phonebook.entity.person import Person


class PersonRepository(SQLiteRepository[Person]):
    def __init__(self, config: DBConfiguration):
        super().__init__(config)

    def table_name(self) -> str:
        return "PERSONS"

    def to_entity_type(self, entity_dict: dict | tuple) -> Person:
        return Person.from_tuple(entity_dict)
