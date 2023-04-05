#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: hspylib.modules.cache
      @file: ttl_cache.py
   @created: Wed, 7 Dec 2022
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
import ast
import os
import tempfile
from threading import Lock
from typing import Generic, Optional, TypeVar

import keyring

from hspylib.core.enums.charset import Charset
from hspylib.core.metaclass.singleton import Singleton
from hspylib.core.preconditions import check_not_none
from hspylib.core.tools.commons import safe_delete_file
from hspylib.modules.cache.ttl_keyring_be import TTLKeyringBE
from hspylib.modules.security.security import b64_decode, b64_encode

T = TypeVar("T")


class TTLCache(Generic[T], metaclass=Singleton):
    """TODO"""

    CACHE_SERVICE = "HS-CACHE-SERVICE"

    def __init__(self, ttl_minutes: int = 15, ttl_seconds: int = 0) -> None:
        super().__init__()
        self._lock = Lock()
        keyring.set_keyring(TTLKeyringBE(ttl_minutes, ttl_seconds, safe_delete_file))

    def save(self, key: str, entry: T) -> str:
        """TODO"""
        check_not_none(key, entry)
        with self._lock:
            with tempfile.NamedTemporaryFile(delete=False, mode="w", encoding=Charset.UTF_8.val) as f_temp:
                content = b64_encode(f"{repr(entry)}")
                f_temp.write(content)
                keyring.set_password(self.CACHE_SERVICE, key, f_temp.name)
                return f_temp.name

    def read(self, key: str) -> Optional[T]:
        """TODO"""
        check_not_none(key)
        with self._lock:
            cache_name = keyring.get_password(self.CACHE_SERVICE, key)
            if not cache_name or not os.path.exists(cache_name):
                return None
            try:
                with open(cache_name, encoding=Charset.UTF_8.val) as f_cache:
                    content = b64_decode(f_cache.readline())
                    return ast.literal_eval(content)
            except (ValueError, TypeError, SyntaxError):
                return None

    def delete(self, key: str) -> None:
        """TODO"""
        check_not_none(key)
        with self._lock:
            keyring.delete_password(self.CACHE_SERVICE, key)
