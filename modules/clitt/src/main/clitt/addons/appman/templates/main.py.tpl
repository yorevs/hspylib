#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from %APP_NAME%.__classpath__ import _Classpath
from hspylib.core.enums.charset import Charset
from hspylib.core.tools.commons import get_path, sysout
from hspylib.modules.application.application import Application
from hspylib.modules.application.exit_status import ExitStatus
from hspylib.modules.application.version import Version

import sys

HERE = get_path(__file__)


class Main(Application):
  """TODO"""

  # The welcome message
  DESCRIPTION = (HERE / "welcome.txt").read_text(encoding=Charset.UTF_8.val)

  # Location of the .version file
  VERSION_DIR = _Classpath.source_path()

  # Location of the resource directory
  RESOURCE_DIR = str(_Classpath.resource_path())

  def __init__(self, app_name: str):
    version = Version.load(load_dir=self.VERSION_DIR)
    super().__init__(app_name, version, self.DESCRIPTION.format(version), resource_dir=self.RESOURCE_DIR)

  def _setup_parameters(self, *params, **kwargs) -> None:
    """Initialize application parameters and options"""

  def _setup_arguments(self) -> None:
    """Initialize application parameters and options"""

  def _main(self, *params, **kwargs) -> ExitStatus:
    """Run the application with the command line arguments"""
    sysout(f'Hello {self._app_name}')
    return ExitStatus.SUCCESS

  def _cleanup(self) -> None:
    """Execute http_code cleanup before exiting"""


if __name__ == "__main__":
  # Application entry point
  Main('%APP_NAME%').INSTANCE.run(sys.argv[1:])
