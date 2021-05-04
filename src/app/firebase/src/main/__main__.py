#!/usr/bin/env python3
import logging as log
import os
import sys
from datetime import datetime

from firebase.src.main.core.agent_config import AgentConfig
from firebase.src.main.core.firebase import Firebase
from hspylib.core.tools.commons import __version__, __curdir__, syserr, __here__
from hspylib.modules.application.application import Application
from hspylib.modules.application.argument_chain import ArgumentChain

HERE = __here__(__file__)


class Main(Application):
    """Firebase Agent - Manage your firebase integration"""

    # The application version
    VERSION = __version__('src/main/.version')

    # Usage message
    USAGE = (HERE / "usage.txt").read_text().format('.'.join(map(str, VERSION)))

    # The welcome message
    WELCOME = (HERE / "welcome.txt").read_text()

    def __init__(self, app_name: str):
        super().__init__(app_name, self.VERSION, self.USAGE, __curdir__(__file__))
        self.firebase = Firebase()

    def setup_parameters(self, *params, **kwargs):
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

    def main(self, *params, **kwargs) -> None:
        """Run the application with the command line arguments"""
        log.info(
            self.WELCOME.format(
                self.app_name,
                self.VERSION,
                AgentConfig.INSTANCE.username(),
                AgentConfig.INSTANCE.config_file(),
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        self._exec_application()

    def _exec_application(self) -> None:
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
