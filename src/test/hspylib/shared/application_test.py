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
        self.opts = set({})
        super().__init__(app_name, self.VERSION, self.USAGE)

    def setup_parameters(self, *params, **kwargs) -> None:
        self.with_option('i', 'input', True, lambda arg: self.opts.add(f'input {arg}'))
        self.with_option('o', 'output', True, lambda arg: self.opts.add(f'output {arg}'))
        # @formatter:off
        self.with_arguments(
            ArgumentChain.builder()
                .when('Number', 'one|two|three', False)
                    .require('Object', 'donut|bagel')
                .end()
                .build()
        )
        # @formatter:on

    def main(self, *params, **kwargs) -> None:
        """Run the application with the command line arguments"""
        self._exec_application()

    def _exec_application(self) -> None:
        """Execute the application"""
        pass
