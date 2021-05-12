from hspylib.core.enums.enumeration import Enumeration


class Extension(Enumeration):
    SNAPSHOT = 1
    STABLE = 2
    RELEASE = 4

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)
