import logging as log
import os
import re
import sys
import yaml
from configparser import ConfigParser
from typing import Optional, Any

from hspylib.core.tools.commons import flatten_dict


class Properties:
    _default_name = 'application'
    _default_extension = '.properties'
    _profiled_format = '{}-{}{}'
    _simple_format = '{}{}'

    def __init__(
            self,
            filename: str = None,
            profile: str = None,
            load_dir: str = None):

        filename, extension = os.path.splitext(
            filename if filename else f'{self._default_name}{self._default_extension}')
        self.filename = filename
        self.extension = extension
        self.profile = profile if profile else os.environ.get('ACTIVE_PROFILE')
        self.load_dir = load_dir if load_dir else f'{sys.path[0]}/resources'
        self.filepath = None
        self.properties = {}
        self._read()

    def __str__(self):
        str_val = ''
        for key, value in self.properties.items():
            str_val += '{}{}={}'.format('\n' if str_val else '', key, value)
        return str_val

    def __getitem__(self, item: str) -> Any:
        return self.get(item)

    def __iter__(self):
        return self.properties.__iter__()

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
            return self.get(key).lower() in ['true', '1', 'on', 'yes']
        except TypeError:
            return default_value

    def size(self) -> int:
        return len(self.properties) if self.properties else 0

    def values(self):
        return self.properties.values()

    def _read(self) -> None:
        self.filepath = self._find_path()
        if os.path.exists(self.filepath):
            self._parse()
        else:
            raise FileNotFoundError(
                'File "{}" does not exist'.format(self.filepath))

    def _find_path(self) -> str:
        if self.profile:
            filepath = self._profiled_format \
                .format(self.filename, self.profile, self.extension)
        else:
            filepath = self._simple_format \
                .format(self.filename, self.extension)
        return f'{self.load_dir}/{filepath}'

    def _parse(self):
        with open(self.filepath) as fh_props:
            if self.extension in ['.ini', '.cfg']:
                all_lines = ''.join(fh_props.readlines())
                cfg = ConfigParser()
                cfg.read_string(all_lines)
                for section in cfg.sections():
                    self.properties.update(dict(cfg.items(section)))
            elif self.extension == '.properties':
                all_lines = list(map(str.strip, filter(None, fh_props.readlines())))
                self.properties.update({
                    p[0].strip(): p[1].strip() for p in [
                        p.split('=', 1) for p in list(
                            filter(lambda l: re.match('[a-zA-Z0-9][._\\-a-zA-Z0-9]* *=.*', l), all_lines)
                        )
                    ]
                })
            elif self.extension in ['.yml', '.yaml']:
                self.properties.update(flatten_dict(yaml.load(fh_props, Loader=yaml.FullLoader)))
            else:
                raise NotImplementedError(f'Extension {self.extension} is not supported')
        log.info(f'Successfully loaded {len(self.properties)} properties from the file {self.filepath}')
