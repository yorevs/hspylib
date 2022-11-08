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

   Copyright 2022, HSPyLib team
"""
import re
from datetime import datetime
from textwrap import dedent
from uuid import UUID

from hspylib.core.datasource.crud_entity import CrudEntity
from hspylib.core.tools.zoned_datetime import now


class VaultEntry(CrudEntity):
    """Represents a vault entity"""

    # Vault entry format to be displayed when listing
    _DISPLAY_FORMAT = dedent("""
    [%BLUE%{}%NC%]:
            Name: %GREEN%{}%NC%
        Password: %GREEN%{}%NC%
            Hint: %GREEN%{}%NC%
        Modified: %GREEN%{}%NC%
    """)

    def __init__(
        self,
        uuid: UUID,
        key: str,
        name: str,
        password: str,
        hint: str,
        modified: datetime = None):
        super().__init__()
        self.uuid = uuid
        self.key = key
        self.name = name
        self.password = password
        self.hint = hint
        self.modified = modified if modified else now()

    def __str__(self) -> str:
        return str(self.as_dict())

    def __repr__(self) -> str:
        return str(self)

    def to_string(self, show_password: bool = False, show_hint: bool = False) -> str:
        """Return the string representation of this entry
        :param show_password: Whether to exhibit the password or not
        :param show_hint: Whether to exhibit the hint or not
        """
        password = self.password if show_password else re.sub('.*', '*' * min(len(self.password), 5), self.password)
        hint = self.hint if show_hint else re.sub('.*', '*' * min(len(self.hint), 8), self.hint)
        return self._DISPLAY_FORMAT.format(self.key.upper(), self.name, password, hint, self.modified)
