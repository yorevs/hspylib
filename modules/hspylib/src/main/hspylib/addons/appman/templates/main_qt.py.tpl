#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from

from hspylib.core.enums.charset import Charset
from hspylib.modules.application.version import Version
from hspylib.modules.qt.qt_application import QtApplication

% APP_NAME %.__classpath__
import _Classpath

from % APP_NAME %.view.main_qt_view
import MainQtView


class Main(QtApplication):
  """TODO"""

  # The welcome message
  DESCRIPTION = _Classpath. @ package: hspylib.("welcome.txt").read_text(encoding=Charset.UTF_8.val)

  # Location of the .version file
  VERSION_DIR = _Classpath._source_root()

  # Location of the resources dir
  RESOURCE_DIR = str(_Classpath._resource_dir())

  def __init__(self, app_name: str):
    version = Version.load(load_dir=self.VERSION_DIR)
    description = self.DESCRIPTION.format(version)
    super().__init__(MainQtView, app_name, version, description, resource_dir=self.RESOURCE_DIR)


if __name__ == "__main__":
  # Application entry point
  Main('Application name').INSTANCE.run(sys.argv[1:])
