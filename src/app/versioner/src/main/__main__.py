#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   hspylib.app.versioner.src.main
      @file: __main__.py
   @created: Tue, 11 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

import sys

from hspylib.core.tools.commons import get_path, read_version, sysout, syserr
from hspylib.core.tools.regex_constants import RegexConstants
from hspylib.modules.cli.application.application import Application
from hspylib.modules.cli.application.argument_chain import ArgumentChain
from versioner.src.main.core.versioner import Versioner
from versioner.src.main.enums.part import Part

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
        """Initialize application parameters and options"""
        self._with_option('b', 'backup', True)
        self._with_option('d', 'search-dir', True)
        # @formatter:off
        self._with_arguments(
            ArgumentChain.builder()
                .when('version', RegexConstants.RE_VERSION_STRING)
                .require('part', '|'.join(list(map(str.lower, Part.names()))))
                .require('files', '.*')
                .end()
              .build()
        )
        # @formatter:on

    def _main(self, *params, **kwargs) -> None:
        """Run the application with the command line arguments"""
        self.versioner = Versioner(self.getarg('version'), self.getopt('search-dir'), self.getarg('files').split(','))
        self._exec_application()

    def _exec_application(self) -> None:
        """Execute the application"""
        caller = getattr(self.versioner, self.getarg('part'))
        caller()
        if self.versioner.save(self.getopt('backup')):
            sysout(f"%GREEN%Successfully updated version to {self.versioner.version()} %NC%")
        else:
            syserr(f"%RED%Failed to update version. No matches found for version {self.getarg('version')} %NC%")


if __name__ == "__main__":
    # Application entry point
    Main('HSPyLib Cloud Foundry Manager').INSTANCE.run(sys.argv[1:])
