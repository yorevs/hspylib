#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.app.firebase.src.main
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

import urllib3
from hspylib.core.tools.commons import get_path, syserr
from hspylib.modules.cli.application.application import Application
from hspylib.modules.cli.application.version import AppVersion

from firebase.core.firebase import Firebase

# Disable this warning because we are hitting our own database
urllib3.disable_warnings()

HERE = get_path(__file__)


class Main(Application):
    """Firebase Agent - Manage your firebase integration"""

    # The welcome message
    DESCRIPTION = (HERE / "welcome.txt").read_text()

    # location of the .version file
    VERSION_DIR = str(HERE)

    # The resources folder
    RESOURCE_DIR = str(HERE / "resources")

    def __init__(self, app_name: str):
        version = AppVersion.load(load_dir=self.VERSION_DIR)
        super().__init__(app_name, version, self.DESCRIPTION.format(version), resource_dir=self.RESOURCE_DIR)
        self.firebase = Firebase()

    def _setup_arguments(self) -> None:
        # @formatter:off
        self._with_options() \
            .option(
                'config-dir', 'd', 'config-dir',
                "the configuration directory. If omitted, the User's home will be used.",
                nargs='?', default=os.getenv('HOME', self._run_dir))
        self._with_chained_args('operation', 'the Firebase operation to process') \
            .argument('setup', 'setup your Firebase account') \
            .argument('upload', 'upload files to your Firebase Realtime Database') \
                .add_option(
                    'dest-dir', 'd', 'dest-dir',
                    'the destination directory. If omitted, the current directory will be used.',
                    nargs='?', default=self._run_dir) \
            .add_option(
                    'glob', 'g', 'glob',
                    'filter path names matching a specified glob pattern.',
                    nargs='?') \
            .add_argument('db_alias', 'alias to identify the firebase object to fetch') \
                .add_argument('files', 'list of files to upload (separated by a space)', nargs='*') \
            .argument('download', 'download files from your Firebase Realtime Database') \
                .add_option(
                    'dest-dir', 'd', 'dest-dir',
                    'the destination directory. If omitted, the current directory will be used.',
                    nargs='?', default=self._run_dir) \
            .add_argument('db_alias', 'alias to identify the firebase object to fetch') \
        # @formatter:on

    def _main(self, *params, **kwargs) -> None:
        """Run the application with the command line arguments"""
        log.info(dedent('''
        {} v{}
        Settings ==============================
                STARTED: {}
        ''').format(
            self._app_name, self._app_version,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        self._exec_application()

    def _exec_application(self) -> None:
        """Execute the specified firebase operation"""
        op = self.getarg('operation')
        if op == 'setup' or not self.firebase.is_configured():
            self.firebase.setup()
        # Already handled above
        if op == 'setup':
            pass
        elif op == 'upload':
            self.firebase.upload(
                self.getarg('db_alias'),
                self.getarg('files'),
                self.getarg('glob'))
        elif op == 'download':
            self.firebase.download(
                self.getarg('db_alias'),
                self.getarg('dest-dir')
            )
        else:
            syserr(f'### Unhandled operation: {op}')
            self.usage(1)


if __name__ == "__main__":
    # Application entry point
    Main('firebase').INSTANCE.run(sys.argv[1:])
