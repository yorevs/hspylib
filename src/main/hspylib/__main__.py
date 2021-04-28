#!/usr/bin/env python3
import pathlib
import sys
from typing import List

from hspylib.core.meta.singleton import Singleton
from hspylib.core.tools.commons import __version__, sysout

# The directory containing this file
HERE = pathlib.Path(__file__).parent


class Main(metaclass=Singleton):

    VERSION = __version__(f"{HERE}/.version")

    USAGE = """
Usage: hspylib <option> [arguments]

    HSPyLib Manager v{} - Manage HSPyLib applications.

    Options:
      -c  |     --create <app_name> <app_version>
""".format('.'.join(map(str, VERSION)))

    def __init__(self):
        super().__init__()

    def run(self, args: List[str]) -> None:
        if len(args) == 0:
            welcome = (HERE / "welcome.txt").read_text()
            sysout(f"{welcome}")
            sysout(self.USAGE)
        else:
            sysout(str(args))


# Application entry point
if __name__ == "__main__":
    """Application entry point"""
    Main().INSTANCE.run(sys.argv[1:])
