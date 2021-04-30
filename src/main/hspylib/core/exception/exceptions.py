import logging as log


class HSBaseException(Exception):
    """This is a generic exception and should not be raised. It may be inherited instead"""
    def __init__(self, message: str, cause: Exception = None):
        fmt_msg = f'{message}' + (' => {str(cause)}' if cause else '')
        super().__init__(fmt_msg)
        log.error(fmt_msg)


class EntityNotFoundError(HSBaseException):
    """Raised when an entity is not found"""


class InputAbortedError(HSBaseException):
    """Raised when an input method is aborted"""


class ProgrammingError(HSBaseException):
    """Exception raised for programming errors, e.g. table not found
    or already exists, syntax error in the SQL statement, wrong number
    of parameters specified, etc."""


class InvalidArgumentError(HSBaseException):
    """Raised when an invalid argument is received by the application"""


class InvalidOptionError(HSBaseException):
    """Raised when an invalid option is received by the application"""
