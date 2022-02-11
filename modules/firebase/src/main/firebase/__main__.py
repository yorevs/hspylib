#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   hspylib.app.firebase.src.main
      @file: __main__.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

import logging as log
import sys
from datetime import datetime

from hspylib.core.tools.commons import get_path, read_version, dirname, syserr
from hspylib.modules.cli.application.application import Application
from hspylib.modules.cli.application.argument_chain import ArgumentChain

from src.main.firebase.core.agent_config import AgentConfig
from src.main.firebase.core.firebase import Firebase

HERE = get_path(__file__)


class Main(Application):
    """Firebase Agent - Manage your firebase integration"""

    # The application version
    VERSION = read_version('src/main/.version')

    # Usage message
    USAGE = (HERE / "usage.txt").read_text().format('.'.join(map(str, VERSION)))

    # The welcome message
    WELCOME = (HERE / "welcome.txt").read_text()

    def __init__(self, app_name: str):
        super().__init__(app_name, self.VERSION, self.USAGE, dirname(__file__))
        self.firebase = Firebase()

    def _setup_parameters(self, *params, **kwargs) -> None:
        # @formatter:off
        self._with_option('d', 'dest-dir', True)
        self._with_arguments(
            ArgumentChain.builder()
                .when('operation', 'setup')
                    .end()
                .when('operation', 'upload')
                    .require('db_alias', '.+')
                    .require('files', '.+')
                    .end()
                .when('operation', 'download')
                    .require('db_alias', '.+')
                    .accept('files', '.+')
                    .end()
                .build()
        )
        # @formatter:on

    def _main(self, *params, **kwargs) -> None:
        """Run the application with the command line arguments"""
        log.info(
            self.WELCOME.format(
                self._app_name,
                self.VERSION,
                AgentConfig.INSTANCE.username(),
                AgentConfig.INSTANCE.config_file(),
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
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
                self.getarg('files').split(',')
            )
        elif op == 'download':
            self.firebase.download(
                self.getarg('db_alias'),
                self.getopt('dest-dir')
            )
        else:
            syserr('### Unhandled operation: {}'.format(op))
            self.usage(1)


if __name__ == "__main__":
    # Application entry point
    Main('HSPyLib Firebase Agent').INSTANCE.run(sys.argv[1:])
