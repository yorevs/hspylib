#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: hspylib.main.hspylib.modules.cli.application
      @file: application.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""
import atexit
import getopt
import logging as log
import signal
import sys
from datetime import datetime
from typing import Callable, List, Optional, Set, Tuple

from hspylib.core.config.app_config import AppConfigs
from hspylib.core.exception.exceptions import InvalidArgumentError, InvalidOptionError
from hspylib.core.metaclass.singleton import Singleton
from hspylib.core.tools.commons import sysout
from hspylib.modules.cli.application.argument import Argument
from hspylib.modules.cli.application.argument_chain import ArgumentChain
from hspylib.modules.cli.application.option import Option


class Application(metaclass=Singleton):
    """HSPyLib application framework"""

    VERSION = None
    USAGE = None

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
        app_name: str = None,
        app_version: Tuple[int, int, int] = None,
        app_usage: str = None,
        source_dir: str = None,
        resource_dir: str = None,
        log_dir: str = None):

        signal.signal(signal.SIGINT, self.exit_handler)
        signal.signal(signal.SIGTERM, self.exit_handler)

        self._app_name = app_name
        self._app_version = app_version
        self._app_usage = app_usage
        self._options = {}
        self._arguments = []
        self._args = {}
        self._opts = {}

        if source_dir:
            self.configs = AppConfigs(
                source_root=source_dir,
                resource_dir=resource_dir,
                log_dir=log_dir
            )
        if app_usage:
            self._with_option('h', 'help', handler=self.usage)
        if app_version:
            self._with_option('v', 'version', handler=self.version)

    def run(self, *params, **kwargs) -> None:
        """Main entry point handler"""
        log.info('Run started %s', datetime.now())
        try:
            atexit.register(self._cleanup)
            self._setup_parameters(*params, **kwargs)
            self._parse_parameters(*params, **kwargs)
            self._main(*params, **kwargs)
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
        sysout(self._app_usage)
        if not no_exit:
            self.exit_handler(exit_code)

    def version(self, exit_code: int = 0, no_exit: bool = False) -> None:
        """Display the current program version and exit
        :param no_exit: Do no exit the application on usage call
        :param exit_code: The exit code
        """
        sysout('{} v{}'.format(self._app_name, '.'.join(map(str, self._app_version))))
        if not no_exit:
            self.exit_handler(exit_code)

    def getopt(self, opt_name: str) -> Optional[str]:
        """Get the option value named by the opt_name"""
        return next((val for opt, val in self._opts.items() if opt == opt_name), None)

    def getarg(self, arg_name: str) -> Optional[str]:
        """Get the argument value named by the opt_name"""
        return next((val for arg, val in self._args.items() if arg == arg_name), None)

    def _setup_parameters(self, *params, **kwargs) -> None:  # pylint: disable=unused-argument,no-self-use
        """Initialize application parameters and options"""
        log.info('setup_parameters was not overridden')

    def _main(self, *params, **kwargs) -> None:  # pylint: disable=unused-argument,no-self-use
        """Execute the application's main statements"""
        log.info('main was not overridden')

    def _cleanup(self) -> None:  # pylint: disable=no-self-use
        """Execute code cleanup before exiting"""
        log.info('cleanup was not overridden')

    def _with_option(
        self,
        shortopt: chr,
        longopt: str,
        has_argument: bool = False,
        handler: Callable = None) -> None:
        """Specify an option for the command line"""
        self._options[longopt] = Option(shortopt, longopt, has_argument, handler)

    def _with_arguments(
        self,
        chained_args: Set[ArgumentChain.ChainedArgument]) -> None:
        """Specify an argument for the command line"""
        self._arguments = chained_args

    def _parse_parameters(self, parameters: List[str]) -> None:
        """ Handle program parameters.
        :param parameters: The list of unparsed program parameters passed by the command line
        """
        # First parse all options, then, arguments
        self._parse_arguments(self._parse_options(parameters))

    def _parse_options(self, parameters: List[str]) -> List[str]:
        """Handle program options in the form: Short opts: -<C>, Long opts: --<Word>
        :param parameters: The list of unparsed program parameters passed by the command line
        :return A list of remaining arguments
        """
        try:
            opts, args = getopt.getopt(parameters, self._shortopts(), self._longopts())
            for op, arg in opts:
                option = self._find_option(op)
                if option:
                    if option.cb_handler:
                        option.cb_handler(arg)
                    self._opts[option.name] = arg
                else:
                    raise InvalidOptionError(f'Option "{op}" not recognized')
            return args
        except getopt.GetoptError as err:
            raise InvalidOptionError(f"### Invalid option: {str(err)}") from err

    def _find_option(self, item: str) -> Optional[Option]:
        """Getter for application option"""
        return next((op for key, op in self._options.items() if op == item), None)

    def _parse_arguments(self, provided_args: List[str]) -> None:
        """Handle program arguments
        :param provided_args: Arguments left after processing all options
        """
        valid = False
        if self._arguments:
            # Walk through all argument conditions in chain and validate the provided arguments
            for argument in self._arguments:
                arg = argument.argument
                try:
                    self._args = {}
                    self._recursive_set(0, arg, provided_args)
                    # At this point, we found a valid argument chain
                    valid = Argument.validate_chained_args(arg)
                    # Will be true if all required args were set
                    break
                except getopt.GetoptError as err:
                    log.debug(str(err))
                    continue  # Log and try next argument in chain
                except LookupError as err:
                    log.debug(str(err))
                    continue  # Log and try next argument in chain
            if not valid:
                raise InvalidArgumentError(f"Invalid arguments [\"{', '.join(provided_args)}\"]")

    def _recursive_set(self, idx: int, argument: Argument, provided_args: List[str]) -> None:
        """ Try to set a value for each provided argument. If any failure setting occur, raise an exception to be caught
            by the parse function, so they can try the next chain in the loop.
        """
        if not argument or idx >= len(provided_args):
            return
        if not argument.set_value(provided_args[idx]):
            raise LookupError(
                f'Invalid argument "{provided_args[idx]}"')
        self._args[argument.name] = \
            provided_args[idx] if argument.next_in_chain else ','.join(provided_args[idx:])
        self._recursive_set(idx + 1, argument.next_in_chain, provided_args)

    def _shortopts(self) -> str:
        return ''.join([op.shortopt.replace('-', '') for key, op in self._options.items()])

    def _longopts(self) -> List[str]:
        return [op.longopt.replace('--', '') + ' ' for key, op in self._options.items()]
