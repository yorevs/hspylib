#!/usr/bin/env python3
import os
import pathlib
import subprocess
import sys

from hspylib.core.enum.enumeration import Enumeration
from hspylib.core.enum.http_code import HttpCode
from hspylib.core.tools.commons import __version__, sysout, syserr
from hspylib.modules.fetch.fetch import get
from hspylib.modules.application.application import Application
from hspylib.modules.application.argument_chain import ArgumentChain

# The directory containing this file
HERE = pathlib.Path(__file__).parent


class Main(Application):
    """HSPyLib Manager v{} - Manage HSPyLib applications."""

    # The application version
    VERSION = __version__(f"{HERE}/.version")

    # HSPyLib manager usage message
    USAGE = (HERE / "usage.txt").read_text().format('.'.join(map(str, VERSION)))

    # The directory containing all template files
    TEMPLATES = (HERE / "templates")

    # The welcome message
    WELCOME = (HERE / "welcome.txt").read_text()

    GRADLE_PROPS = f"""
project.ext.set("projectVersion", '{VERSION}')
project.ext.set("pythonVersion", '3')
project.ext.set("pyrccVersion", '5')"""

    class AppType(Enumeration):
        BASIC = 1
        GRADLE = 2
        GIT = 4
        ALL = 8

    def __init__(self, app_name: str):
        super().__init__(app_name, self.VERSION)
        self.app_dir = None
        self.init_gradle = False
        self.init_git = False

    def main(self, *params, **kwargs) -> None:
        if len(*params) == 0:
            welcome = self.WELCOME
            sysout(f"{welcome}")
            sysout(self.USAGE)
        else:
            # @formatter:off
            self.with_arguments(
                ArgumentChain.builder()
                    .when('Operation', 'create')
                        .require('MngType', 'basic|gradle|git|all')
                        .require('AppName', '.+')
                        .accept('DestDir', '.+')
                        .end()
                    .build()
            )
            # @formatter:on
            self.parse_parameters(*params)
            self._exec_application()

    def _exec_application(self) -> None:
        """Execute the application"""
        op = self.args[0]
        if "create" == op:
            self._create_app(
                Main.AppType.value_of(self.args[1], ignore_case=True),
                self.args[2],
                self.args[3] if len(self.args) > 2 else os.environ.get('HOME'))
        else:
            syserr('### Invalid operation: {}'.format(op))
            self.usage(1)

    def _create_app(self, app_type: AppType, app_name: str, dest_dir: str):
        sysout(f'Creating app: {app_name} -> {dest_dir} ...')
        try:
            assert os.path.exists(dest_dir), f'Destination not found: {dest_dir}'
            self.app_dir = f'{dest_dir}/{app_name}'
            sysout(f'App: {app_name}')
            self._mkdir('')
            self._mkdir('src')
            self._mkdir('src/test')
            self._mkdir('src/main')
            self._mkfile('src/main/__main__.py', (self.TEMPLATES / "tpl-main.py").read_text())
            self._mkfile('src/main/.version', '0.1.0')
            self._mkdir('src/main/resources')
            self._mkfile('src/main/resources/application.properties', '# Main application property file')
            self._mkdir('src/main/resources/log')
            self._mkfile('README.md', f'# {app_name}')
            self._mkfile('MANIFEST.in', '')
            # TODO Create setup.py
            self._mkfile('.env', '# Type in here the environment variables your app requires')
            self._mkfile('run-it.sh', (self.TEMPLATES / "tpl-run-it.sh").read_text())
            os.chmod(f'{self.app_dir}/run-it.sh', 0o755)
            if app_type in [Main.AppType.GRADLE, Main.AppType.ALL]:
                self._init_gradle(app_name)
            if app_type in [Main.AppType.GIT, Main.AppType.ALL]:
                self._init_git()
        except OSError as err:
            syserr(f"Creation of the application {dest_dir}/{app_name} failed")
            syserr(str(err))
        else:
            sysout(f"Successfully created the application {dest_dir}/{app_name}")

    def _mkdir(self, dirname: str):
        dir_path = f"{self.app_dir}/{dirname}"
        sysout(f'  |- {dir_path}')
        os.mkdir(dir_path)

    def _mkfile(self, filename: str, contents: str):
        file_path = f"{self.app_dir}/{filename}"
        sysout(f'  |- {file_path}')
        with open(f'{file_path}', 'w') as fh:
            fh.write(contents)

    def _init_gradle(self, app_name: str):
        sysout('Initializing gradle project')
        args = ['gradle', 'init', '--project-name', app_name, '--type', 'basic', '--dsl', 'groovy']
        result = subprocess.run(args, capture_output=True, text=True, cwd=self.app_dir).stdout
        sysout('Gradle execution result: {}'.format(result))
        sysout('Downloading gradle extensions')
        self._download_ext('badges.gradle')
        self._download_ext('build-info.gradle')
        self._download_ext('docker.gradle')
        self._download_ext('oracle.gradle')
        self._download_ext('pypi-publish.gradle')
        self._download_ext('python.gradle')
        self._mkfile('properties.gradle', self.GRADLE_PROPS.strip())
        self._mkfile(f'build.gradle', (self.TEMPLATES / "tpl-build.gradle").read_text())
        self._mkfile(f'gradle/dependencies.gradle', (self.TEMPLATES / "tpl-dependencies.gradle").read_text())

    def _download_ext(self, extension: str):
        resp = get(f'https://raw.githubusercontent.com/yorevs/hspylib/master/gradle/{extension}')
        assert resp.status_code == HttpCode.OK, f'Unable to download {extension}'
        self._mkfile(f'gradle/{extension}', resp.body)

    def _init_git(self):
        self._mkfile(f'src/main/resources/log/.gitkeep', '')
        self._mkfile(f'.gitignore', (self.TEMPLATES / "tpl.gitignore").read_text())
        sysout('Initializing git repository')
        result = subprocess.run(['git', 'init'], capture_output=True, text=True, cwd=self.app_dir).stdout
        sysout('Git init result: {}'.format(result))
        sysout('Creating first commit')
        subprocess.run(['git', 'add', '.'], capture_output=True, text=True, cwd=self.app_dir)
        result = subprocess.run(
            ['git', 'commit', '-m', 'First commit [@HSPyLib]'],
            capture_output=True, text=True, cwd=self.app_dir).stdout
        sysout('Git commit result: {}'.format(result))


# Application entry point
if __name__ == "__main__":
    """Application entry point"""
    Main('HSPyLib Manager').INSTANCE.run(sys.argv[1:])
