import logging as log
import os
from functools import partial
from threading import Thread
from time import sleep
from typing import Callable, Optional

import speech_recognition as speech_rec
from openai import APIConnectionError, APIStatusError, OpenAI, RateLimitError

from askai.core.engine.ai_engine import AIEngine
from askai.core.engine.ai_model import AIModel
from askai.core.engine.openai.openai_configs import OpenAiConfigs
from askai.core.engine.openai.openai_model import OpenAiModel
from askai.utils.cache_service import CacheService as cache
from askai.utils.utilities import play_audio_file, input_mic


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
        self._chat_context = [
            {"role": "system", "content": "HomSetup thanks you kind AI assistant!"}
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

    def ask(self, question: str) -> str:
        if not (reply := cache.read_reply(question)):
            log.debug('Response not found for: "%s" in cache. Querying AI engine.', question)
            try:
                self._chat_context.append({"role": "user", "content": question})
                log.debug(f"Generating AI answer for: {question}")
                response = self._client.chat.completions.create(
                    model=self._model_name, messages=self._chat_context
                )
                reply = response.choices[0].message.content
                if reply:
                    self._chat_context.append({"role": "assistant", "content": reply})
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
            cache.save_reply(question, reply)
        else:
            log.debug('Response found for: "%s" in cache.', question)

        return reply

    def forget(self) -> None:
        """Forget the chat context and start over."""
        self._chat_context = [
            {"role": "system", "content": "HomeSetup thanks you kind AI assistant!"}
        ]

    def text_to_speech(
        self,
        text: str = None,
        speed: int = 0,
        cb_started: Optional[Callable[[str], None]] = None,
        cb_finished: Optional[Callable] = None,
    ) -> None:
        speech_file_path, file_exists = cache.get_audio_file(text, self._configs.tts_format)
        if not file_exists:
            log.debug(f'Audio file "%s" not found in cache. Querying AI engine.', speech_file_path)
            response = self._client.audio.speech.create(
                input=text,
                model=self._configs.tts_model,
                voice=self._configs.tts_voice,
                response_format=self._configs.tts_format,
            )
            # Save the audio file locally.
            response.stream_to_file(speech_file_path)
        speak_thread = Thread(
            daemon=True,
            target=play_audio_file,
            args=(
                speech_file_path,
                speed,
            ),
        )
        speak_thread.start()
        if cb_started:
            # Delayed start.
            sleep(1)
            cb_started(text)
        # Block until the speech has finished.
        speak_thread.join()
        if cb_finished:
            cb_finished()

    def speech_to_text(
        self,
        fn_listening: partial,
        fn_processing: partial,
    ) -> str:
        text = input_mic(
            fn_listening,
            fn_processing,
            speech_rec.Recognizer.recognize_whisper
        )
        log.debug(f"Audio transcribed to: {text}")
        return text
