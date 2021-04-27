#!/usr/bin/env python3
import sys
from typing import List

from hspylib.core.tools.commons import sysout, __version__
from hspylib.ui.cli.app.application import Application


class Main(Application):

    VERSION = __version__("main/.version")

    def __init__(self, app_name: str):
        super().__init__(app_name, Main.VERSION)

    def main(self, arguments: List[str]) -> None:
        with open("welcome.txt") as fh:
            sysout(fh.read(), end='')
        sysout(f"Version {Main.VERSION}")


# Application entry point
if __name__ == "__main__":
    """Application entry point"""
    Main('HSPyLib Welcome').INSTANCE.run(sys.argv[1:])
