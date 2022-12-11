from hspylib.core.enums.enumeration import Enumeration


class UriScheme(Enumeration):
    """ Uniform Resource Identifier helps identify a source without ambiguity
    Ref.: https://en.wikipedia.org/wiki/List_of_URI_schemes
    """

    # @formatter:off
    ABOUT   = 'about'
    HTTP    = 'http'
    HTTPS   = 'https'
    FTP     = 'ftp'
    FILE    = 'file'
    # @formatter:on

    @classmethod
    def of(cls, scheme: str) -> 'UriScheme':
        try:
            e = super().of_value(scheme, ignore_case=True)
            return e
        except TypeError:
            raise NotImplementedError(f"'{scheme}' scheme is not supported")
