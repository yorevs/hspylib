from hspylib.core.exception.exceptions import HSBaseException


class CFConnectionError(HSBaseException):
    """Raised when failed to connect to CloudFoundry"""


class CFExecutionError(HSBaseException):
    """Raised when failed to execute a cf command"""


class CFAuthenticationError(HSBaseException):
    """Raised when failed to authenticate to CloudFoundry"""
