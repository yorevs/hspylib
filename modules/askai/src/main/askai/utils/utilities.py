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
import hashlib
from subprocess import DEVNULL
from time import sleep

from clitt.core.term.terminal import Terminal
from hspylib.core.enums.charset import Charset
from hspylib.core.preconditions import check_argument
from hspylib.core.tools.commons import sysout, file_is_not_empty


def hash_text(text: str) -> str:
    """Create a hash string based on the provided text.
    :param: text the text to be hashed.
    """
    return hashlib.md5(text.encode(Charset.UTF_8.val)).hexdigest()


def stream(reply_str: str, speed: int = 1, base_interval_s: float = 0.010) -> None:
    """Stream the response from the AI Engine. Simulates a typewriter effect. The following hardcoded values were
    benchmarked according to the selected speaker engine.
    :param reply_str the text to stream.
    :param speed the speed multiplier of the typewriter effect. Defaults to 1.
    :param base_interval_s the base delay interval between each characters.
    """
    base_speed = base_interval_s / max(1, speed)
    words_interval_s: float = 12.5 * base_speed
    breath_interval_s: float = 46 * base_speed
    number_interval_s: float = 28 * base_speed
    comma_interval_s: float = 26 * base_speed
    punct_interval_s: float = 40 * base_speed
    period_interval_s: float = 2.2 * punct_interval_s
    delayed_start_s: float = 0.4
    words: int = 0

    sleep(delayed_start_s)

    for i, next_chr in enumerate(reply_str):
        sysout(next_chr, end="")
        if next_chr.isalpha():
            sleep(base_speed)
        elif next_chr.isnumeric():
            sleep(number_interval_s)
        elif next_chr in [",", ";"]:
            sleep(
                comma_interval_s
                if i + 1 < len(reply_str) and reply_str[i + 1].isspace()
                else base_speed
            )
        elif next_chr in [".", "?", "!"]:
            sleep(
                period_interval_s
                if i + 1 < len(reply_str) and reply_str[i + 1].isspace()
                else punct_interval_s
            )
            continue
        elif next_chr.isspace():
            if i - 1 >= 0 and not reply_str[i - 1].isspace():
                words += 1
                sleep(breath_interval_s if words % 10 == 0 else words_interval_s)
            continue
        sleep(base_speed)
    sysout("")


def play_mp3(path_to_mp3: str, speed: int = 1) -> None:
    """Play the specified mp3 file using ffplay (ffmpeg) application.
    :param path_to_mp3 the path to the mp3 file to be played.
    :param speed the playing speed.
    """
    check_argument(file_is_not_empty(path_to_mp3))
    Terminal.shell_exec(
        f'ffplay -af "atempo={speed}" -v 0 -nodisp -autoexit {path_to_mp3}',
        stdout=DEVNULL,
    )
