from hspylib.modules.cli.application.application import Application
from hspylib.modules.cli.application.argument_chain import ArgumentChain


class ApplicationTest(Application):
    """Versioner - Provides an engine to manage app versions."""

    # The application version
    VERSION = (0, 0, 1)

    # CloudFoundry manager usage message
    USAGE = 'Usage: Its just a test'

    # The welcome message
    WELCOME = 'Welcome to test app'

    def __init__(self, app_name: str):
        super().__init__(app_name, self.VERSION, self.USAGE)

    def _setup_parameters(self, *params, **kwargs) -> None:
        self._with_option('i', 'input', True)
        self._with_option('o', 'output', True)
        # @formatter:off
        self._with_arguments(
            ArgumentChain.builder()
                .when('amount', 'one|two|three', False)
                    .require('item', 'donut|bagel')
                .end()
                .build()
        )
        # @formatter:on

    def _main(self, *params, **kwargs) -> None:
        """Run the application with the command line arguments"""
        self._exec_application()

    def _exec_application(self) -> None:
        """Execute the application"""
        pass
