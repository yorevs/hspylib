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

   Copyright 2021, HSPyLib team
"""

from core.config.app_config import AppConfigs
from core.crud.file.file_repository import FileRepository

from phonebook.entity.Company import Company


class CompanyRepository(FileRepository):

    def __init__(self):
        self.db_file = "{}/db/{}".format(
            AppConfigs.INSTANCE.resource_dir(),
            AppConfigs.INSTANCE["phonebook.entries.db.file"]
        )
        super().__init__(self.db_file)

    def dict_to_entity(self, row: dict) -> Company:
        return Company(
            row['uuid'],
            row['name'],
            row['phone'],
            row['website'],
            row['address'],
            row['complement'])
