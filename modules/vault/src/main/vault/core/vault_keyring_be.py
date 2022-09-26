#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.app.vault.core
      @file: vault_keyring_be.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
import json
from datetime import datetime
from typing import Optional

import keyring
from hspylib.core.tools.zoned_datetime import now_ms
from keyring.backends.chainer import ChainerBackend
from keyring.errors import PasswordDeleteError


class VaultKeyringBE(ChainerBackend):

    priority = 1

    def __init__(self, ttl_minutes: int = 15) -> None:
        super().__init__()
        self._ttl_minutes = ttl_minutes

    def set_password(self, service_name: str, username: str, password: str) -> None:
        """TODO"""
        expires = now_ms() + (self._ttl_minutes * 60)
        passwd_obj = {'sn': service_name, 'un': username, 'pw': password, 'ttl': expires}
        passwd_str = json.dumps(passwd_obj)
        super().set_password(service_name, username, passwd_str)

    def get_password(self, service_name: str, username: str) -> Optional[str]:
        """TODO"""
        passwd_str = super().get_password(service_name, username)
        if passwd_str:
            passwd_obj = json.loads(passwd_str)
            dt_object = datetime.fromtimestamp(passwd_obj['ttl'])
            expired = now_ms() - dt_object.timestamp()
            if expired > 0:
                keyring.delete_password("TESTE_KEY", "test")
                return None
            return passwd_obj['pw']
        return None

    def delete_password(self, service_name: str, username: str) -> None:
        """TODO"""
        try:
            super().delete_password(service_name, username)
        except PasswordDeleteError:
            pass
