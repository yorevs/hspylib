from hspylib.modules.application.exit_status import ExitStatus

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
        return self.translate(f"Hello %VIOLET%{username.title()}%NC%, How can I assist you today?")

    @cached_property
    def wait(self) -> str:
        return self.translate("I'm thinking, please wait... ")

    @cached_property
    def listening(self) -> str:
        return self.translate("%BLUE%I'm listening...%NC%")

    @cached_property
    def transcribing(self) -> str:
        return self.translate("Transcribing %GREEN%your voice%NC%, please wait... ")

    @cached_property
    def goodbye(self) -> str:
        return self.translate("Goodbye, have a nice day ! ")

    @lru_cache(maxsize=500)
    def executing(self, cmd_line: str) -> str:
        return self.translate(f"Executing command %GREEN%`{cmd_line}'%NC%, please wait... ")

    @lru_cache(maxsize=500)
    def cmd_success(self, exit_code: ExitStatus) -> str:
        return self.translate(f"OK, the command returned with code: %GREEN%{exit_code}%NC%")

    @lru_cache(maxsize=500)
    def cmd_no_output(self) -> str:
        return self.translate(f"OK, the command didn't return an output.")

    @lru_cache(maxsize=500)
    def cmd_no_exist(self, command: str) -> str:
        return self.translate(f"Sorry! Command %RED%`{command}'%NC% does not exist !")

    @lru_cache(maxsize=500)
    def cmd_failed(self, cmd_line: str) -> str:
        return self.translate(f"Sorry! Command %RED%`{cmd_line}'%NC% failed to execute !")

    @cached_property
    def security_warning(self) -> str:
        return self.translate("%YELLOW%Warning, your confidential data may be compromised. Continue (yes/[no])?%NC%")

    @lru_cache(maxsize=500)
    def translate(self, text: str) -> str:
        """Translate text using the configured language."""
        return self._translator.translate(text)
