#!/usr/bin/env python3
import sys
from typing import List

from hspylib.core.meta.singleton import Singleton
from hspylib.core.tools.commons import sysout, __version__


class Main(metaclass=Singleton):

    VERSION = __version__("main/.version")

    def __init__(self):
        super().__init__()

    def run(self, *args) -> None:
        with open("welcome.txt") as fh:
            sysout(fh.read(), end='')
        sysout(f"Version {self.VERSION}")


# Application entry point
if __name__ == "__main__":
    """Application entry point"""
    Main().INSTANCE.run(sys.argv[1:])
