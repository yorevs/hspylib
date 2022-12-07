#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   test.shared
      @file: application_test.py
   @created: Thu, 20 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

from hspylib.modules.cli.application.application import Application
from hspylib.modules.cli.application.version import Version


class ApplicationTest(Application):
    """Versioner - Provides an engine to manage app versions."""

    # CloudFoundry manager usage message
    DESCRIPTION = 'Usage: Its just a test'

    # The welcome message
    WELCOME = 'Welcome to test app'

    def __init__(self) -> None:
        super().__init__('AppTest', Version.load(), self.DESCRIPTION)

    def _setup_arguments(self) -> None:
        # @formatter:off
        self._with_options() \
            .option('input', 'i', 'input', required=True) \
            .option('output', 'o', 'output', required=True)
        self._with_arguments() \
            .argument('amount', 'the amount', choices=['one', 'two', 'three']) \
            .argument('item', 'the item', choices=['donut', 'bagel'])
        # @formatter:on

    def _main(self, *params, **kwargs) -> None:
        """Run the application with the command line arguments"""
        self._exec_application()

    def _exec_application(self) -> None:
        """Execute the application"""
        pass

    def _cleanup(self) -> None:
        pass
