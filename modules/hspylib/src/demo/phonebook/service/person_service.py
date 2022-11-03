#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   demo.phonebook.service
      @file: person_service.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

from hspylib.core.datasource.crud_service import CrudService
from hspylib.core.datasource.sqlite.sqlite_configuration import SQLiteConfiguration
from phonebook.__classpath__ import _Classpath
from phonebook.entity.Person import Person
from phonebook.repository.person_repository import PersonRepository


class PersonService(CrudService[Person]):

    def __init__(self):
        cfg = SQLiteConfiguration(str(_Classpath.resource_dir()))
        repository = PersonRepository(cfg)
        super().__init__(repository)
