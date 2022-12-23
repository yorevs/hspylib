#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib-Firebase
   @package: firebase
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

import urllib3
from clitt.core.tui.tui_application import TUIApplication
from hspylib.core.enums.charset import Charset
from hspylib.core.tools.commons import syserr
from hspylib.core.zoned_datetime import now
from hspylib.modules.application.exit_status import ExitStatus
from hspylib.modules.application.version import Version

from firebase.__classpath__ import _Classpath
from firebase.core.firebase import Firebase

# Disable this warning because we are hitting our own database
urllib3.disable_warnings()


class Main(TUIApplication):
    """Firebase Agent - Manage your firebase integration"""

    # The welcome message
    DESCRIPTION = _Classpath.get_source_path("welcome.txt").read_text(encoding=Charset.UTF_8.val)

    # location of the .version file
    VERSION_DIR = _Classpath.source_path()

    # The resources folder
    RESOURCE_DIR = str(_Classpath.resource_path())

    def __init__(self, app_name: str):
        version = Version.load(load_dir=self.VERSION_DIR)
        super().__init__(app_name, version, self.DESCRIPTION.format(version), resource_dir=self.RESOURCE_DIR)
        self.firebase = Firebase()

    def _setup_arguments(self) -> None:
        # fmt: off
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
            .add_parameter('db_alias', 'alias to identify the firebase object to fetch') \
                .add_parameter('files', 'list of files to upload (separated by a space)', nargs='*') \
            .argument('download', 'download files from your Firebase Realtime Database') \
                .add_option(
                    'dest-dir', 'd', 'dest-dir',
                    'the destination directory. If omitted, the current directory will be used.',
                    nargs='?', default=self._run_dir) \
            .add_parameter('db_alias', 'alias to identify the firebase object to fetch')
        # fmt: on

    def _main(self, *params, **kwargs) -> ExitStatus:
        """Run the application with the command line arguments"""
        log.info(
            dedent(
                f"""
        {self._app_name} v{self._app_version}
        Settings ==============================
                STARTED: {now("%Y-%m-%d %H:%M:%S")}
        """
            )
        )
        return self._exec_application()

    def _exec_application(self) -> ExitStatus:
        """Execute the specified firebase operation"""
        op = self.get_arg("operation")
        if op == "setup" or not self.firebase.is_configured():
            self.firebase.setup()
        # Already handled above
        if op == "setup":
            log.debug("Operation is setup but it was already handled")
        elif op == "upload":
            self.firebase.upload(self.get_arg("db_alias"), self.get_arg("files"), self.get_arg("glob"))
        elif op == "download":
            self.firebase.download(self.get_arg("db_alias"), self.get_arg("dest-dir"))
        else:
            syserr(f"### Unhandled operation: {op}")
            self.usage(ExitStatus.FAILED)
        return ExitStatus.SUCCESS


if __name__ == "__main__":
    # Application entry point
    Main("firebase").INSTANCE.run(sys.argv[1:])
