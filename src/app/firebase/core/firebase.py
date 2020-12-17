import os
from typing import List

from firebase.core.agent_config import AgentConfig
from firebase.core.file_processor import FileProcessor
from hspylib.core.config.app_config import AppConfigs
from hspylib.core.tools.commons import sysout, file_is_not_empty

# Application name, read from it's own file path
APP_NAME = os.path.basename(__file__)

# Version tuple: (major,minor,build)
VERSION = (1, 1, 0)


class Firebase(object):
    """Represents the firebase agent and it's functionalities"""

    def __init__(self):
        self.payload = None
        self.processor = FileProcessor()
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
        """Setup a firebase creating or reading an existing configuration file"""
        if file_is_not_empty(self.configs.config_file()):
            self.configs.load()
        else:
            self.configs.prompt()
        self.log.debug(str(self.configs))

    def upload(self, db_alias: str, file_paths: List[str]) -> bool:
        """Upload file_paths to firebase"""
        url = self.configs.url(db_alias)
        assert len(file_paths) > 0, "Unable to upload file_paths (zero size)."
        return self.processor.upload_files(url, file_paths) > 0

    def download(self, db_alias: str, dest_dir: str) -> bool:
        """Download file_paths from firebase"""
        url = self.configs.url(db_alias)
        assert dest_dir and os.path.exists(dest_dir), "Unable find destination directory: {}".format(dest_dir)
        return self.processor.download_files(url, dest_dir or os.environ.get('HOME')) > 0

    def is_setup(self):
        return self.configs is not None and self.configs.fb_configs is not None
