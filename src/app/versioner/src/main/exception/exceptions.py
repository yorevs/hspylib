from hspylib.core.exception.exceptions import HSBaseException


class MissingExtensionError(HSBaseException):
    """Raised when an input version string is the extension part and a promotion or demotion was attempted"""
