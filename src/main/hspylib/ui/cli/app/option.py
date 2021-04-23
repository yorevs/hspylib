from typing import Callable


class Option:

    def __init__(
            self,
            shortopt: chr,
            longopt: str,
            has_argument: bool = False,
            opt_handler: Callable = None,
            required: bool = False):
        self.shortopt = f"-{shortopt.replace('-', '')}{':' if has_argument > 0 else ''}"
        self.longopt = f"--{longopt.replace('-', '')}{'=' if has_argument > 0 else ''}"
        self.has_argument = has_argument
        self.handler = opt_handler
        self.required = required

    def __str__(self) -> str:
        return ("shortopt: {}, longopt: {}, has_argument: {}, handler: {}".format(
            self.shortopt, self.longopt, self.has_argument, self.handler))

    def __repr__(self):
        return f"[{self.shortopt.replace('-', '').replace(':', '')}, {self.longopt.replace('-', '').replace('=', '')}]"

    def is_eq(self, opt: str):
        clean_opt = opt.replace('-', '').replace(':', '').replace('=', '').strip()
        return \
            clean_opt == self.shortopt.replace('-', '').replace(':', '').strip() or \
            clean_opt == self.longopt.replace('-', '').replace('=', '').strip()
