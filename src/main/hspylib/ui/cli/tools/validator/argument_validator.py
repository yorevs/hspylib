from typing import Tuple, List

from hspylib.core.tools.validator import Validator


class ArgumentValidator(Validator):

    def __call__(self, *args, **kwargs) -> Tuple[bool, List[dict]]:
        pass

    @staticmethod
    def validate_argument(arguments, args_num: int) -> bool:
        assert len(arguments) >= args_num, "Invalid number of arguments: {}, expecting: {}"\
            .format(len(arguments), args_num)

        return True
