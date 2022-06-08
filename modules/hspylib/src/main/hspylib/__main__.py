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

   Copyright 2022, HSPyLib team
"""
import sys

from hspylib.addons.appman.app_extension import AppExtension
from hspylib.addons.appman.app_type import AppType
from hspylib.addons.appman.appman import AppManager
from hspylib.addons.widman.widman import WidgetManager
from hspylib.core.tools.commons import get_path, run_dir, syserr
from hspylib.modules.cli.application.application import Application
from hspylib.modules.cli.application.version import AppVersion

HERE = get_path(__file__)


class Main(Application):
    """HSPyLib Manager - Manage HSPyLib applications."""

    # The welcome message
    DESCRIPTION = (HERE / "welcome.txt").read_text()

    # location of the .version file
    VERSION_DIR = str(HERE)

    def __init__(self, app_name: str):
        version = AppVersion.load(load_dir=self.VERSION_DIR)
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
                .add_argument(
                    'app-name',
                    'the application name', nargs='?') \
                .add_argument(
                    'app-type',
                    'the application type. Appman is going to scaffold a basic app based on this type',
                    choices=['app', 'qt-app', 'widget'], nargs='?') \
                .add_argument(
                    'app-ext',
                    '"gradle" is going to initialize you project with gradle (requires gradle). '
                    '"git" is going to initialize a git repository (requires git)',
                    choices=['git', 'gradle'], nargs='?') \
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
            addon = AppManager(self)
            app_type = self.getarg('app-type')
            if app_type:
                app_ext = self.getarg('app-ext')
                addon.create(
                    self.getarg('app-name'), AppType.of_value(app_type),
                    list(map(AppExtension.value_of, app_ext)),
                    self.getarg('dest-dir') or run_dir())
            else:
                args = addon.prompt()
                if args:
                    app_ext = []
                    if args.initialize_gradle:
                        app_ext.append('gradle')
                    if args.initialize_git:
                        app_ext.append('git')
                    addon.create(
                        args.app_name, AppType.of_value(args.app_type),
                        list(map(AppExtension.value_of, app_ext)),
                        args.dest_dir or run_dir())
        elif app == 'widgets':
            addon = WidgetManager(self)
            widget_name = self.getarg('widget-name')
            if widget_name:
                widget_args = self.getarg('widget-args')
                addon.execute(widget_name, widget_args)
            else:
                addon.dashboard()
        else:
            syserr(f'### Invalid application: {app}')
            self.usage(1)


# Application entry point
if __name__ == "__main__":
    Main('hspylib').INSTANCE.run(sys.argv[1:])
