#!/usr/bin/env python3
import logging as log
import os
import sys
from datetime import datetime

from firebase.src.main.core.agent_config import AgentConfig
from firebase.src.main.core.firebase import Firebase
from hspylib.core.tools.commons import __version__, __curdir__, syserr
from hspylib.ui.cli.app.application import Application
from hspylib.ui.cli.app.argument_chain import ArgumentChain


class Main(Application):
    """Firebase Agent - Manage your firebase integration"""

    # The application name
    APP_NAME = os.path.basename(__file__)

    # The application version
    VERSION = __version__('src/main/.version')

    # Usage message
    USAGE = """
Usage: firebase [options] <operation> <arguments>

    Firebase Agent v{} - Manage your firebase integration.

    Options:
      -v  |  --version      : Display current program version.
      -h  |     --help      : Display this help message.

    Operations:
      setup                         : Setup your Firebase account.
      upload <db_alias> <file...>   : Upload files to your Firebase Realtime Database.
      download <db_alias> <file...> : Download files from your Firebase Realtime Database.

    Arguments:
      db_alias      : Alias to be used to identify the firebase object to fetch json_string from.
      file1...      : List of files to upload.
      dest_dir      : Destination directory. If omitted, your home folder will be used.
""".format(APP_NAME, '.'.join(map(str, VERSION)))

    WELCOME = """

{} v{}

Settings ==============================
        FIREBASE_USER: {}
        FIREBASE_CONFIG_FILE: {}
        STARTED: {}
"""

    def __init__(self, app_name: str):
        super().__init__(app_name, self.VERSION, self.USAGE, __curdir__(__file__))
        self.firebase = Firebase()

    def main(self, *params, **kwargs) -> None:
        """Run the application with the command line arguments"""
        # @formatter:off
        self.with_arguments(
            ArgumentChain.builder()
                .when('Operation', 'setup')
                    .end()
                .when('Operation', 'upload')
                    .require('Db_Alias', '.+')
                    .require('Files', '.+')
                    .end()
                .when('Operation', 'download')
                    .require('Db_Alias', '.+')
                    .accept('DestDir', '.+')
                    .end()
                .build()
        )
        # @formatter:on
        self.parse_parameters(*params)
        log.info(
            self.WELCOME.format(
                self.app_name,
                self.VERSION,
                AgentConfig.INSTANCE.username(),
                AgentConfig.INSTANCE.config_file(),
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        self._exec_operation()

    def _exec_operation(self) -> None:
        """Execute the specified firebase operation"""
        op = self.args[0]
        if "setup" == op or not self.firebase.is_configured():
            self.firebase.setup()
        # Already handled above
        if "setup" == op:
            pass
        elif "upload" == op:
            self.firebase.upload(
                self.args[1],
                self.args[2:]
            )
        elif "download" == op:
            self.firebase.download(
                self.args[1],
                self.args[2] if len(self.args) > 2 else os.environ.get('HOME')
            )
        else:
            syserr('### Unhandled operation: {}'.format(op))
            self.usage(1)


if __name__ == "__main__":
    """Application entry point"""
    Main('HSPyLib Firebase Agent').INSTANCE.run(sys.argv[1:])
