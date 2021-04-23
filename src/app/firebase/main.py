#!/usr/bin/env python3
import os
import signal
import sys
import traceback
from datetime import datetime

from firebase.core.agent_config import AgentConfig
from firebase.core.firebase import Firebase
from hspylib.core.tools.commons import sysout
from hspylib.ui.cli.app.application import Application
from hspylib.ui.cli.menu.menu_utils import MenuUtils
from hspylib.ui.cli.tools.validator.argument_validator import ArgumentValidator

# Application name, read from it's own file path
APP_NAME = os.path.basename(__file__)

# Version tuple: (major,minor,build)
VERSION = (1, 2, 0)

# Usage message
USAGE = """
Usage: {} <option> [arguments]

    Firebase Agent v{} Manage your firebase integration.

    Options:
      -v  |  --version                              : Display current program version.
      -h  |     --help                              : Display this help message.
      -s  |    --setup                              : Setup your Firebase account.
      -u  |   --upload <db_alias> <file1...fileN>   : Upload files to your Firebase Realtime Database.
      -d  | --download <db_alias> [dest_dir]        : Download files from your Firebase Realtime Database.

    Arguments:
      db_alias      : Alias to be used to identify the firebase object to fetch json_string from.
      file1..N      : List os file paths to upload.
      download_dir  : Destination directory. If omitted, your home folder will be used.
""".format(APP_NAME, ' '.join(map(str, VERSION)))

WELCOME = """

HSPyLib Firebase Agent v{}

Settings ==============================
        FIREBASE_USER: {}
        FIREBASE_CONFIG_FILE: {}
        STARTED: {}
"""


class Main(Application):

    def __init__(self, app_name: str):
        source_dir = os.path.dirname(os.path.realpath(__file__))
        super().__init__(app_name, VERSION, USAGE, source_dir)
        self.firebase = Firebase()
        signal.signal(signal.SIGINT, self.exit_handler)

    def main(self, *args, **kwargs) -> None:
        """Run the application with the command line arguments"""
        self.with_option('s', 'setup', handler=lambda arg: self.exec_operation('setup'))
        self.with_option('u', 'upload', handler=lambda arg: self.exec_operation('upload', 2))
        self.with_option('d', 'download', handler=lambda arg: self.exec_operation('download', 1))
        self.parse_arguments(*args)
        self.configs.logger().info(
            WELCOME.format(
                VERSION,
                AgentConfig.INSTANCE.username(),
                AgentConfig.INSTANCE.config_file(),
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )

    def exec_operation(self, op: str, req_args: int = 0) -> None:
        """Execute the specified operation
        :param op: The firebase operation to execute
        :param req_args: Number of required arguments for the operation
        """
        try:
            self.args = tuple(ArgumentValidator.check_arguments(self.args, req_args))
            if "setup" == op or not self.firebase.is_setup():
                self.firebase.setup()

            # Already handled above
            if "setup" == op:
                pass
            elif "upload" == op:
                self.firebase.upload(self.args[0], self.args[1:])
            elif "download" == op:
                self.firebase.download(self.args[0], self.args[1] if len(self.args) > 1 else None)
            else:
                sysout('%RED%### Unhandled operation: {}'.format(op))
                self.usage(1)
        except Exception:
            err = str(traceback.format_exc())
            self.configs.logger().error('Failed to execute \'firebase --{}\' => {}'.format(op, err))
            MenuUtils.print_error('Failed to execute \'vault --{}\' => '.format(op), err)
            self.exit_handler(1)

        MenuUtils.wait_enter()


if __name__ == "__main__":
    """Application entry point"""
    Main('HSPyLib Firebase Agent').INSTANCE.run(sys.argv[1:])
