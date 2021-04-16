from typing import Tuple, List

from hspylib.core.tools.validator import Validator


class ArgumentValidator(Validator):

    def __call__(self, *args, **kwargs) -> Tuple[bool, List[dict]]:
        pass

    @staticmethod
    def check_arguments(arguments, args_num: int) -> list:
        assert arguments and len(arguments) >= args_num, \
            "Invalid number of arguments: {}, expecting: {}".format(
                len(arguments) if arguments else '0', args_num)

        return arguments
