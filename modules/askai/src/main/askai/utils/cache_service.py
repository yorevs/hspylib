#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib-AskAI
   @package: askai.utils
      @file: cache_service.py
   @created: Tue, 16 Jan 2024
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright·(c)·2024,·HSPyLib
"""
import os
from pathlib import Path
from typing import Optional

from hspylib.core.metaclass.singleton import Singleton
from hspylib.modules.cache.ttl_cache import TTLCache

from askai.utils.utilities import hash_text

CACHE_DIR: Path = Path(f'{os.getenv("HHS_DIR", os.getenv("TEMP", "/tmp"))}/askai')
AUDIO_DIR: Path = Path(str(CACHE_DIR) + "/cache/audio")
if not AUDIO_DIR.exists():
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)


class CacheService(metaclass=Singleton):
    _ttl_cache: TTLCache[str] = TTLCache(ttl_minutes=60)

    @classmethod
    def read_reply(cls, key: str) -> str:
        return cls._ttl_cache.read(key)

    @classmethod
    def save_reply(cls, key: str, reply: str):
        cls._ttl_cache.save(key, reply)

    @classmethod
    def get_audio_file(cls, text: str, audio_format: str = "mp3") -> str:
        return f"{str(AUDIO_DIR)}/askai-{hash_text(text)}.{audio_format}"
