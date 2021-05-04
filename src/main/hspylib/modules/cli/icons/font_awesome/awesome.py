import struct

from idna.core import unicode

from hspylib.core.enum.enumeration import Enumeration


def awe_print(awesome_str: str) -> None:
    print(awesome_str + ' ', end='')


class Awesome(Enumeration):
    """
        Font awesome codes
        Full list of font awesome icons can be found here:
          - https://fontawesome.com/cheatsheet?from=io
    """

    @staticmethod
    def demo_unicode():
        i = 0
        st_base = ['F{:03X}'.format(x) for x in range(0, 4095)]
        for n in st_base:
            hexa = unicode(struct.pack("!I", int(n, 16)), 'utf_32_be')
            endz = '\n' if i != 0 and i % 10 == 0 else ' '
            print('{} {}'.format(hexa, n), end=endz)
            i += 1

    @classmethod
    def demo_icons(cls):
        list(map(lambda e: awe_print(e), cls.values()))

    def __str__(self) -> str:
        return str(self.value)

    def placeholder(self) -> str:
        return f":{self.name}:"


if __name__ == '__main__':
    Awesome.demo_unicode()
