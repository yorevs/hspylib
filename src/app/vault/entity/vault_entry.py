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
    """Represents a vault entity"""

    def __init__(self, key: str, name: str, password: str, hint: str, modified: datetime = None):
        self.key = key
        self.name = name
        self.password = password
        self.hint = hint
        self.modified = modified if modified else datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self):
        return ENTRY_FORMAT.format(self.key, self.name, self.password, self.hint, self.modified)

    def to_string(self, show_password: bool = False, show_hint: bool = False):
        """Return the string representation of this entry
        :param show_password: Whether to exhibit the password or not
        :param show_hint: Whether to exhibit the hint or not
        """
        password = self.password if show_password else re.sub('.*', '*' * max(len(self.password), 6), self.password)
        hint = self.hint if show_hint else re.sub('.*', '*' * max(len(self.hint), 6), self.hint)
        return DISPLAY_FORMAT.format(self.key.upper(), self.name, password, hint, self.modified)
