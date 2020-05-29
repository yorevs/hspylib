import os
import pathlib
import sys
from abc import ABC
from typing import Optional

from core.config.properties import Properties
from tools.commons import log_init


class AppConfigs(ABC):
    __root_dir = pathlib.Path(sys.argv[0]).parent.absolute()
    __log_file = "{}/../log/application.log".format(__root_dir)
    assert os.path.exists(__log_file)
    __logger = log_init(__log_file)
    __app_properties = Properties(load_dir="{}/resources".format(__root_dir))
    __logger.info('Successfully read {} properties'.format(__app_properties.size()))

    @staticmethod
    def get(property_name: str) -> Optional[str]:
        return AppConfigs.__app_properties.get(property_name) if AppConfigs.__app_properties else None

    @staticmethod
    def get_int(property_name: str) -> Optional[int]:
        return AppConfigs.__app_properties.get_int(property_name) if AppConfigs.__app_properties else None

    @staticmethod
    def get_float(property_name: str) -> Optional[float]:
        return AppConfigs.__app_properties.get_float(property_name) if AppConfigs.__app_properties else None

    @staticmethod
    def get_bool(property_name: str) -> Optional[bool]:
        return AppConfigs.__app_properties.get_bool(property_name) if AppConfigs.__app_properties else None

    @staticmethod
    def root_dir() -> str:
        return AppConfigs.__root_dir

    @staticmethod
    def logger():
        return AppConfigs.__logger
