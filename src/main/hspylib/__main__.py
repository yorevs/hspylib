#!/usr/bin/env python3
import os
import sys

from hspylib.appman import AppManager
from hspylib.core.tools.commons import __version__, sysout, syserr, __here__
from hspylib.modules.application.application import Application
from hspylib.modules.application.argument_chain import ArgumentChain

HERE = __here__(__file__)


class Main(Application):
    """HSPyLib Manager v{} - Manage HSPyLib applications."""

    # The hspylib version
    VERSION = __version__(f"{HERE}/.version")

    # HSPyLib manager usage message
    USAGE = (HERE / "usage.txt").read_text().format('.'.join(map(str, VERSION)))

    # The welcome message
    WELCOME = (HERE / "welcome.txt").read_text()

    def __init__(self, app_name: str):
        super().__init__(app_name, self.VERSION, self.USAGE)

    def main(self, *params, **kwargs) -> None:
        if len(*params) == 0:
            welcome = self.WELCOME
            sysout(f"{welcome}")
            sysout(self.USAGE)
        else:
            # @formatter:off
            self.with_arguments(
                ArgumentChain.builder()
                    .when('Operation', 'create')
                        .require('AppName', '.+')
                        .require('MngType', 'basic|gradle|git|all')
                        .accept('DestDir', '.+')
                        .end()
                    .build()
            )
            # @formatter:on
            self.parse_parameters(*params)
            self._exec_application()

    def _exec_application(self) -> None:
        """Execute the application"""
        op = self.args[0]
        if "create" == op:
            manager = AppManager()
            manager.create_app(
                self.args[1],
                AppManager.AppType.value_of(self.args[2], ignore_case=True),
                self.args[3] if len(self.args) > 2 else os.environ.get('HOME'))
        else:
            syserr('### Invalid operation: {}'.format(op))
            self.usage(1)


# Application entry point
if __name__ == "__main__":
    """Application entry point"""
    Main('HSPyLib Manager').INSTANCE.run(sys.argv[1:])
