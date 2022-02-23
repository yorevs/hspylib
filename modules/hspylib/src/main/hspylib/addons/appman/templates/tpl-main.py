#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   main.addons.appman.templates
      @file: tpl-main.py
   @created: Tue, 1 Jun 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

import sys

from hspylib.core.tools.commons import get_path, sysout
from hspylib.modules.cli.application.application import Application
from hspylib.modules.cli.application.version import AppVersion

HERE = get_path(__file__)


class Main(Application):
    """TODO"""

    # The welcome message
    DESCRIPTION = (HERE / "welcome.txt").read_text()

    # location of the .version file
    VERSION_DIR = str(HERE)

    def __init__(self, app_name: str):
        version = AppVersion.load(load_dir=self.VERSION_DIR)
        super().__init__(app_name, version, self.DESCRIPTION.format(version))

    def _setup_parameters(self, *params, **kwargs) -> None:
        """Initialize application parameters and options"""

    def _main(self, *params, **kwargs) -> None:
        """Run the application with the command line arguments"""
        sysout(f'Hello {self._app_name}')

    def _cleanup(self) -> None:
        """Execute http_code cleanup before exiting"""


if __name__ == "__main__":
    # Application entry point
    Main('application-name').INSTANCE.run(sys.argv[1:])
