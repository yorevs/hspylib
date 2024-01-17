#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib-AskAI
   @package: askai.utils
      @file: presets.py
   @created: Tue, 16 Jan 2024
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright·(c)·2024,·HSPyLib
"""
import functools
from string import Template
from textwrap import dedent


class Presets:
    """TODO"""

    # fmt: off
    _ALL_RESETS = {
        "en": {
             "words.interval.sec": Template("13.2 * ${base_speed}"),
            "breath.interval.sec": Template("44 * ${base_speed}"),
            "number.interval.sec": Template("28 * ${base_speed}"),
             "comma.interval.sec": Template("17 * ${base_speed}"),
             "punct.interval.sec": Template("32 * ${base_speed}"),
              "enum.interval.sec": Template("14 * ${base_speed}"),
            "period.interval.sec": Template("62 * ${base_speed}"),
        },
        "pt": {
             "words.interval.sec": Template("13.2 * ${base_speed}"),
            "breath.interval.sec": Template("44 * ${base_speed}"),
            "number.interval.sec": Template("28 * ${base_speed}"),
             "comma.interval.sec": Template("17 * ${base_speed}"),
             "punct.interval.sec": Template("32 * ${base_speed}"),
              "enum.interval.sec": Template("14 * ${base_speed}"),
            "period.interval.sec": Template("62 * ${base_speed}"),
        }
    }
    # fmt: on

    @classmethod
    @functools.lru_cache(maxsize=125)
    def get(cls, lang: str = "en", tempo: int = 1, base_interval: float = 0.010) -> "Presets":
        base_speed = base_interval / max(1, tempo)
        presets = cls._ALL_RESETS[lang] if hasattr(cls._ALL_RESETS, lang) else cls._ALL_RESETS["en"]
        return Presets(
            lang,
            base_speed,
            float(eval(presets["words.interval.sec"].substitute(base_speed=base_speed))),
            float(eval(presets["breath.interval.sec"].substitute(base_speed=base_speed))),
            float(eval(presets["number.interval.sec"].substitute(base_speed=base_speed))),
            float(eval(presets["comma.interval.sec"].substitute(base_speed=base_speed))),
            float(eval(presets["punct.interval.sec"].substitute(base_speed=base_speed))),
            float(eval(presets["enum.interval.sec"].substitute(base_speed=base_speed))),
            float(eval(presets["period.interval.sec"].substitute(base_speed=base_speed))),
        )

    def __init__(
        self,
        lang: str,
        base_speed: float,
        words_interval: float,
        breath_interval: float,
        number_interval: float,
        comma_interval: float,
        punct_interval: float,
        enum_interval: float,
        period_interval: float
    ):
        self._lang = lang
        self._base_speed = base_speed
        self._words_interval = words_interval
        self._breath_interval = breath_interval
        self._number_interval = number_interval
        self._comma_interval = comma_interval
        self._punct_interval = punct_interval
        self._enum_interval = enum_interval
        self._period_interval = period_interval

    def __str__(self) -> str:
        return dedent((
            f"Presets.{self._lang}("
            f"Base Speed={self.base_speed}, "
            f"Words Interval={self.words_interval}, "
            f"Breath Interval={self.breath_interval}, "
            f"Number Interval={self.number_interval}, "
            f"Comma Interval={self.comma_interval}, "
            f"Punct Interval={self.punct_interval}, "
            f"Enum Interval={self.enum_interval}, "
            f"Period Interval={self.period_interval}"))

    @property
    def base_speed(self) -> float:
        """TODO"""
        return self._base_speed

    @property
    def words_interval(self) -> float:
        """TODO"""
        return self._words_interval

    @property
    def breath_interval(self) -> float:
        """TODO"""
        return self._breath_interval

    @property
    def number_interval(self) -> float:
        """TODO"""
        return self._number_interval

    @property
    def comma_interval(self) -> float:
        """TODO"""
        return self._comma_interval

    @property
    def punct_interval(self) -> float:
        """TODO"""
        return self._punct_interval

    @property
    def enum_interval(self) -> float:
        """TODO"""
        return self._enum_interval

    @property
    def period_interval(self) -> float:
        """TODO"""
        return self._period_interval
