from functools import cached_property, lru_cache

from hspylib.core.metaclass.singleton import Singleton

from askai.core.askai_configs import AskAiConfigs
from askai.lang.language import Language
from askai.lang.multilingual_translator import MultilingualTranslator


class TextualMessages(metaclass=Singleton):
    """TODO"""

    INSTANCE = None

    def __init__(self):
        self._configs: AskAiConfigs = AskAiConfigs.INSTANCE or AskAiConfigs()
        self._translator = MultilingualTranslator.INSTANCE or MultilingualTranslator(
            Language.EN_US, self._configs.language
        )

    @lru_cache(maxsize=500)
    def welcome(self, username: str = "user") -> str:
        return self._translate(f"Hey {username}, How can I assist you today?")

    @cached_property
    def wait(self) -> str:
        return self._translate("I'm processing, please wait...")

    @cached_property
    def listening(self) -> str:
        return self._translate("I'm listening...")

    @cached_property
    def transcribing(self) -> str:
        return self._translate("I'm processing your voice, please wait...")

    @cached_property
    def goodbye(self) -> str:
        return self._translate("Goodbye, have a nice day !")

    @lru_cache(maxsize=500)
    def _translate(self, text: str) -> str:
        """Translate text using the configured language."""
        return self._translator.translate(text)
