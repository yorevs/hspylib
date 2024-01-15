from hspylib.core.enums.charset import Charset


class Constants:
    # Interative mode termination expressions.
    TERM_EXPRESSIONS = r"^((good)?(bye ?)+|(tchau ?)+|(ciao ?)|quit|exit|than(ks| you)).*"
    # Default application language.
    DEFAULT_LANGUAGE = 'en_US'
    # Default application text encoding.
    DEFAULT_ENCODING = Charset.UTF_8.val
