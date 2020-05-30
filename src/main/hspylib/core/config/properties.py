import re
from os import environ, path
from typing import Optional


class Properties:
    __default_profile = 'ACTIVE_PROFILE'
    __default_name = 'application.properties'
    __profiled_format = 'application-{}.properties'

    def __init__(self, filename: str = None, profile: str = environ.get(__default_profile), load_dir: str = '.'):
        assert path.exists(filename)
        self.filename = filename
        self.profile = profile
        self.load_dir = load_dir
        self.properties = {}
        self.__read()

    def __str__(self):
        str_val = ''
        for key, value in self.properties.items():
            str_val += '{}{}={}'.format('\n' if str_val else '', key, value)
        return str_val

    def get(self, key: str, default_value=None) -> Optional[str]:
        return self.properties[key.strip()] if key.strip() in self.properties else default_value

    def get_int(self, key: str, default_value=None) -> Optional[int]:
        try:
            return int(self.get(key))
        except TypeError:
            return default_value

    def get_float(self, key: str, default_value=None) -> Optional[float]:
        try:
            return float(self.get(key))
        except TypeError:
            return default_value

    def get_bool(self, key: str, default_value=None) -> Optional[bool]:
        try:
            return bool(self.get(key))
        except TypeError:
            return default_value

    def size(self) -> int:
        return len(self.properties) if self.properties else 0

    def __read(self):
        default_filename = Properties.__profiled_format.format(
            self.profile) if self.profile else Properties.__default_name
        self.filename = self.filename if self.filename else default_filename
        file_path = '{}/{}'.format(self.load_dir, self.filename)
        if path.exists(file_path):
            with open(file_path) as f_properties:
                all_properties = f_properties.readlines()
                for next_property in all_properties:
                    if next_property.strip().startswith('#'):
                        continue
                    if not re.match('[a-zA-Z0-9][._\\-a-zA-Z0-9]*', next_property):
                        continue
                    parts = next_property.split('=', 1)
                    key = parts[0].strip()
                    value = parts[1].strip()
                    self.properties[key] = value
        else:
            raise OSError('{}: File "{}" does not exist'.format(self.__class__.__name__, file_path))
