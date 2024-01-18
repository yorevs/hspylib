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
import logging as log
from functools import partial
from shutil import which
from subprocess import DEVNULL
from time import sleep
from typing import Callable

import speech_recognition as speech_rec
from clitt.core.term.commons import Direction, Portion
from clitt.core.term.terminal import Terminal
from hspylib.core.enums.charset import Charset
from hspylib.core.preconditions import check_argument
from hspylib.core.tools.commons import sysout, file_is_not_empty
from hspylib.core.tools.text_tools import ensure_endswith
from speech_recognition import AudioData

from askai.__classpath__ import _Classpath
from askai.exception.exceptions import (
    InvalidRecognitionApiError,
    IntelligibleAudioError,
    RecognitionApiRequestError,
)
from askai.lang.language import Language
from askai.utils.presets import Presets

# Sound effects directory.
SFX_DIR = str(_Classpath.resource_path()) + "/assets/sound-fx"


def hash_text(text: str) -> str:
    """Create a hash string based on the provided text.
    :param: text the text to be hashed.
    """
    return hashlib.md5(text.encode(Charset.UTF_8.val)).hexdigest()


def stream(reply_str: str, tempo: int = 1, language: Language = Language.EN_US) -> None:
    """Stream the response from the AI Engine. Simulates a typewriter effect. The following presets were
    benchmarked according to the selected speaker engine and language.
    :param reply_str: the text to stream.
    :param tempo: the speed multiplier of the typewriter effect. Defaults to 1.
    :param language: the language used to stream the text.
    """
    ln = language.mnemonic.split("_")[0]
    presets = Presets.get(ln, tempo=tempo)
    word_count: int = 0

    # The following algorithm was created based on the whisper voice.
    for i, next_chr in enumerate(reply_str):
        sysout(next_chr, end="")
        if next_chr.isalpha():
            sleep(presets.base_speed)
        elif next_chr.isnumeric():
            sleep(
                presets.breath_interval
                if i + 1 < len(reply_str) and reply_str[i + 1] == "."
                else presets.number_interval
            )
        elif next_chr in [":", "-", "\n"]:
            sleep(
                presets.enum_interval
                if i + 1 < len(reply_str)
                and reply_str[i + 1].isnumeric()
                or reply_str[i + 1] in [" ", "\n", "-"]
                else presets.base_speed
            )
        elif next_chr in [",", ";"]:
            sleep(
                presets.comma_interval
                if i + 1 < len(reply_str) and reply_str[i + 1].isspace()
                else presets.base_speed
            )
        elif next_chr in [".", "?", "!", "\n"]:
            sleep(
                presets.period_interval
                if i + 1 < len(reply_str)
                and reply_str[i + 1] in [" ", "\n"]
                and not reply_str[i - 1].isnumeric()
                else presets.punct_interval
            )
            continue
        elif next_chr.isspace():
            if i - 1 >= 0 and not reply_str[i - 1].isspace():
                word_count += 1
                sleep(
                    presets.breath_interval
                    if word_count % 10 == 0
                    else presets.words_interval
                )
            continue
        sleep(presets.base_speed)
    sysout("")


def input_mic(
    fn_listening: partial,
    fn_processing: partial,
    fn_recognition: Callable[[AudioData], str],
) -> str:
    """Listen to the microphone and transcribe the speech into text.
    :param fn_listening: The function to display the listening message.
    :param fn_processing: The function to display the processing message.
    :param fn_recognition: The AI engine API to use to recognize the speech.
    """
    rec: speech_rec.Recognizer = speech_rec.Recognizer()
    with speech_rec.Microphone() as source:
        rec.adjust_for_ambient_noise(source, duration=1)
        msg = fn_listening()
        audio: AudioData = rec.listen(source)
        Terminal.INSTANCE.cursor.move(1, Direction.UP)
        Terminal.INSTANCE.cursor.erase(Portion.LINE)
        Terminal.INSTANCE.cursor.move(len(msg), Direction.LEFT)
        msg = fn_processing()
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
            Terminal.INSTANCE.cursor.move(1, Direction.UP)
            Terminal.INSTANCE.cursor.erase(Portion.LINE)
            Terminal.INSTANCE.cursor.move(len(msg), Direction.LEFT)


def play_audio_file(path_to_audio_file: str, speed: int = 1) -> bool:
    """Play the specified mp3 file using ffplay (ffmpeg) application.
    :param path_to_audio_file: the path to the mp3 file to be played.
    :param speed: the playing speed.
    """
    check_argument(which("ffplay") and file_is_not_empty(path_to_audio_file))
    try:
        Terminal.shell_exec(
            f'ffplay -af "atempo={speed}" -v 0 -nodisp -autoexit {path_to_audio_file}',
            stdout=DEVNULL,
        )
        return True
    except FileNotFoundError:
        log.error("ffplay is not installed, speech is disabled!")
        return False


def play_sfx(sfx_name: str):
    """Play a sound effect audio file."""
    filename = f"{SFX_DIR}/{ensure_endswith(sfx_name, '.mp3')}"
    check_argument(file_is_not_empty(filename), f"Sound effects file does not exist: {filename}")
    play_audio_file(filename)
