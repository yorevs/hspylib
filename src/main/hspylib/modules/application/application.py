import getopt
import logging as log
import signal
import sys
from datetime import datetime
from typing import List, Callable, Optional, Tuple, Set

from hspylib.core.config.app_config import AppConfigs
from hspylib.core.meta.singleton import Singleton
from hspylib.core.tools.commons import sysout, syserr
from hspylib.modules.application.argument import Argument
from hspylib.modules.application.argument_chain import ArgumentChain
from hspylib.modules.application.option import Option


class Application(metaclass=Singleton):
    """HSPyLib application framework"""

    def __init__(
            self,
            app_name: str,
            app_version: Tuple[int, int, int],
            app_usage: str = "Usage: __main__.py [options] <arguments>",
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
        self.with_option('h', 'help', handler=self.usage)
        self.with_option('v', 'version', handler=self.version)

    def main(self, *args, **kwargs):
        """Execute the application's main statements"""
        log.info('Main entry point handler called. nothing to do')

    def run(self, *args, **kwargs):
        """Main entry point handler"""
        log.info('Run started {}'.format(datetime.now()))
        self.main(*args, **kwargs)
        self.exit_handler()
        log.info('Run finished {}'.format(datetime.now()))

    def cleanup(self):
        """TODO"""
        log.info('Cleanup handler called. nothing to cleanup')

    def exit_handler(self, signum=0, frame=None, clear_screen: bool = False) -> None:
        """
        Handle interruptions to shutdown gracefully
        :param signum: The signal number or the exit code
        :param frame: The frame raised by the signal
        :param clear_screen: Whether to clean the screen before execution or not
        """
        if frame is not None:
            log.warn('Signal handler hooked signum={} frame={}'.format(signum, frame))
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
        self.exit_handler(args[0] or 0)

    def version(self, *args) -> None:
        """Display the current program version and exit
        :param args: The application arguments
        """
        sysout('{} v{}'.format(self.app_name, '.'.join(map(str, self.app_version))))
        self.exit_handler(args[0] or 0)

    def parse_parameters(self, parameters: List[str]) -> None:
        """ Handle program parameters.
        :param parameters: The list of unparsed program parameters passed by the command line
        """
        # First parse all options, then, parse arguments
        self.parse_arguments(self.parse_options(parameters))

    def parse_options(self, parameters: List[str]) -> List[str]:
        """Handle program options in the form: Short opts: -<C>, Long opts: --<Word>
        :param parameters: The list of unparsed program parameters passed by the command line
        :return A list of remaining arguments
        """
        try:
            opts, args = getopt.getopt(parameters, self._shortopts(), self._longopts())
            for op, arg in opts:
                opt = self._getopt(op)
                if opt and opt.cb_handler:
                    opt.cb_handler(arg)
                else:
                    assert False, f"Unhandled option: {op}"
            return args
        except getopt.GetoptError as err:
            syserr(f"### Unhandled option: {str(err)}")
            self.usage(1)
        except AssertionError as err:
            syserr(f"### {str(err)}")
            self.usage(1)

    def parse_arguments(self, provided_args: List[str]) -> None:
        """Handle program arguments
        :param provided_args: Arguments left after processing all options
        """
        valid = False
        if self.cond_args_chain:
            # Walk through all argument conditions in chain and validate the provided arguments
            for cond_arg in self.cond_args_chain:
                arg = cond_arg.argument
                try:
                    self.recursive_set(0, arg, provided_args)
                    # At this point, we found a valid argument chain
                    valid = self.validate_args_in_chain(arg)
                    # Will be true if all required args were set
                    self.args = provided_args
                    break
                except getopt.GetoptError as err:
                    log.debug(str(err))
                    continue  # Just try the next chain
            assert valid, f"Invalid arguments => {', '.join(provided_args)}"

    def recursive_set(self, idx: int, argument: Argument, provided_args: List[str]):
        """ Try to set a value for each provided argument. If any failure setting occur, raise an exception to be caught
            by the parse function, so they can try the next chain in the loop.
        """
        if not argument or idx >= len(provided_args):
            return
        if not argument.set_value(provided_args[idx]):
            raise getopt.GetoptError(
                f'Invalid argument: {provided_args[idx]}. Required expression: {argument.validation_regex}')
        else:
            self.recursive_set(idx + 1, argument.next_in_chain, provided_args)

    @staticmethod
    def validate_args_in_chain(arg: Argument) -> bool:
        missing = 0
        next_arg = arg
        while next_arg:
            missing += 1 if not next_arg.value and next_arg.required else 0
            next_arg = next_arg.next_in_chain
        return missing == 0

    def with_option(
            self,
            shortopt: chr,
            longopt: str,
            has_argument: bool = False,
            handler: Callable = None):
        self.options[longopt] = Option(shortopt, longopt, has_argument, handler)

    def with_arguments(
            self,
            chained_args: Set[ArgumentChain.ChainedArgument]):
        self.cond_args_chain = chained_args

    def _shortopts(self) -> str:
        return ''.join([op.shortopt.replace('-', '') for key, op in self.options.items()])

    def _longopts(self) -> List[str]:
        return [op.longopt.replace('-', '') + ' ' for key, op in self.options.items()]

    def _getopt(self, item: str) -> Optional[Option]:
        return next((op for key, op in self.options.items() if op.is_eq(item)), None)
