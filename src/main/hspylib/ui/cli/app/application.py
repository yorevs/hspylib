import getopt
from typing import List, Callable, Optional

from hspylib.ui.cli.appfw.option import Option
from hspylib.core.meta.singleton import Singleton
from hspylib.core.tools.commons import sysout


class Application(metaclass=Singleton):

    VERSION = (0, 0, 0)
    USAGE = "TBD"

    @staticmethod
    def usage(exit_code: int = 0) -> None:
        """Display the usage message and exit with the specified code ( or zero as default )
        :param exit_code: The application exit code
        """
        sysout(Application.USAGE)
        Application.exit_app(exit_code, clear_screen=False)

    def version(self) -> None:
        """Display the current program version and exit"""
        sysout('{} v{}'.format(self.app_name, '.'.join(map(str, Application.VERSION))))
        Application.exit_app(clear_screen=False)

    @staticmethod
    def exit_app(exit_code=0, frame=None, clear_screen: bool = True) -> None:
        """Safely exit the application"""
        sysout(frame if frame else '', end='')
        if clear_screen:
            sysout('%ED2%%HOM%')
        exit(exit_code)

    def parse_arguments(self, arguments: List[str]) -> None:
        """ Handle program arguments and options. Short opts: -<C>, Long opts: --<Word>
        :param arguments: The list of unparsed program arguments passed by the command line
        """
        try:
            opts, args = getopt.getopt(arguments, self.__shortopts__(), self.__longopts__())
            assert self.__has_valid_options__(opts), f'Invalid number of options: {len(opts)}'
            for op, arg in opts:
                opt = self.__getopt__(op)
                if opt and opt.handler:
                    opt.handler()
                else:
                    assert False, f"Unhandled option: {op}"
        except getopt.GetoptError as err:
            sysout(f"%RED%### Unhandled option: {str(err)}")
            self.usage(1)
        except AssertionError as err:
            sysout(f"%RED%### {str(err)}")
            self.usage(1)

    def __init__(self, app_name: str):
        self.app_name = app_name
        self.options = []
        self.with_option('h', 'help', handler=self.usage)
        self.with_option('v', 'version', handler=self.version)

    def main(self, *args, **kwargs):
        pass

    def run(self, *args, **kwargs):
        self.main(*args, **kwargs)
        self.exit_app()

    def with_option(self, shortopt: chr, longopt: str, args_num: int = 0, handler: Callable = None):
        self.options.append(Option(shortopt, longopt, args_num, handler))

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
        return next((opt for opt in self.options if opt.is_eq(item)), None)

    def __reqopts__(self) -> int:
        return sum(opt.args_num > 0 for opt in self.options)
