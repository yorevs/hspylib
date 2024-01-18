from functools import cached_property, lru_cache

from hspylib.core.metaclass.singleton import Singleton

from askai.core.askai_configs import AskAiConfigs
from askai.language.language import Language
from askai.language.argos_translator import ArgosTranslator


class AskAiMessages(metaclass=Singleton):
    """Provide access to static 'translated' messages."""

    INSTANCE = None

    def __init__(self):
        self._configs: AskAiConfigs = AskAiConfigs.INSTANCE or AskAiConfigs()
        self._translator = ArgosTranslator.INSTANCE or ArgosTranslator(
            Language.EN_US, self._configs.language
        )

    @lru_cache(maxsize=500)
    def welcome(self, username: str = "user") -> str:
        return self.translate(f"Hey {username}, How can I assist you today?")

    @cached_property
    def wait(self) -> str:
        return self.translate("I'm thinking, please wait... ")

    @cached_property
    def listening(self) -> str:
        return self.translate("I'm listening... ")

    @cached_property
    def transcribing(self) -> str:
        return self.translate("I'm processing your voice, please wait... ")

    @cached_property
    def goodbye(self) -> str:
        return self.translate("Goodbye, have a nice day ! ")

    @cached_property
    def execute(self) -> str:
        return self.translate("execute")

    @lru_cache(maxsize=500)
    def executing(self) -> str:
        return self.translate(f"Executing command, please wait... ")

    @lru_cache(maxsize=500)
    def translate(self, text: str) -> str:
        """Translate text using the configured language."""
        return self._translator.translate(text)
