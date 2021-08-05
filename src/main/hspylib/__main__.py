#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   hspylib.main.hspylib
      @file: __main__.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

import sys

from hspylib.addons.appman.app_extension import AppExtension
from hspylib.addons.appman.app_type import AppType
from hspylib.addons.appman.appman import AppManager
from hspylib.addons.widman.widman import WidgetManager
from hspylib.core.tools.commons import get_path, read_version, run_dir, syserr, sysout, dirname
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
        super().__init__(app_name, self.VERSION, self.USAGE, dirname(__file__))

    def _setup_parameters(self, *params, **kwargs) -> None:
        """Initialize application parameters and options"""
        if len(*params) == 0:
            welcome = self.WELCOME
            sysout(f"{welcome}")
            self.usage()
        else:
            # @formatter:off
            self._with_option('d', 'dest-dir', True)
            self._with_arguments(
                ArgumentChain.builder()
                    .when('operation', 'appman')
                        .require('app-name', '.+')
                        .require('app-type', '|'.join(AppType.values()))
                        .accept('app_ext', '.+')
                        .end()
                    .when('operation', 'widgets')
                        .accept('widget-name', '.+')
                        .accept('widget-args', '.+')
                        .end()
                    .build()
            )
            # @formatter:on

    def _main(self, *params, **kwargs) -> None:
        """Main entry point handler"""
        self._exec_application()

    def _exec_application(self) -> None:
        """Execute the application"""
        op = self.getarg('operation')
        if op == 'appman':
            manager = AppManager(self)
            app_type = AppType.of_value(self.getarg('app-type'))
            app_ext = self.getarg('app_ext').split(',') if self.getarg('app_ext') else []
            manager.create(
                self.getarg('app-name'),
                app_type,
                list(map(AppExtension.value_of, app_ext)),
                self.getopt('dest-dir') or run_dir())
        elif op == 'widgets':
            manager = WidgetManager(self)
            widget_name = self.getarg('widget-name')
            if widget_name:
                widget_args = str(self.getarg('widget-args')).split(',')
                manager.execute(widget_name, widget_args)
            else:
                manager.dashboard()
        else:
            syserr('### Invalid operation: {}'.format(op))
            self.usage(1)


# Application entry point
if __name__ == "__main__":
    Main('HSPyLib Manager').INSTANCE.run(sys.argv[1:])
