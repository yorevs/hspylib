#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   hspylib.app.cfman.src.main
      @file: __main__.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

import logging as log
import sys
from datetime import datetime
from textwrap import dedent

from hspylib.core.tools.commons import get_path
from hspylib.modules.cli.application.application import Application
from hspylib.modules.cli.application.version import AppVersion

from cfman.core.cf_manager import CFManager

HERE = get_path(__file__)


class Main(Application):
    """Cloud Foundry Manager - Manage PCF applications."""

    # The welcome message
    DESCRIPTION = (HERE / "welcome.txt").read_text()

    def __init__(self, app_name: str):
        version = AppVersion.load()
        super().__init__(app_name, version, self.DESCRIPTION.format(version))
        self.cfman = None

    def _setup_arguments(self) -> None:
        """Initialize application parameters and options"""

        self._with_options() \
            .option('api', 'a', 'api', 'the API to connect to (API endpoint, e.g. https://api.example.com)') \
            .option('org', 'o', 'org', 'the organization to connect to (Target organization)') \
            .option('org', 's', 'space', 'the space to connect to (Target organization space)') \
            .option('org', 'u', 'username', 'the PCF username', required=True) \
            .option('org', 'p', 'password', 'the PCF password', required=True)

    def _main(self, *params, **kwargs) -> None:
        """Run the application with the command line arguments"""
        self.cfman = CFManager(self._args)
        log.info(dedent('''
        {} v{}

        Settings ==============================
                STARTED: {}
        ''').format(self._app_name, AppVersion.load(), datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        self._exec_application()

    def _exec_application(self) -> None:
        """Execute the application"""
        self.cfman.run()


if __name__ == "__main__":
    # Application entry point
    Main('HSPyLib Cloud Foundry Manager').INSTANCE.run(sys.argv[1:])
