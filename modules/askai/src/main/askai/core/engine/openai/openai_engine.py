import logging as log
import os
from functools import lru_cache
from threading import Thread
from time import sleep
from typing import Callable, Optional

import speech_recognition as speech_rec
from hspylib.core.tools.commons import file_is_not_empty
from openai import APIConnectionError, APIStatusError, OpenAI, RateLimitError

from askai.core.engine.ai_engine import AIEngine
from askai.core.engine.ai_model import AIModel
from askai.core.engine.openai.openai_configs import OpenAiConfigs
from askai.core.engine.openai.openai_model import OpenAiModel
from askai.utils.utilities import play_audio_file, hash_text, input_mic


class OpenAIEngine(AIEngine):
    """Provide a base class for OpenAI features. Implements the prototype AIEngine."""

    def __init__(self, model: AIModel = OpenAiModel.GPT_3_5_TURBO):
        super().__init__()
        self._url = "https://api.openai.com/v1/chat/completions"
        self._configs: OpenAiConfigs = OpenAiConfigs()
        self._nickname = "ChatGPT"
        self._model_name = model.model_name()
        self._balance = 0
        self._client = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),
            organization=os.environ.get("OPENAI_ORG_ID"),
        )
        self._chat = [
            {"role": "system", "content": "you are a kind helpful assistant!"}
        ]

    @property
    def url(self):
        return self._url

    def ai_name(self) -> str:
        return self.__class__.__name__

    def ai_model(self) -> str:
        return self._model_name

    def nickname(self) -> str:
        return self._nickname

    @lru_cache(maxsize=500)
    def ask(self, question: str) -> str:
        self._chat.append({"role": "user", "content": question})
        try:
            log.debug(f"Generating AI answer for: {question}")
            response = self._client.chat.completions.create(
                model=self._model_name, messages=self._chat
            )
            reply = response.choices[0].message.content
            self._chat.append({"role": "assistant", "content": reply})
        except RateLimitError as error:
            reply = (
                "RateLimitError => " + error.body["message"] if error.body else error
            )
        except APIConnectionError as error:
            reply = (
                "APIConnectionError => " + error.body["message"]
                if error.body
                else error
            )
        except APIStatusError as error:
            reply = (
                "APIStatusError => " + error.body["message"] if error.body else error
            )

        return reply

    def reset(self) -> None:
        self._chat = [
            {"role": "system", "content": "you are a kind helpful assistant!"}
        ]

    def text_to_speech(
        self,
        text: str = None,
        speed: int = 0,
        cb_started: Optional[Callable[[str], None]] = None,
        cb_finished: Optional[Callable] = None,
    ) -> None:
        """Text-T0-Speech the provided text. The text to generate audio for. The maximum length
        is 4096 characters.
        :param text: The text to speech.
        :param speed: The tempo to play the generated audio [1..3].
        :param cb_started: The callback function called when the speaker starts.
        :param cb_finished: The callback function called when the speaker ends.
        """
        tmp_dir = os.getenv("TEMP", "/tmp")
        speech_file_path = f"{tmp_dir}/{hash_text(text)}.{self._configs.tts_format}"
        if not file_is_not_empty(speech_file_path):
            log.debug(
                f"Audio file not found. Generating the AI mp3 file: {speech_file_path}"
            )
            response = self._client.audio.speech.create(
                input=text,
                model=self._configs.tts_model,
                voice=self._configs.tts_voice,
                response_format=self._configs.tts_format,
            )
            # Save the audio file locally.
            response.stream_to_file(speech_file_path)
        speak_thread = Thread(
            target=play_audio_file,
            args=(
                speech_file_path,
                speed,
            ),
        )
        speak_thread.start()
        if cb_started:
            # Delayed start.
            sleep(1.1)
            cb_started(text)
        # Block until the speech is done.
        speak_thread.join()
        if cb_finished:
            cb_finished()

    def speech_to_text(
        self,
        prompt: str = "Listening...",
        processing_msg: str = "Transcribing audio to text...",
    ) -> str:
        """Transcribes audio input from the microphone into the text input language."""
        return input_mic(prompt, processing_msg, speech_rec.Recognizer.recognize_whisper)
