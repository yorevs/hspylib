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

   Copyright 2021, HSPyLib team
"""

from modules.cli.application.application import Application
from modules.cli.application.argument_chain import ArgumentChain


class ApplicationTest(Application):
    """Versioner - Provides an engine to manage app versions."""

    # The application version
    VERSION = (0, 0, 1)

    # CloudFoundry manager usage message
    USAGE = 'Usage: Its just a test'

    # The welcome message
    WELCOME = 'Welcome to test app'

    def __init__(self, app_name: str):
        super().__init__(app_name, self.VERSION, self.USAGE)

    def _setup_parameters(self, *params, **kwargs) -> None:
        self._with_option('i', 'input', True)
        self._with_option('o', 'output', True)
        # @formatter:off
        self._with_arguments(
            ArgumentChain.builder()
                .when('amount', 'one|two|three', False)
                    .require('item', 'donut|bagel')
                .end()
                .build()
        )
        # @formatter:on

    def _main(self, *params, **kwargs) -> None:
        """Run the application with the command line arguments"""
        self._exec_application()

    def _exec_application(self) -> None:
        """Execute the application"""
