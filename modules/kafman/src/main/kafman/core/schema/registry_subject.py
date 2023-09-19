#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
      @file: registry_subject.py
   @created: Thu, 5 Aug 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
import json


class RegistrySubject:
    """Represent a schema registry subject"""

    def __init__(
        self,
        schema_type: str = None,
        subject: str = None,
        registry_id: int = 0,
        version: int = 0,
        schema: dict = None):
        self.schema_type = schema_type
        self.subject = subject
        self.registry_id = registry_id
        self.version = version
        self.schema_dict = schema or {"type": "string"}

    def __str__(self):
        return f"type={self.schema_type}, subject={self.subject}, id={self.registry_id}, " \
               f"version={self.version}  => {str(self.schema_dict)}"

    def __repr__(self):
        return str(self)

    def schema_content_json(self) -> str:
        return '{"schema": ' + json.dumps(self.schema_dict, indent=1) + '}'
