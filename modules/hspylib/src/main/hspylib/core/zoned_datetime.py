#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib
   @package: hspylib.core
      @file: zoned_datetime.py
   @created: Thu, 20 Sep 2022
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""
from datetime import datetime, timezone
from hspylib.core.enums.enumeration import Enumeration

# fmt: off
# Date and time formats
ISO_DATETIME_FORMAT     = '%Y-%m-%dT%H:%M:%S%z'
SIMPLE_DATETIME_FORMAT  = '%Y-%m-%d %H:%M:%S'
DATE_FORMAT             = '%Y-%m-%d'
TIME_FORMAT             = '%H:%M:%S'
# fmt: on


class ZonedDatetime(Enumeration):
    """TODO"""

    # fmt: off
    LOCAL   = 'localtime'
    UTC     = 'UTC'
    # fmt: on

    def datetime(self) -> datetime:
        """Return the current datetime"""
        now_dt = datetime.now(timezone.utc)
        if self == ZonedDatetime.LOCAL:
            now_dt = now_dt.astimezone()

        return now_dt

    def now(self, date_time_fmt: str = SIMPLE_DATETIME_FORMAT) -> str:
        """Return a formatted datetime string,
        Ref. https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
        """

        return self.datetime().strftime(date_time_fmt)

    def now_ms(self) -> int:
        """Return the datetime timestamp,"""

        return int(self.datetime().timestamp())


def now(date_time_fmt: str = SIMPLE_DATETIME_FORMAT) -> str:
    return ZonedDatetime.LOCAL.now(date_time_fmt)


def now_ms() -> int:
    return ZonedDatetime.LOCAL.now_ms()
