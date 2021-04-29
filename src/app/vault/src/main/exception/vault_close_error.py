import logging as log


class VaultCloseError(Exception):
    def __init__(self, message: str, cause: Exception):
        fmt_msg = f'{message} => {str(cause)}'
        super().__init__(fmt_msg)
        log.error(fmt_msg)
