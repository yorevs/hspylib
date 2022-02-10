#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: hspylib.main.hspylib.core.metaclass
      @file: singleton.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

from typing import Type


class Singleton(type):
    """TODO"""

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """TODO"""
        if not cls.has_instance(cls):
            instance = super(Singleton, cls).__call__(*args, **kwargs)
            cls.INSTANCE = instance
            cls._instances[cls] = instance

        return cls._instances[cls]

    @classmethod
    def instances(mcs) -> dict:  # pylint: disable=bad-mcs-classmethod-argument
        """TODO"""
        return Singleton._instances

    @classmethod
    def has_instance(mcs, cls) -> bool:  # pylint: disable=bad-mcs-classmethod-argument
        """TODO"""
        return cls in Singleton._instances

    @classmethod
    def del_instance(mcs, clazz: Type) -> bool:  # pylint: disable=bad-mcs-classmethod-argument
        """TODO"""
        singleton_instances = Singleton.__getattribute__(mcs, '_instances')
        if clazz in singleton_instances:
            del mcs._instances[clazz]
            delattr(clazz, 'INSTANCE')
            del clazz
            return True

        return False
