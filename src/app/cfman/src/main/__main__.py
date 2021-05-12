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
import sys
from datetime import datetime

from cfman.src.main.core.cf_manager import CFManager
from hspylib.core.tools.commons import dirname, get_path, read_version
from hspylib.modules.cli.application.application import Application

HERE = get_path(__file__)


class Main(Application):
    """Cloud Foundry Manager - Manage PCF applications."""
    
    # The application version
    VERSION = read_version('src/main/.version')
    
    # CloudFoundry manager usage message
    USAGE = (HERE / "usage.txt").read_text().format('.'.join(map(str, VERSION)))
    
    # The welcome message
    WELCOME = (HERE / "welcome.txt").read_text()
    
    def __init__(self, app_name: str):
        super().__init__(app_name, self.VERSION, self.USAGE, dirname(__file__))
        self.option_map = {}
        self.cfman = None
    
    def _setup_parameters(self, *params, **kwargs) -> None:
        self._with_option('a', 'api', True)
        self._with_option('o', 'org', True)
        self._with_option('s', 'space', True)
        self._with_option('u', 'username', True)
        self._with_option('p', 'password', True)
    
    def _main(self, *params, **kwargs) -> None:
        """Run the application with the command line arguments"""
        self.cfman = CFManager(self.option_map)
        log.info(
            self.WELCOME.format(
                self._app_name,
                self.VERSION,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        self._exec_application()
    
    def _exec_application(self) -> None:
        """Execute the application"""
        self.cfman.run()


if __name__ == "__main__":
    # Application entry point
    Main('HSPyLib Cloud Foundry Manager').INSTANCE.run(sys.argv[1:])
