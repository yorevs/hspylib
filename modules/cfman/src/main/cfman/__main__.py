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

   Copyright 2022, HSPyLib team
"""
import logging as log
import os
import sys
from textwrap import dedent

from hspylib.core.enums.charset import Charset
from hspylib.core.zoned_datetime import now
from hspylib.modules.cli.application.application import Application
from hspylib.modules.cli.application.version import Version

from cfman.__classpath__ import _Classpath
from cfman.core.cf_manager import CFManager

log.captureWarnings(True)


class Main(Application):
    """Cloud Foundry Manager - Manage PCF applications."""

    # The welcome message
    DESCRIPTION = _Classpath.get_source_path("welcome.txt").read_text(encoding=str(Charset.UTF_8))

    # location of the .version file
    VERSION_DIR = _Classpath.source_path()

    def __init__(self, app_name: str):
        version = Version.load(load_dir=self.VERSION_DIR)
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
            .option('refresh', 'r', 'refresh', 'avoiding using cached apps', nargs='?') \
            .option('endpoints', 'f', 'endpoints',
                    'the file containing the CF API endpoint entries. If not provided, '
                    '$HOME/cf_endpoints.txt will be used instead.', nargs=1)

    def _main(self, *params, **kwargs) -> int:
        """Run the application with the command line arguments"""
        self.cfman = CFManager(
            self.get_arg('api'), self.get_arg('org'), self.get_arg('space'),
            self.get_arg('username'), self.get_arg('password'), self.get_arg('refresh'),
            self.get_arg('endpoints') or f"{os.getenv('HOME', os.getcwd())}/.cfman_endpoints.txt"
        )
        log.info(dedent(f'''
        {self._app_name} v{self._app_version}

        Settings ==============================
                STARTED: {now("%Y-%m-%d %H:%M:%S")}
        '''))
        self._exec_application()
        return 0

    def _exec_application(self) -> None:
        """Execute the application"""
        self.cfman.run()

    def _cleanup(self) -> None:
        pass

if __name__ == "__main__":
    # Application entry point
    Main('cfman').INSTANCE.run(sys.argv[1:])
