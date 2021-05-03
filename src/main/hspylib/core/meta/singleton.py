import logging as log
from typing import Type


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if not cls.has_instance(cls):
            instance = super(Singleton, cls).__call__(*args, **kwargs)
            cls.INSTANCE = instance
            cls._instances[cls] = instance

        return cls._instances[cls]

    @classmethod
    def del_instance(mcs, clazz: Type) -> bool:
        singleton_instances = Singleton.__getattribute__(mcs, '_instances')
        if clazz in singleton_instances:
            clazz_name = clazz.__name__
            del mcs._instances[clazz]
            delattr(clazz, 'INSTANCE')
            del clazz
            log.warn(f'Singleton instance was deleted: {clazz_name}')
            return True
        else:
            return False

    @classmethod
    def instances(mcs):
        print(Singleton._instances)

    @classmethod
    def has_instance(mcs, cls):
        return cls in cls._instances
