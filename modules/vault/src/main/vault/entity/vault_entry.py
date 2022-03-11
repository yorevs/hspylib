#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.app.vault.entity
      @file: vault_entry.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""
import re
from datetime import datetime
from uuid import UUID

from hspylib.core.crud.crud_entity import CrudEntity
from hspylib.core.tools.constants import DATE_TIME_FORMAT


class VaultEntry(CrudEntity):
    """Represents a vault entity"""

    # Vault entry format to be displayed when listing
    _DISPLAY_FORMAT = """
[%BLUE%{}%NC%]:
        Name: %GREEN%{}%NC%
    Password: %GREEN%{}%NC%
        Hint: %GREEN%{}%NC%
    Modified: %GREEN%{}%NC%
"""

    # Vault file entry format
    _FILE_ENTRY_FORMAT = "{}|{}|{}|{}\n"

    def __init__(
        self,
        uuid: UUID,
        key: str,
        name: str,
        password: str,
        hint: str,
        modified: datetime = None):
        super().__init__(uuid)
        self.key = key
        self.name = name
        self.password = password
        self.hint = hint
        self.modified = modified if modified else datetime.now().strftime(DATE_TIME_FORMAT)

    def __str__(self):
        return self._FILE_ENTRY_FORMAT.format(
            self.key, self.name, self.password, self.hint, self.modified)

    def __repr__(self):
        return str(self)

    def to_string(self, show_password: bool = False, show_hint: bool = False) -> str:
        """Return the string representation of this entry
        :param show_password: Whether to exhibit the password or not
        :param show_hint: Whether to exhibit the hint or not
        """
        password = self.password if show_password else re.sub('.*', '*' * min(len(self.password), 5), self.password)
        hint = self.hint if show_hint else re.sub('.*', '*' * min(len(self.hint), 8), self.hint)
        return self._DISPLAY_FORMAT.format(self.key.upper(), self.name, password, hint, self.modified)
