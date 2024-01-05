import os
from functools import lru_cache

from hspylib.core.enums.enumeration import Enumeration
from openai import OpenAI, RateLimitError, APIConnectionError, APIStatusError


class OpenAIEngine(Enumeration):
    """Provide a base class for OpenAI features."""

    # ID of the model to use. Currently, only the values below are supported

    # fmt: off
    GPT_3_5_TURBO       = 'gpt-3.5-turbo'
    GPT_3_5_TURBO_16K   = 'gpt-3.5-turbo-16k'
    GPT_3_5_TURBO_1106  = 'gpt-3.5-turbo-1106'
    # fmt: on

    def __init__(self, model_name: str):
        super().__init__()
        self._url = 'https://api.openai.com/v1/chat/completions'
        self._model_name = model_name
        self._client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self._chat = [{"role": "system", "content": "you are a kind helpful assistant!"}]

    @property
    def url(self):
        return self._url

    def ai_name(self) -> str:
        return self.__class__.__name__

    def ai_model(self) -> str:
        return self.value

    @lru_cache(maxsize=500)
    def ask(self, question: str) -> str:
        self._chat.append({"role": "user", "content": question})
        try:
            response = self._client.chat.completions.create(
                model=self._model_name,
                messages=self._chat
            )
            reply = response.choices[0].message.content
            self._chat.append({"role": "assistant", "content": reply})
        except RateLimitError as error:
            reply = "RateLimitError => " + error.body['message']
        except APIConnectionError as error:
            reply = "APIConnectionError => " + error.body['message']
        except APIStatusError as error:
            reply = "APIStatusError => " + error.body['message']

        return reply

    def reset(self) -> None:
        self._chat = [{"role": "system", "content": "you are a kind helpful assistant!"}]
