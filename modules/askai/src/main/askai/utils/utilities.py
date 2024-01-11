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
from subprocess import DEVNULL, STDOUT
from time import sleep

from clitt.core.term.terminal import Terminal
from hspylib.core.tools.commons import sysout


def stream(
    reply_str: str,
    speed: int = 1,
    base_interval_ms: float = 0.014,
) -> None:
    """Stream the response from the AI Engine. Simulates a typewriter effect.
    :param reply_str the text to stream.
    :param speed the speed multiplier of the typewriter effect. Defaults to 1.
    :param base_interval_ms the base delay interval between each characters.
    """
    # hardcoded values were benchmarked
    base_speed = base_interval_ms / max(1, speed)
    alpha_interval_ms: float = base_speed
    number_interval_ms: float = 30 * base_speed
    comma_interval_ms: float = 20 * base_speed
    punct_interval_ms: float = 60 * base_speed

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


def play_mp3(path_to_mp3: str) -> None:
    """TODO"""
    Terminal.shell_exec(
        f"ffplay -v 0 -nodisp -autoexit {path_to_mp3}", stdout=DEVNULL, stderr=STDOUT
    )
