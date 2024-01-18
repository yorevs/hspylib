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
from askai.utils.utilities import hash_text
from hspylib.core.metaclass.singleton import Singleton
from hspylib.core.tools.commons import file_is_not_empty
from hspylib.modules.cache.ttl_cache import TTLCache
from pathlib import Path
from typing import Optional, Tuple

import os

CACHE_DIR: Path = Path(f'{os.getenv("HHS_DIR", os.getenv("TEMP", "/tmp"))}/askai')
AUDIO_DIR: Path = Path(str(CACHE_DIR) + "/cache/audio")
if not AUDIO_DIR.exists():
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)


class CacheService(metaclass=Singleton):
    """Provide a cache service for previously used queries, audio generation, etc..."""

    _ttl_cache: TTLCache[str] = TTLCache(ttl_minutes=60)

    @classmethod
    def read_reply(cls, text: str) -> Optional[str]:
        """Read a previous reply from cache."""
        key = text.strip().lower()
        return cls._ttl_cache.read(key)

    @classmethod
    def save_reply(cls, text: str, reply: str) -> None:
        """Save a reply into the cache."""
        key = text.strip().lower()
        cls._ttl_cache.save(key, reply)

    @classmethod
    def get_audio_file(cls, text: str, audio_format: str = "mp3") -> Tuple[str, bool]:
        """Retrieve the audio filename and whether it exists or not."""
        key = text.strip().lower()
        audio_file_path = f"{str(AUDIO_DIR)}/askai-{hash_text(key)}.{audio_format}"
        return audio_file_path, file_is_not_empty(audio_file_path)
