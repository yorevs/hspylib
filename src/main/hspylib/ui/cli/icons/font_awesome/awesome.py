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
    @classmethod
    def awesomize(cls, awesome_str: str) -> str:
        return f"{awesome_str}"

    @classmethod
    def deawesomize(cls, awesome_code: str) -> str:
        return f"{awesome_code}"

    def __str__(self) -> str:
        return self.value

    def placeholder(self) -> str:
        return f":{self.name}:"

    @staticmethod
    def demo_unicodes():
        i = 0
        st_base = ['F{:03X}'.format(x) for x in range(0, 4095)]
        for n in st_base:
            hexa = unicode(struct.pack("!I", int(n, 16)), 'utf_32_be')
            endz = '\n' if i != 0 and i % 10 == 0 else ' '
            print('{} {}'.format(hexa, n), end=endz)
            i += 1


if __name__ == '__main__':
    print(Awesome.awesomize('arrow-left'))
    print(Awesome.deawesomize(''))
