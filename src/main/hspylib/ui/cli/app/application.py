import getopt
import logging as log
import signal
import sys
from typing import List, Callable, Optional, Tuple

from hspylib.core.config.app_config import AppConfigs
from hspylib.core.meta.singleton import Singleton
from hspylib.core.tools.commons import sysout
from hspylib.ui.cli.app.argument import Argument
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
        self.options = []
        self.required_args = []
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

    def parse_parameters(self, arguments: List[str]) -> None:
        """ Handle program arguments and options. Short opts: -<C>, Long opts: --<Word>
        :param arguments: The list of unparsed program arguments passed by the command line
        """
        try:
            opts, self.args = getopt.getopt(arguments, self._shortopts(), self._longopts())
            assert self._validate_args_and_opts(self.args, opts), \
                f'Invalid arguments/options => Opts: {str(opts)}, Args: {str(self.args)}'
            for op, arg in opts:
                opt = self._getopt(op)
                if opt and opt.cb_handler:
                    opt.cb_handler(arg)
                else:
                    assert False, f"Unhandled option: {op}"
        except getopt.GetoptError as err:
            sysout(f"%RED%### Unhandled option: {str(err)}")
            self.usage(1)
        except AssertionError as err:
            sysout(f"%RED%### {str(err)}")
            self.usage(1)

    def with_option(
            self,
            shortopt: chr,
            longopt: str,
            has_argument: bool = False,
            handler: Callable = None):
        self.options.append(Option(shortopt, longopt, has_argument, handler))

    def with_argument(self, arg_name: str, validation_regex: str = '.*'):
        self.required_args.append(Argument(arg_name, validation_regex))

    def _validate_args_and_opts(self, args: List[str], options: List[str]) -> bool:
        if any(opt[0].strip() in ['-v', '--version', '-h', '--help'] for opt in options):
            return True
        else:
            if len(args) < len(self.required_args):
                return False
            for idx, arg in enumerate(self.required_args):
                if not arg.set_value(args[idx]):
                    return False
        return True

    def _shortopts(self) -> str:
        str_all_opts = ''.join([lop.shortopt.replace('-', '') for lop in self.options])
        return str_all_opts

    def _longopts(self) -> List[str]:
        str_all_opts = [lop.longopt.replace('-', '') + ' ' for lop in self.options]
        return str_all_opts

    def _getopt(self, item: str) -> Optional[Option]:
        return next((op for op in self.options if op.is_eq(item)), None)
