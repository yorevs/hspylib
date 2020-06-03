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
   \\- {}
"""


class AppConfigs(metaclass=Singleton):
    INSTANCE = None

    def __init__(self, log_file: str = 'application.log', source_root: str = None):
        self.__root_dir = source_root or os.environ.get('SOURCE_ROOT', '.')
        assert os.path.exists(self.__root_dir)
        self.__log_file = "{}/../log/{}".format(self.__root_dir or self.__root_dir, log_file)
        self.__logger = log_init(self.__log_file)
        self.__app_properties = Properties(load_dir="{}/main/resources".format(self.__root_dir))
        AppConfigs.INSTANCE = AppConfigs.INSTANCE or self

    def __str__(self):
        return '\n{}{}{}'.format(
            '-=' * 40,
            APP_CONFIG_FORMAT.format(
                self.__root_dir,
                self.__log_file,
                str(self.__app_properties).replace('\n', '\n   |- ')
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
    def root_dir() -> str:
        return AppConfigs.INSTANCE.__root_dir

    @staticmethod
    def logger():
        return AppConfigs.INSTANCE.__logger


AppConfigs().logger().info(AppConfigs.INSTANCE)
