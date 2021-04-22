from typing import Callable


class Option:

    def __init__(self, shortopt: chr, longopt: str, args_num: int = 0, opt_handler: Callable = None):
        self.shortopt = f"-{shortopt.replace('-', '')}{':' if args_num > 0 else ''}"
        self.longopt = f"--{longopt.replace('-', '')}"
        self.handler = opt_handler
        self.args_num = args_num

    def __str__(self) -> str:
        return ("shortopt: {}, longopt: {}, args_num: {}, handler: {}".format(
            self.shortopt, self.longopt, self.args_num, self.handler))

    def __repr__(self):
        return f"[{self.shortopt.replace('-', '').replace(':', '')}, {self.longopt.replace('-', '')}]"

    def is_eq(self, opt: str):
        clean_opt = opt.replace('-', '').replace(':', '').strip()
        return \
            clean_opt == self.shortopt.replace('-', '').replace(':', '').strip() or \
            clean_opt == self.longopt.replace('-', '').strip()
