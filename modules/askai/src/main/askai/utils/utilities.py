#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib-AskAI
   @package: askai.utils
      @file: utilities.py
   @created: Wed, 10 Jan 2024
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright·(c)·2024,·HSPyLib
"""
from time import sleep

from hspylib.core.tools.commons import sysout


def stream(
    reply_str: str,
    speed: int = 1,
    base_interval_ms: float = 0.010,
) -> None:
    """Stream the response from the AI Engine. Simulates a typewriter effect.
    :param reply_str the text to stream.
    :param speed the speed multiplier of the typewriter effect. Defaults to 1.
    :param base_interval_ms the base delay interval between each characters.
    """
    # hardcoded values were benchmarked
    base_speed = base_interval_ms / max(1, speed)
    alpha_interval_ms: float = base_speed
    number_interval_ms: float = 2 * base_speed
    comma_interval_ms: float = 25 * base_speed
    punct_interval_ms: float = 40 * base_speed

    for next_chr in reply_str:
        sysout(next_chr, end="")
        if next_chr.isalpha():
            sleep(alpha_interval_ms)
        elif next_chr.isnumeric():
            sleep(number_interval_ms)
        elif next_chr in [",", ";"]:
            sleep(comma_interval_ms)
        elif next_chr in [".", "?", "!"]:
            sleep(punct_interval_ms)
        sleep(base_speed)

    sysout("")


if __name__ == '__main__':
    stream("Hello, my friend! How are you doing ? I'm very good thanks, and you ?", speed=0)

