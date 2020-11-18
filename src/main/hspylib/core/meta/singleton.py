from typing import TypeVar, Generic

T = TypeVar('T')


class Singleton(type):
    __instances = {}

    def __call__(cls, *args, **kwargs):
        if not Singleton.has_instance(cls):
            instance = super(Singleton, cls).__call__(*args, **kwargs)
            cls.INSTANCE = instance
            cls.__instances[cls] = instance

        return cls.__instances[cls]

    @classmethod
    def instances(mcs):
        print(Singleton.__instances)

    @classmethod
    def has_instance(mcs, cls):
        return cls in cls.__instances
