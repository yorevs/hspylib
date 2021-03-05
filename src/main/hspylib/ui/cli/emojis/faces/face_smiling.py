from hspylib.ui.cli.emojis.emojis import Emoji, emj_print


class FaceSmiling(Emoji):
    """
        Face smiling emojis.
        Codes can be found here:
        - https://unicode.org/emoji/charts/emoji-list.html#face-smiling
    """
    DEFAULT = '\U0001F600'
    BEAMING = '\U0001F601'
    TEARS_OF_JOY = '\U0001F602'
    BIG_EYES = '\U0001F603'
    SMILING_EYES = '\U0001F604'
    SWEAT = '\U0001F605'
    SQUINTING = '\U0001F606'
    HALO = '\U0001F607'
    WINKING = '\U0001F609'
    BLUSHING = '\U0001F60A'
    SLIGHTLY = '\U0001F642'
    UPSIDE_DOWN = '\U0001F643'
    ROFL = '\U0001F923'

    @classmethod
    def demo_emojis(cls):
        list(map(lambda e: emj_print(e), cls.values()))


if __name__ == '__main__':
    FaceSmiling.demo_emojis()
