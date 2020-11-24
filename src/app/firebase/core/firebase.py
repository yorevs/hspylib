import os
from typing import List

from firebase.core.agent_config import AgentConfig
from hspylib.core.config.app_config import AppConfigs
from hspylib.core.tools.commons import sysout, file_is_not_empty

# Application name, read from it's own file path
APP_NAME = os.path.basename(__file__)

# Version tuple: (major,minor,build)
VERSION = (1, 1, 0)

# Usage message
USAGE = """
Usage: {} <option> [arguments]

    HomeSetup firebase v{} Manage your firebase integration.

    Options:
      -v  |  --version              : Display current program version.
      -h  |     --help              : Display this help message.
      -s  |    --setup              : Setup your Firebase account to use with HomeSetup.
      -u  |   --upload <name>   : Upload files to your Firebase Realtime Database.
      -d  | --download <name>   : Download files from your Firebase Realtime Database.

    Arguments:
      name  : Alias to be used to identify the firebase object to fetch json_string from.
""".format(APP_NAME, ' '.join(map(str, VERSION)))


class Firebase(object):
    """Represents the firebase agent and it's functionalities"""

    def __init__(self):
        self.payload = None
        self.configs = AgentConfig()
        self.log = AppConfigs.INSTANCE.logger()

    def __str__(self):
        return str(self.payload)

    def exit_handler(self, signum=0, frame=None) -> None:
        """
        Handle interruptions to shutdown gracefully
        :param signum: The signal number or the exit code
        :param frame: The frame raised by the signal
        """
        if frame is not None:
            self.log.warn('Signal handler hooked signum={} frame={}'.format(signum, frame))
            exit_code = 3
        else:
            self.log.info('Exit handler called')
            exit_code = signum
        sysout('')
        exit(exit_code)

    def setup(self):
        if file_is_not_empty(self.configs.config_file()):
            self.configs.load()
        else:
            self.configs.prompt()
        sysout(str(self.configs))

    def upload(self, db_alias: str, files: List[str]) -> bool:
        url = self.configs.url(db_alias)
        # TODO
        return True

    def download(self, db_alias: str, files: List[str]) -> bool:
        url = self.configs.url(db_alias)
        # TODO
        return True

    def is_setup(self):
        return self.configs is not None and self.configs.fb_configs is not None
