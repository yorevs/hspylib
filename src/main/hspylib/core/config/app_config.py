import os
from typing import Optional

from main.hspylib.core.config.properties import Properties
from main.hspylib.core.meta.singleton import Singleton
from main.hspylib.tools.commons import log_init

APP_CONFIG_FORMAT = """
AppConfigs
  |-RootDir = {}
  |-LogFile = {}
  |-AppProperties:
   \\-{}
"""


class AppConfigs(metaclass=Singleton):
    INSTANCE = None

    def __init__(self,
                 source_root: str = None,
                 resource_dir: str = None,
                 log_dir: str = None,
                 log_file: str = 'application.log'):
        self._source_root = source_root or os.environ.get('SOURCE_ROOT', os.path.abspath(os.curdir))
        assert os.path.exists(self._source_root), "Unable to find the source directory: {}".format(self._source_root)
        self._log_dir = log_dir if log_dir else '{}/../log'.format(os.environ.get('LOG_DIR', self._source_root))
        assert os.path.exists(self._log_dir), "Unable to find the log directory: {}".format(self._log_dir)
        self._log_file = "{}/{}".format(self._log_dir, log_file)
        self._logger = log_init(self._log_file)
        assert self._logger, "Unable to create the logger: {}".format(str(self._logger))
        self._resource_dir = resource_dir \
            if resource_dir else os.environ.get('RESOURCE_DIR', "{}/main/resources".format(self._source_root))
        self._app_properties = Properties(load_dir=self._resource_dir)
        AppConfigs.INSTANCE = AppConfigs.INSTANCE if AppConfigs.INSTANCE else self

    def __str__(self):
        return '\n{}{}{}'.format(
            '-=' * 40,
            APP_CONFIG_FORMAT.format(
                self._source_root,
                self._log_file,
                str(self._app_properties).replace('\n', '\n   |-')
                if self._app_properties.size() > 0 else ''
            ),
            '-=' * 40
        )

    def get(self, property_name: str) -> Optional[str]:
        return self._app_properties.get(
            property_name) if self._app_properties else None

    def get_int(self, property_name: str) -> Optional[int]:
        return self._app_properties.get_int(
            property_name) if self._app_properties else None

    def get_float(self, property_name: str) -> Optional[float]:
        return self._app_properties.get_float(
            property_name) if self._app_properties else None

    def get_bool(self, property_name: str) -> Optional[bool]:
        return self._app_properties.get_bool(
            property_name) if self._app_properties else None

    def source_root(self) -> str:
        return self._source_root

    def logger(self):
        return self._logger
