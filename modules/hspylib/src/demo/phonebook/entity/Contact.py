#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   demo.phonebook.entity
      @file: Contact.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

from uuid import UUID

from core.crud.crud_entity import CrudEntity


class Contact(CrudEntity):
    def __init__(
        self,
        uuid: UUID = None,
        name: str = None,
        phone: str = None,
        address: str = None,
        complement: str = None):
        super().__init__(uuid)
        self.name = name
        self.phone = phone
        self.address = address
        self.complement = complement
