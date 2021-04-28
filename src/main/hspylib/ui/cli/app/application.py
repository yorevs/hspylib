import getopt
import logging as log
import signal
import sys
from typing import List, Callable, Optional, Tuple

from hspylib.core.config.app_config import AppConfigs
from hspylib.core.meta.singleton import Singleton
from hspylib.core.tools.commons import sysout
from hspylib.ui.cli.app.option import Option


class Application(metaclass=Singleton):
    """TODO"""

    def __init__(
            self,
            app_name: str,
            app_version: Tuple[int, int, int],
            app_usage: str = "Usage: __main__.py <option> [arguments]",
            source_dir: str = None,
            resource_dir: str = None,
            log_dir: str = None):

        signal.signal(signal.SIGINT, self.exit_handler)
        self.app_name = app_name
        self.app_version = app_version
        self.app_usage = app_usage
        self.options = []
        self.args = None
        self.configs = AppConfigs(
            source_root=source_dir if source_dir else '.',
            resource_dir=resource_dir,
            log_dir=log_dir
        )
        self.with_option('h', 'help', handler=self.usage)
        self.with_option('v', 'version', handler=self.version)

    def main(self, *args, **kwargs):
        """TODO"""
        pass

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

    def usage(self, exit_code: int = 0) -> None:
        """Display the usage message and exit with the specified code ( or zero as default )
        :param exit_code: The application exit code
        """
        sysout(self.app_usage)
        self.exit_handler(exit_code)

    def version(self) -> None:
        """Display the current program version and exit"""
        sysout('{} v{}'.format(self.app_name, '.'.join(map(str, self.app_version))))
        self.exit_handler()

    def parse_arguments(self, arguments: List[str]) -> None:
        """ Handle program arguments and options. Short opts: -<C>, Long opts: --<Word>
        :param arguments: The list of unparsed program arguments passed by the command line
        """
        try:
            if self.options:
                opts, self.args = getopt.getopt(arguments, self.__shortopts__(), self.__longopts__())
                assert self.__has_valid_options__(opts), f'Invalid number of options: {len(opts)}'
                for op, arg in opts:
                    opt = self.__getopt__(op)
                    if opt and opt.handler:
                        opt.handler(arg)
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
            handler: Callable = None,
            required: bool = False):
        self.options.append(Option(shortopt, longopt, has_argument, handler, required))

    def __has_valid_options__(self, options: List[str]):
        if self.__reqopts__() > 0 and not len(options) and len(self.options):
            self.usage(1)
        elif len(options) < self.__reqopts__():
            return any(opt[0].strip() in ['-v', '--version', '-h', '--help'] for opt in options)
        return True

    def __shortopts__(self) -> str:
        str_all_opts = ''.join([lop.shortopt.replace('-', '') for lop in self.options])
        return str_all_opts

    def __longopts__(self) -> List[str]:
        str_all_opts = [lop.longopt.replace('-', '') + ' ' for lop in self.options]
        return str_all_opts

    def __getopt__(self, item: str) -> Optional[Option]:
        return next((op for op in self.options if op.is_eq(item)), None)

    def __reqopts__(self) -> int:
        return sum(opt.required for opt in self.options)
