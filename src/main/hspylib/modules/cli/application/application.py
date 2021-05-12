#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.main.hspylib.modules.cli.application
      @file: application.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

import getopt
import logging as log
import signal
import sys
from datetime import datetime
from typing import Callable, List, Optional, Set, Tuple

from hspylib.core.config.app_config import AppConfigs
from hspylib.core.exception.exceptions import InvalidArgumentError, InvalidOptionError
from hspylib.core.meta.singleton import Singleton
from hspylib.core.tools.commons import syserr, sysout
from hspylib.modules.cli.application.argument import Argument
from hspylib.modules.cli.application.argument_chain import ArgumentChain
from hspylib.modules.cli.application.option import Option


class Application(metaclass=Singleton):
    """HSPyLib application framework"""
    
    def __init__(
            self,
            app_name: str = None,
            app_version: Tuple[int, int, int] = None,
            app_usage: str = None,
            source_dir: str = None,
            resource_dir: str = None,
            log_dir: str = None):
        
        signal.signal(signal.SIGINT, self.exit_handler)
        self.app_name = app_name
        self.app_version = app_version
        self.app_usage = app_usage
        self.options = {}
        self.cond_args_chain = {}
        self.args = None
        if source_dir:
            self.configs = AppConfigs(
                source_root=source_dir,
                resource_dir=resource_dir,
                log_dir=log_dir
            )
        if app_usage:
            self.with_option('h', 'help', handler=self.usage)
        if app_version:
            self.with_option('v', 'version', handler=self.version)
    
    def run(self, *params, **kwargs) -> None:
        """Main entry point handler"""
        log.info('Run started {}'.format(datetime.now()))
        try:
            self.setup_parameters(*params, **kwargs)
            self._parse_parameters(*params, **kwargs)
            self.main(*params, **kwargs)
            self.exit_handler()
        except (InvalidArgumentError, InvalidOptionError) as err:
            syserr(str(err))
            self.usage(1)
        finally:
            log.info('Run finished {}'.format(datetime.now()))
    
    def exit_handler(self, signum=0, frame=None, clear_screen: bool = False) -> None:
        """
        Handle interruptions to shutdown gracefully
        :param signum: The signal number or the exit code
        :param frame: The frame raised by the signal
        :param clear_screen: Whether to clean the screen before execution or not
        """
        if frame is not None:
            log.warning('Signal handler hooked signum={} frame={}'.format(signum, frame))
            exit_code = 3
        else:
            log.info('Exit handler called')
            exit_code = signum
        self.cleanup()
        if clear_screen:
            sysout('%ED2%%HOM%')
        sys.exit(exit_code)
    
    def usage(self, *args) -> None:
        """Display the usage message and exit with the specified code ( or zero as default )
        :param args: The application arguments
        """
        sysout(self.app_usage)
        self.exit_handler(args[0] if args and len(args) > 0 else 0)
    
    def version(self, *args) -> None:
        """Display the current program version and exit
        :param args: The application arguments
        """
        sysout('{} v{}'.format(self.app_name, '.'.join(map(str, self.app_version))))
        self.exit_handler(args[0] if args and len(args) > 0 else 0)
    
    def get_option(self, item: str) -> Optional[Option]:
        """Getter for application option"""
        return next((op for key, op in self.options.items() if op.is_eq(item)), None)
    
    def get_argument(self, index: int) -> Optional[Argument]:
        """Getter for application arguments"""
        return self.args[index] if self.args and 0 <= index < len(self.args) else None
    
    def setup_parameters(self, *params, **kwargs) -> None:  # pylint: disable=unused-argument,no-self-use
        """Initialize application parameters and options"""
        log.info('setup_parameters was not overridden')
    
    def main(self, *params, **kwargs) -> None:  # pylint: disable=unused-argument,no-self-use
        """Execute the application's main statements"""
        log.info('main was not overridden')
    
    def cleanup(self) -> None:  # pylint: disable=no-self-use
        """Execute code cleanup before exiting"""
        log.info('cleanup was not overridden')
    
    def with_option(
            self,
            shortopt: chr,
            longopt: str,
            has_argument: bool = False,
            handler: Callable = None) -> None:
        """Specify an option for the command line"""
        self.options[longopt] = Option(shortopt, longopt, has_argument, handler)
    
    def with_arguments(
            self,
            chained_args: Set[ArgumentChain.ChainedArgument]) -> None:
        """Specify an argument for the command line"""
        self.cond_args_chain = chained_args
    
    def _parse_parameters(self, parameters: List[str]) -> None:
        """ Handle program parameters.
        :param parameters: The list of unparsed program parameters passed by the command line
        """
        # First parse all options, then, parse arguments
        self._parse_arguments(self._parse_options(parameters))
    
    def _parse_options(self, parameters: List[str]) -> List[str]:
        """Handle program options in the form: Short opts: -<C>, Long opts: --<Word>
        :param parameters: The list of unparsed program parameters passed by the command line
        :return A list of remaining arguments
        """
        try:
            opts, args = getopt.getopt(parameters, self._shortopts(), self._longopts())
            for op, arg in opts:
                opt = self.get_option(op)
                if opt and opt.cb_handler:
                    opt.cb_handler(arg)
                else:
                    raise InvalidOptionError(f'Option "{op}" not recognized')
            return args
        except getopt.GetoptError as err:
            raise InvalidOptionError(f"### Invalid option: {str(err)}") from err
    
    def _parse_arguments(self, provided_args: List[str]) -> None:
        """Handle program arguments
        :param provided_args: Arguments left after processing all options
        """
        valid = False
        if self.cond_args_chain:
            # Walk through all argument conditions in chain and validate the provided arguments
            for cond_arg in self.cond_args_chain:
                arg = cond_arg.argument
                try:
                    self._recursive_set(0, arg, provided_args)
                    # At this point, we found a valid argument chain
                    valid = self._validate_args_in_chain(arg)
                    # Will be true if all required args were set
                    self.args = provided_args
                    break
                except getopt.GetoptError as err:
                    log.debug(str(err))
                    continue  # Just try the next chain
                except LookupError:
                    continue  # Just try the next chain
            if not valid:
                raise InvalidArgumentError(f"Invalid arguments  \"{', '.join(provided_args)}\"")
    
    def _recursive_set(self, idx: int, argument: Argument, provided_args: List[str]) -> None:
        """ Try to set a value for each provided argument. If any failure setting occur, raise an exception to be caught
            by the parse function, so they can try the next chain in the loop.
        """
        if not argument or idx >= len(provided_args):
            return
        if not argument.set_value(provided_args[idx]):
            raise LookupError(
                f'Invalid argument "{provided_args[idx]}"')
        self._recursive_set(idx + 1, argument.next_in_chain, provided_args)
    
    @staticmethod
    def _validate_args_in_chain(arg: Argument) -> bool:
        """Validate all arguments following the chain path"""
        missing = 0
        next_arg = arg
        while next_arg:
            missing += 1 if not next_arg.value and next_arg.required else 0
            next_arg = next_arg.next_in_chain
        return missing == 0
    
    def _shortopts(self) -> str:
        return ''.join([op.shortopt.replace('-', '') for key, op in self.options.items()])
    
    def _longopts(self) -> List[str]:
        return [op.longopt.replace('-', '') + ' ' for key, op in self.options.items()]
