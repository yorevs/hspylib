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
import traceback
from typing import Type

from hspylib.core.tools.commons import syserr


# pylint: disable=bad-mcs-classmethod-argument


class Singleton(type):
    """TODO"""

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """TODO"""
        if not cls.has_instance(cls):
            try:
                instance = super(Singleton, cls).__call__(*args, **kwargs)
                assert instance is not None, f'Unable to create Singleton instance: {cls}'
                cls.INSTANCE = instance
                cls._instances[cls] = instance
                log.debug(f'Created a new Singleton instance: {cls.__module__}.{cls.__name__}')
            except Exception:
                log.error(traceback.format_exc())
                syserr(traceback.format_exc())

        return cls._instances[cls]

    @classmethod
    def instances(mcs) -> dict:
        """TODO"""
        return Singleton._instances

    @classmethod
    def has_instance(mcs, cls) -> bool:
        """TODO"""
        return cls in Singleton._instances

    @classmethod
    def del_instance(mcs, clazz: Type) -> bool:
        """TODO"""
        singleton_instances = Singleton.__getattribute__(mcs, '_instances')
        if clazz in singleton_instances:
            log.warning(f'Deleted an existing Singleton instance: {mcs.__module__}.{mcs.__name__}')
            del mcs._instances[clazz]
            delattr(clazz, 'INSTANCE')
            del clazz
            return True

        return False
