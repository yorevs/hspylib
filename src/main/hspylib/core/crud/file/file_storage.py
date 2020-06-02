import ast
import os

from main.hspylib.core.config.app_config import AppConfigs


class FileStorage:
    def __init__(self, filename: str):
        self.logger = AppConfigs.logger()
        self.filename = filename
        self.data = []
        self.load()
        self.logger.debug('File storage created filename={} and loaded entries={}'.format(filename, len(self.data)))

    def load(self):
        mode = 'r+' if os.path.exists(self.filename) else 'w+'
        with open(self.filename, mode) as f_local_db:
            lines = f_local_db.read()
            if lines:
                saved_data = ast.literal_eval(lines)
                self.data = saved_data

    def commit(self):
        with open(self.filename, 'w') as f_local_db:
            f_local_db.write(str(self.data))
        self.logger.debug('File storage committed entries={}'.format(len(self.data)))

    def truncate(self):
        open(self.filename, 'w').close()
        self.logger.warn('File storage was truncated')
