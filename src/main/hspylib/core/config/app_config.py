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
        self.__source_root = source_root or os.environ.get('SOURCE_ROOT', os.path.abspath(os.curdir))
        assert os.path.exists(self.__source_root), "Unable to find the source directory: {}".format(self.__source_root)
        self.__log_dir = log_dir if log_dir else '{}/../log'.format(os.environ.get('LOG_DIR', self.__source_root))
        assert os.path.exists(self.__log_dir), "Unable to find the log directory: {}".format(self.__log_dir)
        self.__log_file = "{}/{}".format(self.__log_dir, log_file)
        self.__logger = log_init(self.__log_file)
        assert self.__logger, "Unable to create the logger: {}".format(str(self.__logger))
        self.__resource_dir = resource_dir \
            if resource_dir else os.environ.get('RESOURCE_DIR', "{}/main/resources".format(self.__source_root))
        self.__app_properties = Properties(load_dir=self.__resource_dir)
        AppConfigs.INSTANCE = AppConfigs.INSTANCE if AppConfigs.INSTANCE else self

    def __str__(self):
        return '\n{}{}{}'.format(
            '-=' * 40,
            APP_CONFIG_FORMAT.format(
                self.__source_root,
                self.__log_file,
                str(self.__app_properties).replace('\n', '\n   |-')
                if self.__app_properties.size() > 0 else ''
            ),
            '-=' * 40
        )

    @staticmethod
    def get(property_name: str) -> Optional[str]:
        return AppConfigs.INSTANCE.__app_properties.get(
            property_name) if AppConfigs.INSTANCE.__app_properties else None

    @staticmethod
    def get_int(property_name: str) -> Optional[int]:
        return AppConfigs.INSTANCE.__app_properties.get_int(
            property_name) if AppConfigs.INSTANCE.__app_properties else None

    @staticmethod
    def get_float(property_name: str) -> Optional[float]:
        return AppConfigs.INSTANCE.__app_properties.get_float(
            property_name) if AppConfigs.INSTANCE.__app_properties else None

    @staticmethod
    def get_bool(property_name: str) -> Optional[bool]:
        return AppConfigs.INSTANCE.__app_properties.get_bool(
            property_name) if AppConfigs.INSTANCE.__app_properties else None

    @staticmethod
    def source_root() -> str:
        return AppConfigs.INSTANCE.__source_root

    @staticmethod
    def logger():
        return AppConfigs.INSTANCE.__logger
