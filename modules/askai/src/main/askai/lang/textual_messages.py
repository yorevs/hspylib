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

    def welcome(self, username: str = "user") -> str:
        return self._translate(f"Hey {username}, How can I assist you today?")

    @property
    def wait(self) -> str:
        return self._translate("I'm processing, please wait...")

    @property
    def listening(self) -> str:
        return self._translate("I'm listening...")

    @property
    def transcribing(self) -> str:
        return self._translate("I'm processing your voice, please wait...")

    @property
    def goodbye(self) -> str:
        return self._translate("Goodbye, have a nice day !")

    def _translate(self, text: str) -> str:
        """Translate text using the configured language."""
        return self._translator.translate(text)
