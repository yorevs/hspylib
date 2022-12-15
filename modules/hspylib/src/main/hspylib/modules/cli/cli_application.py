from hspylib.modules.application.application import Application
from hspylib.modules.application.exit_status import ExitStatus


class CliApplication(Application):
    """TODO"""

    def _setup_arguments(self) -> None:
        pass

    def _main(self, *params, **kwargs) -> ExitStatus:
        pass

    def _cleanup(self) -> None:
        pass
