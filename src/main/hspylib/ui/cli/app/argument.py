import re


class Argument:

    def __init__(self, arg_name: str, validation_regex: str = '.*'):
        self.arg_name = arg_name
        self.validation_regex = validation_regex
        self.value = ''

    def __str__(self):
        return "arg_nam: {}, validation_regex: {}".format(self.arg_name, self.validation_regex)

    def __repr__(self):
        return str(self)

    def set_value(self, provided_arg: str) -> bool:
        self.value = provided_arg if re.match(rf'^({self.validation_regex})$', provided_arg) else None
        return True if self.value else False
