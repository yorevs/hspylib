#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: hspylib
   @package: hspylib
      @file: __main__.py
   @created: Fri, 5 Jan 2024
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright·(c)·2024,·HSPyLib
"""
import re
import sys
from clitt.__classpath__ import _Classpath
from clitt.core.tui.tui_application import TUIApplication
from hspylib.core.enums.charset import Charset
from hspylib.core.tools.commons import sysout
from hspylib.modules.application.exit_status import ExitStatus
from hspylib.modules.application.version import Version

from askai.core.ask_ai import AIBrain


class Main(TUIApplication):
    """HsPyLib Ask-AI Terminal Tools - AI on the palm of your shell."""

    # The welcome message
    DESCRIPTION = _Classpath.get_source_path("welcome.txt").read_text(encoding=Charset.UTF_8.val)

    # Location of the .version file
    VERSION_DIR = _Classpath.source_path()

    def __init__(self, app_name: str):
        version = Version.load(load_dir=self.VERSION_DIR)
        super().__init__(app_name, version, self.DESCRIPTION.format(version))
        self._ai = AIBrain()

    def _setup_arguments(self) -> None:
        """Initialize application parameters and options."""

    def _main(self, *params, **kwargs) -> ExitStatus:
        """Main entry point handler."""
        return self._exec_application()

    def _exec_application(self) -> ExitStatus:
        """Execute the application main flow."""
        sysout(self._ai)

        while message := input("User: "):
            if re.match(r"(good)?bye|tchau|quit|exit", message.lower()):
                sysout(f"ChatGPT: {message.title()}")
                break
            sysout("ChatGPT: ", end='')
            sysout(self._ai.ask(message))

        if not message:
            sysout("ChatGPT: Bye")

        return ExitStatus.SUCCESS


# Application entry point
if __name__ == "__main__":
    Main("askai").INSTANCE.run(sys.argv[1:])
