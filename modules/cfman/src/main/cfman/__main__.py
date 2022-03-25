#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.app.cfman.src.main
      @file: __main__.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""
import logging as log
import os
import sys
from datetime import datetime
from textwrap import dedent

from hspylib.core.tools.commons import get_path
from hspylib.modules.cli.application.application import Application
from hspylib.modules.cli.application.version import AppVersion

from cfman.core.cf_manager import CFManager

HERE = get_path(__file__)

log.captureWarnings(True)


class Main(Application):
    """Cloud Foundry Manager - Manage PCF applications."""

    # The welcome message
    DESCRIPTION = (HERE / "welcome.txt").read_text()

    # location of the .version file
    VERSION_DIR = str(HERE)

    def __init__(self, app_name: str):
        version = AppVersion.load(load_dir=self.VERSION_DIR)
        super().__init__(app_name, version, self.DESCRIPTION.format(version))
        self.cfman = None

    def _setup_arguments(self) -> None:
        """Initialize application parameters and options"""
        self._with_options() \
            .option('api', 'a', 'api', 'the API endpoint to connect to (e.g. https://api.example.com)', nargs='?') \
            .option('org', 'o', 'org', 'the organization to connect to (Target organization)', nargs='?') \
            .option('space', 's', 'space', 'the space to connect to (Target organization space)', nargs='?') \
            .option('username', 'u', 'username', 'the PCF username', nargs='?') \
            .option('password', 'p', 'password', 'the PCF password', nargs='?') \
            .option(
            'endpoints', 'f', 'endpoints',
            'the file containing the CF API endpoint entries. If not provided, '
            '$HOME/cf_endpoints.txt will be used instead.', nargs=1)

    def _main(self, *params, **kwargs) -> None:
        """Run the application with the command line arguments"""
        self.cfman = CFManager(
            self.getarg('api'), self.getarg('org'), self.getarg('space'),
            self.getarg('username'), self.getarg('password'),
            self.getarg('endpoints') or os.getenv('HOME', os.getcwd()) + '/.cfman_endpoints.txt'
        )
        log.info(dedent('''
        {} v{}

        Settings ==============================
                STARTED: {}
        ''').format(self._app_name, self._app_version, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        self._exec_application()

    def _exec_application(self) -> None:
        """Execute the application"""
        self.cfman.run()


if __name__ == "__main__":
    # Application entry point
    Main('cfman').INSTANCE.run(sys.argv[1:])
