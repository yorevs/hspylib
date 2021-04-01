import emoji

from hspylib.core.enum.enumeration import Enumeration


def emj_print(emoji_str: str) -> None:
    print(Emoji.emojize(emoji_str) + ' ', end='')


class Emoji(Enumeration):
    """
        Emoji codes
        Full list of emojis can be found here:
          - https://unicode.org/emoji/charts/emoji-list.html
    """
    @classmethod
    def emojize(cls, emoji_str: str) -> str:
        return emoji.emojize(f"{emoji_str}")

    @classmethod
    def demojize(cls, emoji_str: str) -> str:
        return emoji.demojize(f"{emoji_str}")

    def __str__(self) -> str:
        return self.value

    def placeholder(self) -> str:
        return f":{self.name}:"
