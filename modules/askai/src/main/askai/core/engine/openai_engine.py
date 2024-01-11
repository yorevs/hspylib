import logging as log
import os
from functools import lru_cache
from threading import Thread
from time import sleep
from typing import Callable, Optional

from hspylib.core.enums.enumeration import Enumeration
from hspylib.core.tools.commons import file_is_not_empty
from openai import APIConnectionError, APIStatusError, OpenAI, RateLimitError

from askai.utils.utilities import play_mp3, hash_text


class OpenAIEngine(Enumeration):
    """Provide a base class for OpenAI features."""

    # ID of the model to use. Currently, only the values below are supported

    # fmt: off
    GPT_3_5_TURBO       = 'gpt-3.5-turbo'
    GPT_3_5_TURBO_16K   = 'gpt-3.5-turbo-16k'
    GPT_3_5_TURBO_1106  = 'gpt-3.5-turbo-1106'
    GPT_4               = 'gpt-4'
    # fmt: on

    def __init__(self, model_name: str):
        super().__init__()
        self._url = "https://api.openai.com/v1/chat/completions"
        self._nickname = "ChatGPT"
        self._model_name = model_name
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
        return self.value

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

    def speak(
        self,
        text: str,
        cb_started: Optional[Callable[[str], None]] = None,
        cb_finished: Optional[Callable] = None,
    ) -> None:
        tmp_dir = os.getenv("TEMP", "/tmp")
        speech_file_path = f"{tmp_dir}/{hash_text(text)}.mp3"
        if not file_is_not_empty(speech_file_path):
            log.debug(f"Generating AI mp3 file: {speech_file_path}")
            response = self._client.audio.speech.create(
                model="tts-1", voice="onyx", input=text
            )
            response.stream_to_file(speech_file_path)
        speak_thread = Thread(target=play_mp3, args=(speech_file_path,))
        speak_thread.start()
        if cb_started:
            sleep(1)  # Delayed start.
            cb_started(text)
        speak_thread.join()
        if cb_finished:
            cb_finished()
