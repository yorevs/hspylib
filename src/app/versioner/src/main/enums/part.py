from hspylib.core.enums.enumeration import Enumeration


class Part(Enumeration):
    MAJOR = 1
    MINOR = 2
    PATCH = 4

    def __str__(self):
        return self.name.lower()

    def __repr__(self):
        return str(self)
