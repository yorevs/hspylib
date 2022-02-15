import sys
from argparse import ArgumentParser, ArgumentError
from gettext import gettext as _


class HSArgumentParser(ArgumentParser):

    def _check_value(self, action, value):
        # converted value must be one of the choices (if specified)
        if action.choices is not None and value not in action.choices:
            args = {'value': value,
                    'choices': ', '.join(map(repr, action.choices))}
            msg = _('invalid choice: %(value)r (choose from %(choices)s)')
            raise ArgumentError(action, msg % args)

    def error(self, message):
        self.print_help(sys.stderr)
        self.exit(2, _(f'\n### Error {self.prog} -> {message}\n\n'))
