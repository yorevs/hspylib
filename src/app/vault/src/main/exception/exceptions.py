from hspylib.core.exception.exceptions import HSBaseException


class VaultCloseError(HSBaseException):
    """Raised when closing the vault"""


class VaultOpenError(HSBaseException):
    """Raised when opening the vault"""
