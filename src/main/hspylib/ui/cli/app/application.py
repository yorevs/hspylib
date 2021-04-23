import getopt
from typing import List, Callable, Optional, Tuple

from hspylib.core.config.app_config import AppConfigs
from hspylib.core.meta.singleton import Singleton
from hspylib.core.tools.commons import sysout
from hspylib.ui.cli.app.option import Option


class Application(metaclass=Singleton):

    @staticmethod
    def exit_app(exit_code=0, frame=None, clear_screen: bool = False) -> None:
        """Safely exit the application"""
        sysout(frame if frame else '', end='')
        if clear_screen:
            sysout('%ED2%%HOM%')
        exit(exit_code)

    def usage(self, exit_code: int = 0) -> None:
        """Display the usage message and exit with the specified code ( or zero as default )
        :param exit_code: The application exit code
        """
        sysout(self.app_usage)
        Application.exit_app(exit_code)

    def version(self) -> None:
        """Display the current program version and exit"""
        sysout('{} v{}'.format(self.app_name, '.'.join(map(str, self.app_version))))
        Application.exit_app()

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

    def __init__(
            self,
            app_name: str,
            app_version: Tuple[int, int, int],
            app_usage: str,
            source_dir: str,
            resource_dir: str = None,
            log_dir: str = None):

        self.app_name = app_name
        self.app_version = app_version
        self.app_usage = app_usage
        self.options = []
        self.args = None
        self.configs = AppConfigs(
            source_root=source_dir,
            resource_dir=resource_dir,
            log_dir=log_dir
        )
        self.configs.logger().info(self.configs)
        self.with_option('h', 'help', handler=self.usage)
        self.with_option('v', 'version', handler=self.version)

    def main(self, *args, **kwargs):
        pass

    def run(self, *args, **kwargs):
        self.main(*args, **kwargs)
        self.exit_app()

    def with_option(
            self,
            shortopt: chr,
            longopt: str,
            has_argument: bool = False,
            handler: Callable = None,
            required: bool = False):
        self.options.append(Option(shortopt, longopt, has_argument, handler, required))

    def __has_valid_options__(self, options: List[str]):
        if len(options) < self.__reqopts__():
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
