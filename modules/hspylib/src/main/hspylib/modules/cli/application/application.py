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
from textwrap import dedent
from typing import Optional, Union

from hspylib.core.config.app_config import AppConfigs
from hspylib.core.exception.exceptions import InvalidArgumentError, InvalidOptionError
from hspylib.core.metaclass.singleton import Singleton
from hspylib.core.tools.commons import log_init, sysout
from hspylib.core.tools.preconditions import check_state
from hspylib.modules.cli.application.argument_parser import HSArgumentParser
from hspylib.modules.cli.application.arguments_builder import ArgumentsBuilder
from hspylib.modules.cli.application.chained_arguments_builder import ChainedArgumentsBuilder
from hspylib.modules.cli.application.exit_hooks import ExitHooks
from hspylib.modules.cli.application.options_builder import OptionsBuilder
from hspylib.modules.cli.application.version import AppVersion


class Application(metaclass=Singleton):
    """HSPyLib application framework"""

    @staticmethod
    def exit(signum=0, frame=None, clear_screen: bool = False) -> None:
        """
        Handle interruptions to shutdown gracefully
        :param signum: The signal number or the exit http_code
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
        version: AppVersion,
        description: str = None,
        usage: str = None,
        epilog: str = None,
        resource_dir: str = None,
        log_dir: str = None):

        signal.signal(signal.SIGINT, self.exit)
        signal.signal(signal.SIGTERM, self.exit)

        self.exit_hooks = ExitHooks()
        self.exit_hooks.hook()
        self._run_dir = os.getcwd()
        self._app_name = name
        self._app_version = version
        self._app_description = description
        self._arg_parser = HSArgumentParser(
            exit_on_error=False, prog=name, allow_abbrev=False,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description=dedent(description or ''), usage=usage,
            epilog=dedent(epilog or ''))
        self._arg_parser.add_argument(
            '-v', '--version', action='version', version=f"%(prog)s v{self._app_version}")
        self._args = {}

        # Initialize application configs
        if os.path.exists(f'{resource_dir}'):
            self.configs = AppConfigs(resource_dir=resource_dir, log_dir=log_dir)
        elif not resource_dir and os.path.exists(f'{self._run_dir}/resources/application.properties'):
            self.configs = AppConfigs(resource_dir=f'{self._run_dir}/resources', log_dir=log_dir)
        else:
            pass  # AppConfigs will not be available

        # Initialize application logs
        log_file = f"{log_dir or os.getenv('LOG_DIR', os.getcwd())}/{name}.log"
        check_state(log_init(log_file), "Unable to initialize logging. log_file={}", log_file)

    def run(self, *params, **kwargs) -> None:
        """Main entry point handler"""
        log.info('Run started %s', datetime.now())
        try:

            atexit.register(self._cleanup)
            self._setup_arguments()
            self._args = self._arg_parser.parse_args(*params)
            self._main(*params, **kwargs)
            log.debug(f'Command line arguments: {str(self._args)}')
        except (InvalidOptionError, InvalidArgumentError) as err:
            self.usage(exit_code=1, no_exit=True)
            raise err  # Re-Raise the exception so upper level layers can catch
        finally:
            log.info('Run finished %s', datetime.now())

    def usage(self, exit_code: int = 0, no_exit: bool = False) -> None:
        """Display the usage message and exit with the specified http_code ( or zero as default )
        :param no_exit: Do no exit the application on usage call
        :param exit_code: The exit http_code
        """
        self._arg_parser.print_help(sys.stderr if exit_code != 0 else sys.stdout)
        if not no_exit:
            self.exit(exit_code)

    def version(self) -> str:
        """Return the application version"""
        return str(self._app_version)

    def name(self) -> str:
        """Return the application name"""
        return self._app_name

    def getarg(self, arg_name: str) -> Optional[Union[str, list]]:
        """Get the argument value named by arg_name"""
        return getattr(self._args, arg_name) if self._args and hasattr(self._args, arg_name) else None

    @abstractmethod
    def _setup_arguments(self) -> None:
        """Initialize application parameters and options"""

    def _with_options(self) -> 'OptionsBuilder':
        """TODO"""
        return OptionsBuilder(self._arg_parser)

    def _with_arguments(self) -> 'ArgumentsBuilder':
        """TODO"""
        return ArgumentsBuilder(self._arg_parser)

    def _with_chained_args(self, subcommand_name: str, subcommand_help: str = None) -> 'ChainedArgumentsBuilder':
        return ChainedArgumentsBuilder(self._arg_parser, subcommand_name, subcommand_help)

    def _main(self, *params, **kwargs) -> None:
        """Execute the application's main statements"""

    def _cleanup(self) -> None:
        """Execute http_code cleanup before exiting"""
