from typing import Callable


class Option:

    def __init__(
            self,
            shortopt: chr,
            longopt: str,
            has_argument: bool = False,
            cb_handler: Callable = None):
        self.shortopt = f"-{shortopt.replace('-', '')}{':' if has_argument > 0 else ''}"
        self.longopt = f"--{longopt.replace('-', '')}{'=' if has_argument > 0 else ''}"
        self.has_argument = has_argument
        self.cb_handler = cb_handler

    def __str__(self) -> str:
        return ("shortopt: {}, longopt: {}, has_argument: {}, cb_handler: {}".format(
            self.shortopt, self.longopt, self.has_argument, self.cb_handler))

    def __repr__(self):
        return f"[{self.shortopt.replace('-', '').replace(':', '')}, {self.longopt.replace('-', '').replace('=', '')}]"

    def is_eq(self, opt: str):
        clean_opt = opt.replace('-', '').replace(':', '').replace('=', '').strip()
        return \
            clean_opt == self.shortopt.replace('-', '').replace(':', '').strip() or \
            clean_opt == self.longopt.replace('-', '').replace('=', '').strip()
