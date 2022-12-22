#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib-Datasource
   @package: phonebook.service
      @file: company_service.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

from datasource.crud_service import CrudService
from datasource.db_configuration import DBConfiguration
from phonebook.__classpath__ import _Classpath
from phonebook.entity.company import Company
from phonebook.repository.company_repository import CompanyRepository


class CompanyService(CrudService[CompanyRepository, Company]):
    def __init__(self) -> None:
        cfg = DBConfiguration(str(_Classpath.resource_path()))
        repository = CompanyRepository(cfg)
        super().__init__(repository)
