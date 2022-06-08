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

   Copyright 2022, HSPyLib team
"""

import sys

from hspylib.core.config.app_config import AppConfigs
from hspylib.core.tools.commons import get_path
from hspylib.modules.cli.application.application import Application
from hspylib.modules.cli.application.version import AppVersion
from hspylib.modules.cli.vt100.vt_utils import exit_app
from hspylib.modules.qt.qt_application import QtApplication
from hspylib.modules.qt.views.qt_view import QtView

HERE = get_path(__file__)

# The resources folder
RESOURCES_DIR = str(HERE / "resources")


class Main(Application):
    """TODO"""

    # The welcome message
    DESCRIPTION = (HERE / "welcome.txt").read_text()

    # location of the .version file
    VERSION_DIR = str(HERE)

    class MainQtView(QtView):
        FORMS_DIR = str(HERE / f"{RESOURCES_DIR}/forms")

        def __init__(self):
            # Must come after the initialization above
            super().__init__(load_dir=self.FORMS_DIR)
            self.configs = AppConfigs.INSTANCE
            self.setup_ui()

        def setup_ui(self) -> None:
            """Connect signals and startup components"""
            print(self.ui.lblHello, self.ui.bboxOkCancel)

    def __init__(self, app_name: str):
        # Invoke the super constructor without source_dir parameter to skip creation of log and properties
        version = AppVersion.load(load_dir=self.VERSION_DIR)
        super().__init__(app_name, version, self.DESCRIPTION.format(version), resource_dir=RESOURCES_DIR)
        self.main_view = QtApplication(self.MainQtView)

    def _setup_arguments(self) -> None:
        """Initialize application parameters and options"""

    def _main(self, *params, **kwargs) -> None:
        """Run the application with the command line arguments"""
        exit_app(self.main_view.run())

    def _cleanup(self) -> None:
        """Execute http_code cleanup before exiting"""


if __name__ == "__main__":
    # Application entry point
    Main('Application name').INSTANCE.run(sys.argv[1:])
