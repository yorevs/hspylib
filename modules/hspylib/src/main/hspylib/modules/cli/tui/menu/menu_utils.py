from hspylib.core.namespace import Namespace
from hspylib.core.tools.commons import sysout
from hspylib.modules.cli.keyboard import Keyboard
from hspylib.modules.cli.tui.minput.input_validator import InputValidator
from hspylib.modules.cli.tui.minput.minput import minput, MenuInput
from hspylib.modules.cli.tui.tui_preferences import TUIPreferences
from hspylib.modules.cli.vt100.vt_utils import restore_cursor


class MenuUtils:

    # fmt: off
    PREFS = TUIPreferences.INSTANCE or TUIPreferences()
    MENU_LINE = f"{'┅┅' * PREFS.title_line_length}"
    MENU_TITLE_FMT = (
        f"{PREFS.title_color}"
        f"┍{MENU_LINE}┓%EOL%"
        "┣{title:^" + str(2 * PREFS.title_line_length) + "s}┫%EOL%"
        f"┕{MENU_LINE}┙%EOL%%NC%"
    )
    # fmt: on

    @classmethod
    def title(cls, title_msg: str) -> None:
        sysout(cls.MENU_TITLE_FMT.format(title=title_msg or "TITLE"))

    @classmethod
    def prompt(cls, label: str, validator: InputValidator = InputValidator.words()) -> Namespace:
        form_fields = MenuInput.builder() \
            .field() \
                .label(label) \
                .validator(validator) \
                .build() \
            .build()
        ret_val = minput(form_fields)
        restore_cursor(True)
        return ret_val

    @classmethod
    def wait_keystroke(cls, wait_message: str = "Press any key to continue") -> None:
        sysout(wait_message)
        Keyboard.wait_keystroke()
