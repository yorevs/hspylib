#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.app.versioner.src.main
      @file: __main__.py
   @created: Tue, 11 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

import sys

from hspylib.core.tools.commons import get_path, read_version
from hspylib.modules.cli.application.application import Application
from versioner.src.main.core.versioner import Versioner

HERE = get_path(__file__)


class Main(Application):
    """Versioner - Provides an engine to manage app versions."""

    # The application version
    VERSION = read_version()

    # CloudFoundry manager usage message
    USAGE = (HERE / "usage.txt").read_text().format('.'.join(map(str, VERSION)))

    # The welcome message
    WELCOME = (HERE / "welcome.txt").read_text()

    def __init__(self, app_name: str):
        super().__init__(app_name, self.VERSION, self.USAGE)
        self.option_map = {}
        self.versioner = None

    def _setup_parameters(self, *params, **kwargs) -> None:
        self._with_option('b', 'backup', True, lambda arg: print(f'Option -b | --backup = {arg}'))
        self._with_option('d', 'search-dir', True, lambda arg: print(f'Option -d | --search-dir = {arg}'))

    def _main(self, *params, **kwargs) -> None:
        """Run the application with the command line arguments"""
        self.versioner = Versioner(self._get_argument(0).value, self._find_option('d'), self.args[2:])
        self._exec_application()

    def _exec_application(self) -> None:
        """Execute the application"""
        self.versioner.run()


if __name__ == "__main__":
    # Application entry point
    Main('HSPyLib Cloud Foundry Manager').INSTANCE.run(sys.argv[1:])
