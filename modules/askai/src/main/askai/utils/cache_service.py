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
from typing import Optional, Tuple, List

from clitt.core.tui.line_input.keyboard_input import KeyboardInput
from hspylib.core.metaclass.singleton import Singleton
from hspylib.core.tools.commons import file_is_not_empty
from hspylib.modules.cache.ttl_cache import TTLCache

from askai.utils.utilities import hash_text

CACHE_DIR: Path = Path(f'{os.getenv("HHS_DIR", os.getenv("TEMP", "/tmp"))}/askai')
AUDIO_DIR: Path = Path(str(CACHE_DIR) + "/cache/audio")
if not AUDIO_DIR.exists():
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)


class CacheService(metaclass=Singleton):
    """Provide a cache service for previously used queries, audio generation, etc..."""

    _ttl_cache: TTLCache[str] = TTLCache(ttl_minutes=30)

    ASKAI_INPUT_CACHE_KEY = "askai-input-history"

    @classmethod
    def read_reply(cls, text: str) -> Optional[str]:
        """Read AI replies from TTL cache.
        :param text: Text to be cached.
        """
        key = text.strip().lower()
        return cls._ttl_cache.read(key)

    @classmethod
    def save_reply(cls, text: str, reply: str) -> None:
        """Save a AI reply into the TTL cache.
        :param text: Text to be cached.
        :param reply: The reply associated to this text.
        """
        key = text.strip().lower()
        cls._ttl_cache.save(key, reply)

    @classmethod
    def get_audio_file(cls, text: str, audio_format: str = "mp3") -> Tuple[str, bool]:
        """Retrieve the audio filename and whether it exists or not.
        :param text: Text to be cached.
        :param audio_format: The audio format used.
        """
        key = text.strip().lower()
        audio_file_path = f"{str(AUDIO_DIR)}/askai-{hash_text(key)}.{audio_format}"
        return audio_file_path, file_is_not_empty(audio_file_path)

    @classmethod
    def read_query_history(cls) -> None:
        """Read the input queries from TTL cache."""
        hist_str: str = cls._ttl_cache.read(cls.ASKAI_INPUT_CACHE_KEY)
        if hist_str:
            hist: List[str] = hist_str.split(",")
            KeyboardInput.preload_history(hist)

    @classmethod
    def save_query_history(cls) -> None:
        """Save the line input queries into the TTL cache."""
        hist = KeyboardInput.history()
        cls._ttl_cache.save(cls.ASKAI_INPUT_CACHE_KEY, ",".join(hist))
