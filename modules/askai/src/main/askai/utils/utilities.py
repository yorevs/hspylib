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
from typing import Callable

import speech_recognition as speech_rec
from clitt.core.term.commons import Portion, Direction
from clitt.core.term.terminal import Terminal
from hspylib.core.enums.charset import Charset
from hspylib.core.preconditions import check_argument
from hspylib.core.tools.commons import sysout, file_is_not_empty
from speech_recognition import AudioData

from askai.exception.exceptions import (
    InvalidRecognitionApiError,
    IntelligibleAudioError,
    RecognitionApiRequestError,
)


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
    # fmt: off
    base_speed: float           = base_interval_s / max(1, speed)
    words_interval_s: float     = 13.2 * base_speed
    breath_interval_s: float    = 44 * base_speed
    number_interval_s: float    = 28 * base_speed
    comma_interval_s: float     = 17 * base_speed
    punct_interval_s: float     = 32 * base_speed
    enum_interval_s: float      = 14 * base_speed
    period_interval_s: float    = 62 * base_speed
    # fmt: on
    word_count: int = 0

    for i, next_chr in enumerate(reply_str):
        sysout(next_chr, end="")
        if next_chr.isalpha():
            sleep(base_speed)
        elif next_chr.isnumeric():
            sleep(
                breath_interval_s
                if i + 1 < len(reply_str) and reply_str[i + 1] == "."
                else number_interval_s
            )
        elif next_chr in [":", "-", "\n"]:
            sleep(
                enum_interval_s
                if i + 1 < len(reply_str)
                and reply_str[i + 1].isnumeric()
                or reply_str[i + 1] in [" ", "\n", "-"]
                else base_speed
            )
        elif next_chr in [",", ";"]:
            sleep(
                comma_interval_s
                if i + 1 < len(reply_str) and reply_str[i + 1].isspace()
                else base_speed
            )
        elif next_chr in [".", "?", "!", "\n"]:
            sleep(
                period_interval_s
                if i + 1 < len(reply_str)
                and reply_str[i + 1] in [" ", "\n"]
                and not reply_str[i - 1].isnumeric()
                else punct_interval_s
            )
            continue
        elif next_chr.isspace():
            if i - 1 >= 0 and not reply_str[i - 1].isspace():
                word_count += 1
                sleep(breath_interval_s if word_count % 10 == 0 else words_interval_s)
            continue
        sleep(base_speed)
    sysout("")


def input_text(prompt: str) -> str:
    """Read a string from standard input. The trailing newline is stripped.
    :param prompt: The message to be displayed to the user.
    """
    return input(prompt)


def input_mic(
    prompt: str,
    processing_msg: str,
    fn_recognition: Callable[[AudioData], str] = None,
) -> str:
    """Listen to the microphone and transcribe the speech into text.
    :param prompt: The message to be displayed to the user.
    :param processing_msg: The message displayed when the audio is being processed.
    :param fn_recognition: The AI engine API to use to recognize the speech.
    """
    rec: speech_rec.Recognizer = speech_rec.Recognizer()
    with speech_rec.Microphone() as source:
        sysout(prompt)
        audio: AudioData = rec.listen(source)
        Terminal.INSTANCE.cursor.erase(Portion.LINE)
        Terminal.INSTANCE.cursor.move(len(prompt), Direction.LEFT)
        sysout(processing_msg)
        try:
            recognizer_api = getattr(rec, fn_recognition.__name__)
            if recognizer_api and isinstance(recognizer_api, Callable):
                text = recognizer_api(audio)
                return text.strip()
            raise InvalidRecognitionApiError(str(fn_recognition or "<none>"))
        except speech_rec.UnknownValueError as err:
            raise IntelligibleAudioError(str(err)) from err
        except speech_rec.RequestError as err:
            raise RecognitionApiRequestError(str(err))
        finally:
            Terminal.INSTANCE.cursor.erase(Portion.LINE)
            Terminal.INSTANCE.cursor.move(len(processing_msg), Direction.LEFT)


def play_audio_file(path_to_audio_file: str, speed: int = 1) -> None:
    """Play the specified mp3 file using ffplay (ffmpeg) application.
    :param path_to_audio_file the path to the mp3 file to be played.
    :param speed the playing speed.
    """
    check_argument(file_is_not_empty(path_to_audio_file))
    Terminal.shell_exec(
        f'ffplay -af "atempo={speed}" -v 0 -nodisp -autoexit {path_to_audio_file}',
        stdout=DEVNULL,
    )
