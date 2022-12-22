#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.app.vault.entity.validator
      @file: entry_validator.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

from datetime import datetime
from typing import List, Tuple

from hspylib.core.constants import RE_COMMON_2_30_NAME
from hspylib.core.preconditions import check_argument, check_state
from hspylib.core.tools.validator import Validator

from vault.entity.vault_entry import VaultEntry


class EntryValidator(Validator):
    def __call__(self, *entries: VaultEntry, **kwargs) -> Tuple[bool, List[dict]]:
        errors = []
        check_argument(len(entries) == 1, "Exactly one entry can be validated at a time. Given: {}", len(entries))
        check_state(isinstance(entries[0], VaultEntry), "Only vault VaultEntry can be validated")
        self.assert_valid(errors, self.validate_key(entries[0].key))
        self.assert_valid(errors, self.validate_name(entries[0].name))
        self.assert_valid(errors, self.validate_password(entries[0].password))
        self.assert_valid(errors, self.validate_hint(entries[0].hint))
        self.assert_valid(errors, self.validate_modified(entries[0].modified))

        return len(errors) == 0, errors

    @staticmethod
    def validate_key(key: str) -> Tuple[bool, str]:
        return Validator.matches(key, RE_COMMON_2_30_NAME), "Invalid key"

    @staticmethod
    def validate_name(name: str) -> Tuple[bool, str]:
        return Validator.matches(name, RE_COMMON_2_30_NAME), "Invalid name"

    @staticmethod
    def validate_password(password: str) -> Tuple[bool, str]:
        return Validator.is_not_blank(password, 3), "Invalid password"

    @staticmethod
    def validate_hint(hint: str) -> Tuple[bool, str]:
        return hint is not None, "Invalid hint"

    @staticmethod
    def validate_modified(modified: datetime) -> Tuple[bool, str]:
        return modified is not None, "Invalid modified date"
