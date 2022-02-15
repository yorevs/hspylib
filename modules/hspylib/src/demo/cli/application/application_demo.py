#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   demo.cli.application
      @file: application_demo.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""
import sys

from core.tools.commons import sysout
from modules.cli.application.application import Application

APP_NAME = 'AppTest'

VERSION = (0, 1, 0)

DESCRIPTION = "HsPyLib application Demo"

EPILOG = "This is just a simple application demo"


class Main(Application):

    def _setup_arguments(self) -> None:
        # @formatter:off
        self._with_options()\
            .option('verbose', 'v', 'verbose', 'to be more verbose')
        self._with_chained_args('operation', 'Upload/Download files from/to server')\
            .argument('download', 'download a file from server') \
                .add_argument('url', 'the url of the file') \
            .argument('upload', 'upload a file to server') \
                .add_argument('source', 'the source file') \
                .add_argument('url', 'the url of the file') \
        # @formatter:on

    def _main(self, *params, **kwargs) -> None:
        self._exec_application()

    def _exec_application(self) -> None:
        if self.getarg('operation') == 'download':
            print('Downloading')
        elif self.getarg('operation') == 'upload':
            print('Uploading')

        sysout(f'Done, running from {self.run_dir}')


if __name__ == "__main__":
    # Application entry point
    Main('AppTest', VERSION, DESCRIPTION, epilog=EPILOG).INSTANCE.run(sys.argv[1:])
