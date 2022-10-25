#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: main.metaclass
      @file: singleton.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

import logging as log
import sys
from typing import Type, TypeVar, Union

from hspylib.core.exception.exceptions import HSBaseException
from hspylib.core.preconditions import check_not_none

SINGLETON = TypeVar('SINGLETON', bound=Union[Type, 'Singleton'])


# pylint: disable=bad-mcs-classmethod-argument
class Singleton(Type):
    """Singleton pattern is a software design pattern that restricts the instantiation of a class to a singular
    instance. This metaclass enables a class to be singleton."""

    _instances = {}

    def __call__(self, *args, **kwargs):
        """Invoke the class constructor or return the instance if it exists."""
        if not Singleton.has_instance(self):
            try:
                instance = super(Singleton, self).__call__(*args, **kwargs)
                check_not_none(instance, f'Unable to create Singleton instance: {self}')
                setattr(self, 'INSTANCE',  instance)
                Singleton._instances[self.__name__] = instance
                log.debug('Created a new Singleton instance: %s.%s', self.__module__, self.__name__)
            except Exception as err:  # pylint: disable=broad-except
                raise HSBaseException(f"Failed to create singleton instance: '{self.__name__}'", err) from err
        return Singleton._instances[self.__name__]

    @classmethod
    def has_instance(cls, clazz: SINGLETON) -> bool:
        """Whether the class has an instance or not. """
        return clazz.__name__ in cls._instances

    @classmethod
    def del_instance(cls, clazz: SINGLETON) -> None:
        """Deletes the singleton instance. This method should be used only for testing purposes."""
        if any(m in sys.modules.keys() for m in ['unittest', 'pytest']):
            if Singleton.has_instance(clazz):
                log.warning('Deleted an existing Singleton instance: %s.%s', cls.__module__, cls.__name__)
                del cls._instances[clazz.__name__]
                delattr(clazz, 'INSTANCE')
                del clazz
            else:
                raise TypeError(f"Instance not found: '{clazz.__name__}'")
        else:
            raise TypeError("This method is only available for testing purposes (cleanup).")
