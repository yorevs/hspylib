from emoji.core import emojize

from hspylib.core.enum.enumeration import Enumeration


def emj_print(emoji_str: str) -> None:
    print(emojize(emoji_str) + ' ', end='')


class Emoji(Enumeration):
    """
        Emoji codes
        Full list of emojis can be found here:
          - https://unicode.org/emoji/charts/emoji-list.html
    """
    def __str__(self) -> str:
        return str(self.value)

    def placeholder(self) -> str:
        return f":{self.name}:"
