from typing import Tuple, List, Any

from hspylib.core.tools.validator import Validator


class ArgumentValidator(Validator):

    def __call__(self, *args, **kwargs) -> Tuple[bool, List[dict]]:
        pass

    @staticmethod
    def check_arguments(arguments: Tuple[Any], req_args_num: int) -> Any:
        assert len(arguments) >= req_args_num, \
            "Invalid number of arguments = {}, expecting >= {}".format(
                len(arguments) if arguments else '0', req_args_num)

        return arguments
