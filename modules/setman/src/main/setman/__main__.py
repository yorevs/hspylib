#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: hspylib
   @package: hspylib
      @file: __main__.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""
import sys


from clitt.core.tui.tui_application import TUIApplication
from hspylib.core.enums.charset import Charset
from hspylib.modules.application.argparse.parser_action import ParserAction
from hspylib.modules.application.exit_status import ExitStatus
from hspylib.modules.application.version import Version

from setman.__classpath__ import _Classpath
from setman.core.setman_enums import SetmanOps, SettingsType


class Main(TUIApplication):
    """HsPyLib CLI Terminal Tools - Create professional CLI applications."""

    # The welcome message
    DESCRIPTION = _Classpath.get_source_path("welcome.txt").read_text(encoding=Charset.UTF_8.val)

    # Location of the .version file
    VERSION_DIR = _Classpath.source_path()

    def __init__(self, app_name: str):
        version = Version.load(load_dir=self.VERSION_DIR)
        super().__init__(app_name, version, self.DESCRIPTION.format(version))

    def _setup_arguments(self) -> None:
        """Initialize application parameters and options."""

        # fmt: off
        self._with_chained_args('operation', 'the operation to execute') \
            .argument(self.Addon.SETMAN.val, 'app Settings Manager: Manage your terminal settings') \
                .add_parameter(
                    'operation',
                    'the operation to be performed against your settings. ',
                    choices=SetmanOps.choices()) \
                .add_option(
                    'name', 'n', 'name',
                    'the settings name. ', nargs='?') \
                .add_option(
                    'value', 'v', 'value',
                    'the settings value. ', nargs='?') \
                .add_option(
                    'stype', 't', 'type',
                    'the settings type. ',
                    choices=SettingsType.choices()) \
                .add_option(
                    'simple', 's', 'simple',
                    'display without formatting. ', action=ParserAction.STORE_TRUE)  # fmt: on

    def _main(self, *params, **kwargs) -> ExitStatus:
        """Main entry point handler."""
        return self._exec_application()

    def _exec_application(self) -> ExitStatus:
        """Execute the application main flow."""

        return ExitStatus.SUCCESS


# Application entry point
if __name__ == "__main__":
    Main("setman").INSTANCE.run(sys.argv[1:])
