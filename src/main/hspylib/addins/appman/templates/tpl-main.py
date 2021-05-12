#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.main.hspylib.addins.appman.templates
      @file: tpl-main.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

import sys

from hspylib.core.tools.commons import dirname, get_path, read_version, sysout
from hspylib.modules.cli.application.application import Application

HERE = get_path(__file__)


class Main(Application):
    """TODO"""
    
    # The application version
    VERSION = read_version(f"{HERE}/.version")
    
    # Usage message
    USAGE = (HERE / "usage.txt").read_text().format('.'.join(map(str, VERSION)))
    
    def __init__(self, app_name: str):
        # Invoke the super constructor without source_dir parameter to skip creation of log and properties
        super().__init__(app_name, self.VERSION, self.USAGE, source_dir=dirname(__file__))
    
    def _setup_parameters(self, *params, **kwargs):
        """Initialize application parameters and options"""
    
    def _main(self, *params, **kwargs) -> None:
        """Run the application with the command line arguments"""
        sysout(f'Hello {self._app_name}')
    
    def _cleanup(self):
        """Execute code cleanup before exiting"""


if __name__ == "__main__":
    # Application entry point
    Main('Application name').INSTANCE.run(sys.argv[1:])
