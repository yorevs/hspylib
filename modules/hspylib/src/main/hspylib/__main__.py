#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   main.hspylib
      @file: __main__.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""
import sys

from addons.appman.app_extension import AppExtension
from addons.appman.app_type import AppType
from addons.appman.appman import AppManager
from addons.widman.widman import WidgetManager
from core.tools.commons import get_path, run_dir, syserr
from modules.cli.application.application import Application
from modules.cli.application.version import AppVersion

HERE = get_path(__file__)


class Main(Application):
    """HSPyLib Manager - Manage HSPyLib applications."""

    # The usage message
    USAGE = 'hspylib [application] <operation> <arguments>'

    # The welcome message
    DESCRIPTION = (HERE / "welcome.txt").read_text()

    def __init__(self, app_name: str):
        version = AppVersion.load()
        super().__init__(app_name, version, self.DESCRIPTION.format(version))

    def _setup_arguments(self) -> None:
        """Initialize application parameters and options"""
        # @formatter:off
        self._with_chained_args('application', 'the HSPyLib application to run') \
            .argument('appman', 'app Application Manager: Create HSPyLib based python applications') \
                .add_option(
                    'dest-dir', 'd', 'dest-dir',
                    'the destination directory. If omitted, the current directory will be used.',
                    nargs='?', default=self._run_dir) \
                .add_argument('app-name', 'the application name') \
                .add_argument(
                    'app-type',
                    'the application type. Appman is going to scaffold a basic app based on this type',
                    choices=['app', 'qt-app', 'widget']) \
                .add_argument(
                    'app-ext',
                    '"gradle" is going to initialize you project with gradle (requires gradle). '
                    '"git" is going to initialize a git repository (requires git)',
                    nargs="+", choices=['git', 'gradle'], default=["git", "gradle"]) \
            .argument('widgets', 'app Widgets Manager: Execute an HSPyLib widget') \
                .add_argument(
                    'widget-name',
                    'the name of the widget to be executed. If omitted, all available widgets will be '
                    'presented in a dashboard',
                    nargs='?') \
                .add_argument('widget-args', "the widget's arguments (if applicable)", nargs='*') \
            # @formatter:on

    def _main(self, *params, **kwargs) -> None:
        """Main entry point handler"""
        self._exec_application()

    def _exec_application(self) -> None:
        """Execute the application"""
        app = self.getarg('application')
        if app == 'appman':
            manager = AppManager(self)
            app_type = AppType.of_value(self.getarg('app-type'))
            app_ext = self.getarg('app-ext')
            manager.create(
                self.getarg('app-name'),
                app_type,
                list(map(AppExtension.value_of, app_ext)),
                self.getarg('dest-dir') or run_dir())
        elif app == 'widgets':
            manager = WidgetManager(self)
            widget_name = self.getarg('widget-name')
            if widget_name:
                widget_args = self.getarg('widget-args')
                manager.execute(widget_name, widget_args)
            else:
                manager.dashboard()
        else:
            syserr(f'### Invalid application: {app}')
            self.usage(1)


# Application entry point
if __name__ == "__main__":
    Main('hspylib').INSTANCE.run(sys.argv[1:])
