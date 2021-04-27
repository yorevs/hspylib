import ast
import logging as log
import os


class FileStorage:
    def __init__(self, filename: str):
        self.filename = filename
        self.data = []
        self.load()
        log.debug('File storage filename={} created and loaded entries={}'.format(filename, len(self.data)))

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
        log.debug('File storage filename={} committed entries={}'.format(self.filename, len(self.data)))

    def truncate(self):
        open(self.filename, 'w').close()
        log.warn('File storage filename={} was truncated'.format(self.filename))
