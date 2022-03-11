#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.versioner.src.main
      @file: __main__.py
   @created: Tue, 11 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""
import logging as log
import sys
from datetime import datetime
from textwrap import dedent

from hspylib.core.tools.commons import get_path, syserr, sysout
from hspylib.modules.cli.application.application import Application
from hspylib.modules.cli.application.version import AppVersion
from versioner.core.versioner import Versioner

HERE = get_path(__file__)


class Main(Application):
    """Versioner - Provides an engine to manage app versions."""

    # The welcome message
    DESCRIPTION = (HERE / "welcome.txt").read_text()

    # location of the .version file
    VERSION_DIR = str(HERE)

    def __init__(self, app_name: str):
        version = AppVersion.load(load_dir=self.VERSION_DIR)
        super().__init__(app_name, version, self.DESCRIPTION.format(version))
        self._versioner = None

    def _setup_arguments(self) -> None:
        """Initialize application parameters and options"""
        # @formatter:off
        self._with_options() \
            .option(
                'backup', 'b', 'backup',
                'create a backup of the original files using the specified extension', nargs=1) \
            .option(
                'search-dir', 'd', 'search-dir',
                'specify the search directory. If omitted, current execution path will be used', nargs=1)
        self._with_chained_args('action', 'what to do with the version') \
            .argument('update', 'increment a version part') \
                .add_argument('part', 'the version part to be updated', choices=['major', 'minor', 'patch']) \
                .add_argument('version', 'the searching version to be updated') \
                .add_argument('files', 'the list of files containing te version to be updated', nargs='*') \
            .argument('promote', 'promote current version') \
                .add_argument('version', 'the searching version to be updated') \
                .add_argument('files', 'the list of files containing te version to be updated', nargs='*') \
            .argument('demote', 'demote current version') \
                .add_argument('version', 'the searching version to be updated') \
                .add_argument('files', 'the list of files containing te version to be updated', nargs='*')
        # @formatter:on

    def _main(self, *params, **kwargs) -> None:
        """Run the application with the command line arguments"""
        log.info(dedent('''
        {} v{}

        Settings ==============================
                BACKUP: {}
                SEARCH-DIR: {}
                STARTED: {}
        ''').format(
            self._app_name, self._app_version,
            self.getarg('backup'), self.getarg('search-dir'),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        self._versioner = Versioner(
            self.getarg('version'),
            self.getarg('search-dir'),
            self.getarg('files'))

        self._exec_application()

    def _exec_application(self) -> None:
        """Execute the application"""
        if 'update' == self.getarg('action'):
            caller = getattr(self._versioner, self.getarg('part'))
        else:
            caller = getattr(self._versioner, self.getarg('action'))
        caller()
        result = self._versioner.save(self.getarg('backup'))
        if result:
            sysout(f"%GREEN%Successfully updated from version {self.getarg('version')} to {self._versioner.version()}")
            sysout('%ORANGE%Files changed:')
            list(map(lambda r: sysout(f'%BLUE%  |- {r}'), result))
        else:
            syserr(f"%RED%No matches found for version {self.getarg('version')}")


if __name__ == "__main__":
    # Application entry point
    Main('versioner').INSTANCE.run(sys.argv[1:])
