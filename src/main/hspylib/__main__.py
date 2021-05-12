#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.main.hspylib
      @file: __main__.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

import sys

from hspylib.addins.appman.appman import AppManager
from hspylib.core.tools.commons import get_path, read_version, run_dir, syserr, sysout
from hspylib.modules.cli.application.application import Application
from hspylib.modules.cli.application.argument_chain import ArgumentChain

HERE = get_path(__file__)


class Main(Application):
    """HSPyLib Manager v{} - Manage HSPyLib applications."""
    
    # The hspylib version
    VERSION = read_version(f"{HERE}/.version")
    
    # HSPyLib manager usage message
    USAGE = (HERE / "usage.txt").read_text().format('.'.join(map(str, VERSION)))
    
    # The welcome message
    WELCOME = (HERE / "welcome.txt").read_text()
    
    def __init__(self, app_name: str):
        super().__init__(app_name, self.VERSION, self.USAGE)
    
    def _setup_parameters(self, *params, **kwargs) -> None:
        """Initialize application parameters and options"""
        if len(*params) == 0:
            welcome = self.WELCOME
            sysout(f"{welcome}")
            self.usage()
        else:
            # @formatter:off
            self._with_arguments(
                ArgumentChain.builder()
                    .when('Operation', 'create')
                    .require('AppName', '.+')
                    .require('MngType', 'basic|gradle|git|all')
                    .accept('DestDir', '.+')
                    .end()
                    .build()
            )
            # @formatter:on
    
    def _main(self, *params, **kwargs) -> None:
        """Main entry point handler"""
        self._exec_application()
    
    def _exec_application(self) -> None:
        """Execute the application"""
        op = self.args[0]
        if op == 'create':
            manager = AppManager(self)
            manager.create_app(
                self.args[1],
                AppManager.AppType.value_of(self.args[2], ignore_case=True),
                self.args[3] if len(self.args) > 3 else run_dir())
        else:
            syserr('### Invalid operation: {}'.format(op))
            self.usage(1)


# Application entry point
if __name__ == "__main__":
    # Application entry point
    Main('HSPyLib Manager').INSTANCE.run(sys.argv[1:])
