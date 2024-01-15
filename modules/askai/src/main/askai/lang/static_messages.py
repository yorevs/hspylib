from hspylib.core.metaclass.singleton import Singleton

from askai.core.askai_configs import AskAiConfigs
from askai.lang.language import Language
from askai.lang.multilingual_translator import MultilingualTranslator


class StaticMessages(Singleton):
    def __init__(self, username: str):
        self._configs: AskAiConfigs = AskAiConfigs.INSTANCE or AskAiConfigs()
        self._translator = MultilingualTranslator.INSTANCE or MultilingualTranslator(
            Language.EN_US, self._configs.language
        )
        self._username = username

    @staticmethod
    def welcome(username: str) -> str:
        return f"Hey {username}, How can I assist you today?"

    @staticmethod
    def wait(symbol: str, nickname: str) -> str:
        return f"{symbol}  {nickname}: Processing, please wait..."

    @staticmethod
    def listening(symbol: str, nickname: str) -> str:
        return f"{symbol}  {nickname}: Listening..."

    @staticmethod
    def transcribing(symbol: str, nickname: str) -> str:
        return f"{symbol}  {nickname}: Processing your voice..."
