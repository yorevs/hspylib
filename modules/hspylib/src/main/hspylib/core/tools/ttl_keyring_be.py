#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.core.tools
      @file: ttl_keyring_be.py
   @created: Tue, 4 Oct 2022
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
import json
from datetime import datetime
from typing import Optional

import keyring
from keyring.backends.chainer import ChainerBackend
from keyring.errors import PasswordDeleteError, PasswordSetError

from hspylib.core.preconditions import check_not_none
from hspylib.core.tools.zoned_datetime import now_ms


class TTLKeyringBE(ChainerBackend):

    priority = 1

    def __init__(self, ttl_minutes: int = 15, ttl_seconds=0) -> None:
        super().__init__()
        self._ttl_minutes = ttl_minutes
        self._ttl_seconds = ttl_seconds

    def get_pws(self, service_name: str, username: str) -> str:
        return super().get_password(service_name, username)

    def set_password(self, service_name: str, username: str, password: str) -> None:
        """Set password for the username of the service."""
        try:
            check_not_none(service_name, username, password)
            expires_sec = now_ms() + ((self._ttl_minutes * 60) + self._ttl_seconds)
            passwd_obj = {'sn': service_name, 'un': username, 'pw': password, 'ttl': expires_sec}
            super().set_password(service_name, username, json.dumps(passwd_obj))
        except PasswordSetError:
            pass  # it does not matter if the password set failed.

    def get_password(self, service_name: str, username: str) -> Optional[str]:
        """Get password of the username for the service."""
        check_not_none(service_name, username)
        if passwd_str := self.get_pws(service_name, username):
            passwd_obj = json.loads(passwd_str)
            dt_object = datetime.fromtimestamp(passwd_obj['ttl'])
            if now_ms() - dt_object.timestamp() > 0:
                keyring.delete_password(service_name, username)
            else:
                return passwd_obj['pw']

        return None

    def delete_password(self, service_name: str, username: str) -> None:
        """Delete the password for the username of the service."""
        check_not_none(service_name, username)
        try:
            super().delete_password(service_name, username)
        except PasswordDeleteError:
            pass  # it does not matter if the password does not exist.
