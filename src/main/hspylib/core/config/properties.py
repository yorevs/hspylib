import os
import re
from typing import Optional, List


class Properties:
    _default_name = 'application.properties'
    _profiled_format = 'application-{}.properties'

    def __init__(self,
                 filename: str = None,
                 profile: str = None,
                 load_dir: str = None):
        self.filename = filename
        self.profile = profile if profile else os.environ.get('ACTIVE_PROFILE')
        self.load_dir = load_dir if load_dir else os.path.abspath(os.curdir)
        self.properties = {}
        self._read()

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
        return self.get(key).capitalize() in ['True', '1', 'on', 'yes']

    def size(self) -> int:
        return len(self.properties) if self.properties else 0

    def _read(self) -> None:
        default_filename = Properties._profiled_format.format(
            self.profile) if self.profile else Properties._default_name
        self.filename = self.filename if self.filename else default_filename
        file_path = '{}/{}'.format(self.load_dir, self.filename)
        if os.path.exists(file_path):
            with open(file_path) as f_properties:
                all_properties = list(map(str.strip, filter(None, f_properties.readlines())))
                self._parse(all_properties)
        else:
            raise OSError('{}: File "{}" does not exist'.format(self.__class__.__name__, file_path))

    def _parse(self, all_properties: List[str]) -> None:
        self.properties = {
            p[0].strip(): p[1].strip() for p in [
                p.split('=', 1) for p in list(
                    filter(lambda l: re.match('[a-zA-Z0-9][._\\-a-zA-Z0-9]* *=.*', l), all_properties)
                )
            ]
        }
