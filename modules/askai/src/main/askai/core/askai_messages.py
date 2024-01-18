from askai.core.askai_configs import AskAiConfigs
from askai.language.argos_translator import ArgosTranslator
from askai.language.language import Language
from functools import cached_property, lru_cache
from hspylib.core.metaclass.singleton import Singleton


class AskAiMessages(metaclass=Singleton):
    """Provide access to static 'translated' messages."""

    INSTANCE = None

    def __init__(self):
        self._configs: AskAiConfigs = AskAiConfigs.INSTANCE or AskAiConfigs()
        self._translator = ArgosTranslator.INSTANCE or ArgosTranslator(Language.EN_US, self._configs.language)

    @lru_cache(maxsize=500)
    def welcome(self, username: str = "user") -> str:
        return self.translate(f"Hello {username}, How can I assist you today?")

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
        return self.translate(f"OK, executing command, please wait... ")

    @cached_property
    def security_warning(self) -> str:
        return self.translate("Warning, your confidential data may be compromised. Continue (yes/[no])?")

    @lru_cache(maxsize=500)
    def translate(self, text: str) -> str:
        """Translate text using the configured language."""
        return self._translator.translate(text)
