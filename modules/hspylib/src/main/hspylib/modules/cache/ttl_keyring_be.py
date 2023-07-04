#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib
   @package: hspylib.modules.cache
      @file: ttl_keyring_be.py
   @created: Tue, 4 Oct 2022
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""
from datetime import datetime
from hspylib.core.preconditions import check_not_none
from hspylib.core.zoned_datetime import now_ms
from hspylib.modules.security.security import b64_decode, b64_encode
from keyring.backends.chainer import ChainerBackend
from keyring.errors import PasswordDeleteError, PasswordSetError
from typing import Any, Callable, Optional

import json
import keyring

PWD_EXPIRED_CB = Callable[[str], Any]


class TTLKeyringBE(ChainerBackend):
    """Class to provide a customized Keyring backend with time-to-live timeout."""

    priority = 1

    def __init__(self, ttl_minutes: int = 15, ttl_seconds: int = 0, cb_expired: PWD_EXPIRED_CB = None) -> None:
        super().__init__()
        self._ttl = ttl_minutes, ttl_seconds
        self._cb_expired = cb_expired

    def set_password(self, service: str, username: str, password: str) -> None:
        """Set password for the username of the service."""
        try:
            check_not_none(service, username, password)
            expires_sec = now_ms() + (self._ttl[0] * 60 + self._ttl[1])
            passwd_obj = {"sn": service, "un": username, "pw": password, "ttl": expires_sec}
            b64_pwd = b64_encode(json.dumps(passwd_obj))
            super().set_password(service, username, b64_pwd)
        except PasswordSetError:
            pass  # it does not matter if the password set failed.

    def get_password(self, service: str, username: str) -> Optional[str]:
        """Get password of the username for the service."""
        check_not_none(service, username)
        if b64_pwd := super().get_password(service, username):
            passwd_str = b64_decode(b64_pwd)
            passwd_obj = json.loads(passwd_str)
            dt_object = datetime.fromtimestamp(passwd_obj["ttl"])
            if now_ms() - dt_object.timestamp() > 0:
                keyring.delete_password(service, username)
                if self._cb_expired:
                    self._cb_expired(passwd_obj["pw"])
            else:
                return passwd_obj["pw"]

        return None

    def delete_password(self, service: str, username: str) -> None:
        """Delete the password for the username of the service."""
        check_not_none(service, username)
        try:
            super().delete_password(service, username)
        except PasswordDeleteError:
            pass  # it does not matter if the password does not exist.
