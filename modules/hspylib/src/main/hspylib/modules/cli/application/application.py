#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: main.modules.cli.application
      @file: application.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""
import argparse
import atexit
import logging as log
import os
import signal
import sys
from abc import abstractmethod
from datetime import datetime
from typing import Optional, Tuple

from core.config.app_config import AppConfigs
from core.exception.exceptions import InvalidArgumentError, InvalidOptionError
from core.metaclass.singleton import Singleton
from core.tools.commons import sysout, get_path
from modules.cli.application.argument_parser import HSArgumentParser
from modules.cli.application.arguments_builder import ArgumentsBuilder
from modules.cli.application.options_builder import OptionsBuilder
from src.main.hspylib.modules.cli.application.chained_arguments_builder import ChainedArgumentsBuilder


class Application(metaclass=Singleton):
    """HSPyLib application framework"""

    @staticmethod
    def exit_handler(signum=0, frame=None, clear_screen: bool = False) -> None:
        """
        Handle interruptions to shutdown gracefully
        :param signum: The signal number or the exit code
        :param frame: The frame raised by the signal
        :param clear_screen: Whether to clean the screen before execution or not
        """
        if frame is not None:
            log.warning('Signal handler hooked signum=%d frame=%s', signum, frame)
            exit_code = 3
        else:
            log.info('Exit handler called')
            exit_code = signum
        if clear_screen:
            sysout('%ED2%%HOM%')
        sys.exit(exit_code)

    def __init__(
        self,
        name: str,
        version: Tuple[int, int, int] = None,
        description: str = None,
        usage: str = None,
        epilog: str = None,
        resource_dir: str = None,
        log_dir: str = None):

        signal.signal(signal.SIGINT, self.exit_handler)
        signal.signal(signal.SIGTERM, self.exit_handler)

        self.run_dir = get_path(__file__)
        self._arg_parser = HSArgumentParser(
            prog=name, allow_abbrev=False, description=description, usage=usage, epilog=epilog)
        self._arg_parser.add_argument(
            '-V', '--version', action='version', version=f"%(prog)s v{'.'.join(map(str, version))}")
        self._app_name = name
        self._app_version = version
        self._app_description = description
        self._args = {}

        if os.path.isfile(f'{resource_dir}/application.properties'):
            self.configs = AppConfigs(
                resource_dir=resource_dir,
                log_dir=log_dir
            )

    def run(self, *params, **kwargs) -> None:
        """Main entry point handler"""
        log.info('Run started %s', datetime.now())
        try:
            atexit.register(self._cleanup)
            self._setup_arguments()
            self._args = self._arg_parser.parse_args()
            self._main(*params, **kwargs)
            log.debug(f'Command line arguments: {str(self._args)}')
        except (InvalidOptionError, InvalidArgumentError) as err:
            self.usage(exit_code=1, no_exit=True)
            raise err  # Re-Raise the exception so upper level layers can catch
        finally:
            log.info('Run finished %s', datetime.now())

    def usage(self, exit_code: int = 0, no_exit: bool = False) -> None:
        """Display the usage message and exit with the specified code ( or zero as default )
        :param no_exit: Do no exit the application on usage call
        :param exit_code: The exit code
        """
        self._arg_parser.print_help(sys.stderr if exit_code != 0 else sys.stdout)
        if not no_exit:
            self.exit_handler(exit_code)

    def getarg(self, arg_name: str) -> Optional[str]:
        """Get the argument value named by the opt_name"""
        arg = getattr(self._args, arg_name) if self._args and hasattr(self._args, arg_name) else []
        return arg[0] if arg else None

    @abstractmethod
    def _setup_arguments(self) -> None:
        """Initialize application parameters and options"""

    def _with_options(self) -> 'OptionsBuilder':
        return OptionsBuilder(self._arg_parser)

    def _with_arguments(self) -> 'ArgumentsBuilder':
        return ArgumentsBuilder(self._arg_parser)

    def _with_chained_args(self, subcommand_name: str, subcommand_help: str) -> 'ChainedArgumentsBuilder':
        return ChainedArgumentsBuilder(self._arg_parser, subcommand_name, subcommand_help)

    def _main(self, *params, **kwargs) -> None:
        """Execute the application's main statements"""

    def _cleanup(self) -> None:
        """Execute code cleanup before exiting"""
