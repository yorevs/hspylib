from typing import Tuple, List

from hspylib.core.tools.validator import Validator


class ArgumentValidator(Validator):

    def __call__(self, *args, **kwargs) -> Tuple[bool, List[dict]]:
        errors = []
        assert len(args) == 1, "Only one argument can be validated at a time"
        assert isinstance(args[0], str), "Only string arguments can be validated"
        assert self.validate_argument(args[0]), "Invalid arguments: {}".format(args[0])
        super().__call__(args, kwargs)

        return len(errors) == 0, errors

    @staticmethod
    def validate_argument(arguments, args_num: int) -> (bool, str):
        return len(arguments) < args_num, "### Invalid number of arguments: {}, expecting: {}"\
            .format(len(arguments), args_num)
