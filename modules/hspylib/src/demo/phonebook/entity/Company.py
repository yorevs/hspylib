#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   demo.phonebook.entity
      @file: Company.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

from uuid import UUID
from phonebook.entity.Contact import Contact


class Company(Contact):
    def __init__(
        self,
        uuid: UUID = None,
        name: str = None,
        phone: str = None,
        website: str = None,
        address: str = None,
        complement: str = None):
        super().__init__(uuid, name, phone, address, complement)
        self.website = website
