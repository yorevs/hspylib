#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: hspylib
   @package: main.hspylib
      @file: __main__.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
import sys

from hspylib.__classpath__ import _Classpath
from hspylib.addons.appman.appman import AppManager
from hspylib.addons.appman.appman_enums import AppType, Extension
from hspylib.addons.widman.widman import WidgetManager
from hspylib.core.enums.charset import Charset
from hspylib.core.enums.enumeration import Enumeration
from hspylib.core.tools.commons import run_dir, syserr
from hspylib.core.tools.text_tools import strip_linebreaks
from hspylib.modules.cli.application.application import Application
from hspylib.modules.cli.application.version import Version


class Main(Application):
    """HSPyLib Manager - Manage HSPyLib applications."""

    # The welcome message
    DESCRIPTION = _Classpath.get_source_path_path("welcome.txt").read_text(encoding=str(Charset.UTF_8))

    # Location of the .version file
    VERSION_DIR = _Classpath.source_root()

    class Addon(Enumeration):
        """TODO"""
        APPMAN = 'appman'
        WIDGETS = 'widgets'

    def __init__(self, app_name: str):
        version = Version.load(load_dir=self.VERSION_DIR)
        super().__init__(app_name, version, self.DESCRIPTION.format(version))

    def _setup_arguments(self) -> None:
        """Initialize application parameters and options"""

        # @formatter:off
        self._with_chained_args('application', 'the HSPyLib application to run') \
            .argument(self.Addon.APPMAN.value, 'app Application Manager: Create HSPyLib based python applications') \
                .add_option(
                    'dest-dir', 'd', 'dest-dir',
                    'the destination directory. If omitted, the current directory will be used.',
                    nargs='?', default=self._run_dir) \
                .add_argument(
                    'app-name',
                    'the application name', nargs='?') \
                .add_argument(
                    'app-type',
                    'the application type. Appman is going to scaffold a basic application based on the app type',
                    choices=[
                        AppType.APP.value, AppType.QT_APP.value, AppType.WIDGET.value
                    ], nargs='?') \
                .add_argument(
                    'app-ext',
                    '"gradle" is going to initialize you project with gradle (requires gradle). '
                    '"git" is going to initialize a git repository (requires git)',
                    nargs='*') \
            .argument(self.Addon.WIDGETS.value, 'app Widgets Manager: Execute an HSPyLib widget') \
                .add_argument(
                    'widget-name',
                    'the name of the widget to be executed. If omitted, all available widgets will be '
                    'presented in a dashboard',
                    nargs='?') \
                .add_argument(
                    'widget-args', "the widget's arguments (if applicable)",
                    nargs='*') \
            # @formatter:on

    def _main(self, *params, **kwargs) -> int:
        """Main entry point handler"""
        self._run()
        return 0

    def _run(self) -> None:
        """Execute the application"""

        app = self.get_arg('application')
        if app == self.Addon.APPMAN.value:
            addon = AppManager(self)
            app_type = self.get_arg('app-type')
            if app_type:
                app_ext = self.get_arg('app-ext')
                addon.create(
                    self.get_arg('app-name'), AppType.of_value(app_type),
                    list(map(Extension.value_of, app_ext)) if app_ext else [],
                    self.get_arg('dest-dir') or run_dir())
            else:
                args = addon.prompt()
                if args:
                    app_ext = []
                    if args.initialize_gradle:
                        app_ext.append(Extension.GRADLE)
                    if args.initialize_git:
                        app_ext.append(Extension.GIT)
                    addon.create(
                        args.app_name, AppType.of_value(args.app_type),
                        list(app_ext),
                        args.dest_dir or run_dir())
        elif app == self.Addon.WIDGETS.value:
            addon = WidgetManager(self)
            widget_name = self.get_arg('widget-name')
            if widget_name:
                widget_args = list(map(strip_linebreaks, self.get_arg('widget-args')))
                addon.execute(widget_name, widget_args)
            else:
                addon.dashboard()
        else:
            syserr(f'### Invalid application: {app}')
            self.usage(1)


# Application entry point
if __name__ == "__main__":
    Main('hspylib').INSTANCE.run(sys.argv[1:])
