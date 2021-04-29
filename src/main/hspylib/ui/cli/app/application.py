import getopt
import logging as log
import signal
import sys
from typing import List, Callable, Optional, Tuple, Set

from hspylib.core.config.app_config import AppConfigs
from hspylib.core.meta.singleton import Singleton
from hspylib.core.tools.commons import sysout
from hspylib.ui.cli.app.argument import Argument
from hspylib.ui.cli.app.argument_chain import ArgumentChain
from hspylib.ui.cli.app.option import Option


class Application(metaclass=Singleton):
    """TODO"""

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
        """TODO"""
        log.info('Main entry point handler called. nothing to do')

    def run(self, *args, **kwargs):
        """TODO"""
        self.main(*args, **kwargs)
        self.exit_handler()

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
        """ Handle program arguments and options. Short opts: -<C>, Long opts: --<Word>
        :param parameters: The list of unparsed program arguments passed by the command line
        """
        # First parse all options, then, parse arguments
        self.parse_arguments(self.parse_options(parameters))

    def parse_options(self, parameters: List[str]) -> List[str]:
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
            sysout(f"%RED%### Unhandled option: {str(err)}")
            self.usage(1)
        except AssertionError as err:
            sysout(f"%RED%### {str(err)}")
            self.usage(1)

    def parse_arguments(self, provided_args: List[str]) -> None:
        valid = False
        if self.cond_args_chain:
            for cond_arg in self.cond_args_chain:
                arg = cond_arg.argument
                try:
                    self.recursive_set(0, arg, provided_args)
                    # This is true if all required args were set
                    valid = self.validate_argument(arg, len(provided_args))
                    self.args = provided_args
                    break
                except getopt.GetoptError as err:
                    log.debug(str(err))
                    continue  # Just try the next chain
            assert valid, f"Invalid arguments => {', '.join(provided_args)}"

    def recursive_set(self, idx: int, argument: Argument, provided_args: List[str]):
        if not argument or idx >= len(provided_args):
            return
        if not argument.set_value(provided_args[idx]):
            raise getopt.GetoptError(
                f'Invalid argument: {provided_args[idx]}. Required expression: {argument.validation_regex}')
        else:
            self.recursive_set(idx + 1, argument.next_in_chain, provided_args)

    def validate_argument(self, arg: Argument, args_num: int) -> bool:
        missing = 0
        narg = arg
        while narg:
            missing += 1 if not narg.value and narg.required else 0
            narg = narg.next_in_chain
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
