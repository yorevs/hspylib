#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: hspylib
   @package: hspylib
      @file: __main__.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""
from clitt.core.tui.tui_application import TUIApplication
from hspylib.core.enums.charset import Charset
from hspylib.core.zoned_datetime import now
from hspylib.modules.application.argparse.parser_action import ParserAction
from hspylib.modules.application.exit_status import ExitStatus
from hspylib.modules.application.version import Version
from setman.__classpath__ import _Classpath
from setman.core.setman import Setman
from setman.core.setman_enums import SetmanOps, SettingsType
from textwrap import dedent

import logging as log
import sys


class Main(TUIApplication):
    """HsPyLib CLI Terminal Tools - Create professional CLI applications."""

    # The welcome message
    DESCRIPTION = _Classpath.get_source_path("welcome.txt").read_text(encoding=Charset.UTF_8.val)

    # Location of the .version file
    VERSION_DIR = _Classpath.source_path()

    def __init__(self, app_name: str):
        version = Version.load(load_dir=self.VERSION_DIR)
        super().__init__(app_name, version, self.DESCRIPTION.format(version))
        self._setman = Setman(self)

    def _setup_arguments(self) -> None:
        """Initialize application parameters and options."""

        # fmt: off
        self._with_options() \
            .option(
                'simple', 's', 'simple',
                'display without formatting.', action=ParserAction.STORE_TRUE) \
            .option(
                'preserve', 'p', 'preserve',
            'whether to preserve (no overwrite) existing settings.', action=ParserAction.STORE_TRUE)

        self._with_chained_args('operation', 'the operation to execute.') \
            .argument(SetmanOps.GET.val, 'Retrieve the specified setting.') \
                .add_parameter('name', 'the settings name to get.') \
            .argument(SetmanOps.SET.val, 'Upsert the specified setting.') \
                .add_option('name', 'n', 'name', 'the settings name to set.') \
                .add_option('prefix', 'x', 'prefix', 'the settings prefix to set.') \
                .add_option('value', 'v', 'value', 'the settings value to set.') \
                .add_option('type', 't', 'type', 'the settings type to set.', choices=SettingsType.choices()) \
            .argument(SetmanOps.DEL.val, 'Delete the specified setting.') \
                .add_parameter('name', 'the settings name to delete.') \
            .argument(SetmanOps.LIST.val, 'List in a table all settings matching criteria.') \
                .add_option('name', 'n', 'name', 'filter settings matching name.') \
                .add_option('type', 't', 'type', 'filter settings matching type.', choices=SettingsType.choices()) \
            .argument(SetmanOps.SEARCH.val, 'Search and display all settings matching criteria.') \
                .add_option('name', 'n', 'name', 'filter settings matching name.') \
                .add_option('type', 't', 'type', 'filter settings matching type.', choices=SettingsType.choices()) \
            .argument(SetmanOps.TRUNCATE.val, 'Clear all settings matching name.') \
                .add_option('name', 'n', 'name', 'filter settings matching name.') \
                .add_option('type', 't', 'type', 'filter settings matching type.', choices=SettingsType.choices()) \
            .argument(SetmanOps.IMPORT.val, 'Import settings from a CSV formatted file.') \
                .add_parameter('file', 'the path of the CSV file to be imported.') \
            .argument(SetmanOps.EXPORT.val, 'Export settings to a CSV formatted file.') \
                .add_parameter('file', 'the path of the CSV file to be exported.') \
                .add_option('name', 'n', 'name', 'filter settings matching name.') \
                .add_option('type', 't', 'type', 'filter settings matching type.', choices=SettingsType.choices()) \
            .argument(SetmanOps.SOURCE.val, 'Source (bash export) all environment settings to current shell.') \
                .add_option('name', 'n', 'name', 'filter settings matching name.') \
                .add_option('file', 'f', 'file', 'the output file containing the bash exports.')
        # fmt: on

    def _main(self, *params, **kwargs) -> ExitStatus:
        """Run the application with the command line arguments."""
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
        """Execute the application main flow."""
        op = self.get_arg("operation")
        st = self.get_arg("type")
        return self._setman.execute(
            SetmanOps.of_value(op) if op else None,
            self.get_arg("name"),
            self.get_arg("prefix"),
            self.get_arg("value"),
            SettingsType.of_value(st) if st else None,
            self.get_arg("simple"),
            self.get_arg("preserve"),
            self.get_arg("file"),
        )


# Application entry point
if __name__ == "__main__":
    Main("setman").INSTANCE.run(sys.argv[1:])
