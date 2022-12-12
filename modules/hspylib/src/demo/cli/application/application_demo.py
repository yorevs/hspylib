#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: demo.cli.application
      @file: application_demo.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
import sys

from hspylib.core.enums.exit_status import ExitStatus
from hspylib.core.tools.commons import sysout
from hspylib.modules.application.application import Application
from hspylib.modules.application.version import Version

APP_NAME = 'AppTest'

DESCRIPTION = "HsPyLib application Demo"

EPILOG = "This is just a simple application demo"


class Main(Application):

    def _setup_arguments(self) -> None:
        # @formatter:off
        self._with_options()\
            .option('verbose', 'V', 'verbose', 'to be more verbose')
        self._with_chained_args('operation', 'Upload/Download files from/to server') \
            .argument('download', 'download a file from server') \
                .add_argument('url', 'the url of the file') \
            .argument('upload', 'upload a file to server') \
                .add_argument('source', 'the source file') \
                .add_argument('url', 'the url of the file') \
        # @formatter:on

    def _main(self, *params, **kwargs) -> ExitStatus:
        return self._exec_application()

    def _exec_application(self) -> ExitStatus:
        """Execute the application logic."""
        if self.get_arg('operation') == 'download':
            print('Downloading')
        elif self.get_arg('operation') == 'upload':
            print('Uploading')

        status = ExitStatus.SUCCESS
        sysout(f'{repr(status)}, running from {self._run_dir}')
        return status

    def _cleanup(self) -> None:
        pass

if __name__ == "__main__":
    # Application entry point
    Main('AppTest', Version.load(), DESCRIPTION, epilog=EPILOG).INSTANCE.run(sys.argv[1:])
