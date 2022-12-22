#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @Package: demo.phonebook.entity
      @file: company.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
from collections import namedtuple
from typing import List, Tuple

from datasource.crud_entity import CrudEntity
from datasource.identity import Identity


class Company(CrudEntity):

    CompanyId = namedtuple("CompanyId", ["uuid"])

    @staticmethod
    def columns() -> List[str]:
        return ["uuid", "cnpj", "name", "website", "phone", "address", "complement"]

    @classmethod
    def from_tuple(cls, values: Tuple) -> "Company":
        row = {k: v for k, v in zip(cls.columns(), values)}
        return Company(Identity(cls.CompanyId(row["uuid"])), **row)
