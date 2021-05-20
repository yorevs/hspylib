from hspylib.core.enums.enumeration import Enumeration


class ExitCode(Enumeration):

    """ Returned when something went wrong due to any Human interaction """
    ERROR = -1

    """ Returned when something ran successfully without errors """
    SUCCESS = 0

    """ Returned when something that was supposed to work and failed due to unexpected software behaviour """
    FAILED = 1

    # Custom exit codes can be defined here {

    # }

    def __str__(self):
        return f"{self.name}({self.value})"

    def __repr__(self):
        return self.value
