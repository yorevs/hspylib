# @purpose: Represents a vault entity
import re
from datetime import datetime


DISPLAY_FORMAT = """[%BLUE%{}%NC%]:
        Name: %GREEN%{}%NC%
    Password: %GREEN%{}%NC%
        Hint: %GREEN%{}%NC%
    Modified: %GREEN%{}%NC%
"""

ENTRY_FORMAT = """{}|{}|{}|{}"""


class VaultEntry(object):

    def __init__(self, key: str, name: str, password: str, hint: str, modified: datetime = None):
        self.key = key
        self.name = name
        self.password = password
        self.hint = hint
        self.modified = modified if modified else datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self):
        return ENTRY_FORMAT.format(self.key, self.name, self.password, self.hint, self.modified)

    def to_string(self, show_password=False):
        password = self.password if show_password else re.sub('.*', '*' * 6, self.password)
        return DISPLAY_FORMAT.format(self.key, self.key, password, self.hint, self.modified)
