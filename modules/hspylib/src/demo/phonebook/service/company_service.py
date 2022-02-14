#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   demo.phonebook.service
      @file: company_service.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

from core.crud.crud_service import CrudService
from core.metaclass.singleton import Singleton

from phonebook.repository.company_repository import CompanyRepository


class CompanyService(CrudService, metaclass=Singleton):

    def __init__(self):
        self.repository = CompanyRepository()
        super().__init__(self.repository)
