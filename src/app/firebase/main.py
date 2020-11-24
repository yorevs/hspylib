# Application name, read from it's own file path
import getopt
import os
import signal
import sys
from datetime import datetime
from typing import List

from firebase.core.agent_config import AgentConfig
from firebase.core.firebase import APP_NAME, VERSION, Firebase
from hspylib.core.config.app_config import AppConfigs
from hspylib.core.meta.singleton import Singleton
from hspylib.core.tools.commons import sysout
from hspylib.ui.cli.menu_utils import MenuUtils
from hspylib.ui.cli.tools.validator.argument_validator import ArgumentValidator

# Usage message
USAGE = """
Usage: {} <option> [arguments]

    Firebase Agent v{} Manage your firebase integration.

    Options:
      -v  |  --version                          : Display current program version.
      -h  |     --help                          : Display this help message.
      -s  |    --setup                          : Setup your Firebase account.
      -u  |   --upload <name> <file_path>   : Upload a file to your Firebase Realtime Database.
      -d  | --download <name> <file_path>   : Download a file from your Firebase Realtime Database.

    Arguments:
      name  : Alias to be used to identify the firebase object to fetch json_string from.
""".format(APP_NAME, ' '.join(map(str, VERSION)))

WELCOME = """

HSPyLib Firebase Agent v{}

Settings ==============================
        FIREBASE_USER: {}
        FIREBASE_CONFIG_FILE: {}
        STARTED: {}
"""


class Main(metaclass=Singleton):
    options_map = {}

    @staticmethod
    def usage(exit_code: int = 0) -> None:
        """Display the usage message and exit with the specified code ( or zero as default )
        :param exit_code: The application exit code
        """
        sysout(USAGE)
        Main.exit_app(exit_code, cls=False)

    @staticmethod
    def version() -> None:
        """Display the current program version and exit"""
        sysout('HSPyLib Vault v{}'.format('.'.join(map(str, VERSION))))
        Main.exit_app(cls=False)

    @staticmethod
    def exit_app(exit_code=0, frame=None, cls: bool = True) -> None:
        """Safely exit the application"""
        sysout(frame if frame else '', end='')
        if cls:
            sysout('\033[2J\033[H')
        exit(exit_code)

    @staticmethod
    def parse_arguments(arguments: List[str]) -> None:
        """ Handle program arguments and options. Short opts: -<C>, Long opts: --<Word>
        :param arguments: The list of program arguments passed on the command line
        """
        try:
            opts, args = getopt.getopt(arguments, 'vhsu:d:', [
                'version', 'help', 'setup', 'upload', 'download'
            ])

            if len(opts) == 0:
                Main.usage()

            for opt, arg in opts:
                if opt in ('-v', '--version'):
                    Main.version()
                elif opt in ('-h', '--help'):
                    Main.usage()
                elif opt in ('-s', '--setup'):
                    Main.options_map['setup'] = args
                elif opt in ('-u', '--upload'):
                    Main.options_map['upload'] = args if ArgumentValidator.validate_argument(args, 1) else None
                elif opt in ('-d', '--download'):
                    Main.options_map['download'] = args if ArgumentValidator.validate_argument(args, 1) else None
                else:
                    assert False, '### Unhandled option: {}'.format(opt)
                break

        except getopt.GetoptError as err:
            sysout('%RED%### Unhandled operation: {}'.format(str(err)))
            Main.usage(1)
        except AssertionError as err:
            sysout('%RED%### {}'.format(str(err)))
            Main.usage(1)

    def __init__(self):
        source_dir = os.path.dirname(os.path.realpath(__file__))
        resource_dir = '{}/resources'.format(source_dir)
        log_dir = '{}/log'.format(resource_dir)
        self.configs = AppConfigs(
            source_root=source_dir,
            resource_dir=resource_dir,
            log_dir=log_dir
        )
        self.configs.logger().info(self.configs)
        self.firebase = Firebase()
        signal.signal(signal.SIGINT, self.firebase.exit_handler)

    def run(self, arguments: List[str]) -> None:
        """Run the application with the command line arguments"""
        self.parse_arguments(arguments)
        signal.signal(signal.SIGINT, self.firebase.exit_handler)
        self.app_exec()

    def app_exec(self):
        """Execute the application logic based on the specified operation"""
        for op in Main.options_map:
            if not Main.options_map[op] is None:
                self.exec_operation(op)
                break

    def exec_operation(self, op):
        """Execute the specified operation
        :param op: The vault operation to execute
        """
        try:
            options = tuple(Main.options_map[op])
            if "setup" == op or not self.firebase.is_setup():
                self.firebase.setup()
            self.configs.logger().info(
                WELCOME.format(
                    VERSION,
                    AgentConfig.INSTANCE.username(),
                    AgentConfig.INSTANCE.config_file(),
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            )
            if "setup" == op:
                pass
            elif "upload" == op:
                self.firebase.upload(options[0])
            elif "download" == op:
                self.firebase.download(options[0])
            else:
                sysout('%RED%### Unhandled operation: {}'.format(op))
                Main.usage(1)
        except Exception as err:
            self.configs.logger().error('Failed to execute \'firebase --{}\' => {}'.format(op, str(err)))
            MenuUtils.print_error('Failed to execute \'firebase --{}\' => '.format(op), str(err))
            self.firebase.exit_handler(1)

        MenuUtils.wait_enter()


if __name__ == "__main__":
    """Application entry point"""
    Main().INSTANCE.run(sys.argv[1:])
    Main.exit_app()
