#!/usr/bin/env python3
import getopt
import os
import pathlib
import subprocess
import sys
from typing import List

from hspylib.modules.fetch.fetch import get

from hspylib.core.enum.enumeration import Enumeration
from hspylib.core.enum.http_code import HttpCode
from hspylib.core.meta.singleton import Singleton
from hspylib.core.tools.commons import __version__, sysout, syserr

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The directory containing all template files
TEMPLATES = (HERE / "templates")

# The directory containing the welcome message
WELCOME = (HERE / "welcome.txt")

VERSION = __version__(f"{HERE}/.version")

USAGE = """
Usage: hspylib [options] <arguments>

    HSPyLib Manager v{} - Manage HSPyLib applications.

    Options:
      -v  |  --version                                      : Display current program version.
      -h  |     --help                                      : Display this help message.
      -c  |     --create <type> <app_name> [dest_dir]     : Manage an HSPyLib application.

    Arguments:
      type      : One of basic|gradle|git|all. "basic" is going to scaffold a basic app based on HSPyLib application 
                  structure. "gradle" is going to initialize you project with gradle (requires gradle installed). 
                  "git" is going to initialize a git repository. "all" is going to create a gradle project and also
                  initialize a git repository.

""".format('.'.join(map(str, VERSION)))

GRADLE_PROPS = f"""
project.ext.set("projectVersion", '0.1.0')
project.ext.set("pythonVersion", '3')
project.ext.set("pyrccVersion", '5')
"""


class Main(metaclass=Singleton):

    class AppType(Enumeration):
        BASIC = 1
        GRADLE = 2
        GIT = 4
        ALL = 8

    def __init__(self):
        super().__init__()
        self.app_dir = None
        self.init_gradle = False
        self.init_git = False

    def run(self, arguments: List[str]) -> None:
        if len(arguments) == 0:
            welcome = WELCOME.read_text()
            sysout(f"{welcome}")
            sysout(USAGE)
        else:
            try:
                opts, args = getopt.getopt(arguments, 'hvc:', ['--help', '--version', '--create'])
                for op, arg in opts:
                    if op in ['-h', '--help']:
                        sysout(USAGE)
                    elif op in ['-v', '--version']:
                        sysout('.'.join(map(str, VERSION)))
                    elif op in ['-c', '--create']:
                        assert arg.lower() in ['basic', 'gradle', 'git', 'all'], f'Invalid type: {arg}'
                        assert len(args) > 0, f'Invalid arguments: {str(args)}'
                        self._create_app(
                            Main.AppType.value_of(arg, ignore_case=True),
                            args[0],
                            args[1] if len(args) > 1 else os.environ.get('HOME'))
            except getopt.GetoptError as err:
                sysout(f"%RED%### Unhandled option: {str(err)}")
                sysout(USAGE)

    def _create_app(self, app_type: AppType, app_name: str, dest_dir: str):
        sysout(f'Creating app: {app_name} -> {dest_dir} ...')
        try:
            assert os.path.exists(dest_dir), f'Destination not found: {dest_dir}'
            self.app_dir = f'{dest_dir}/{app_name}'
            sysout(f'App: {app_name}')
            self._mkdir('')
            self._mkdir(f'resources')
            self._mkfile(f'resources/application.properties', '# Main application property file')
            self._mkdir(f'resources/log')
            self._mkfile(f'__main__.py', (TEMPLATES / "tpl-main.py").read_text())
            self._mkfile(f'run-it.sh', (TEMPLATES / "tpl-run-it.sh").read_text())
            self._mkfile(f'README.md', f'# {app_name}')
            self._mkfile(f'.env', '# Type in here the environment variables your app requires')
            self._mkfile(f'.version', '0.1.0')
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
        self._mkfile('properties.gradle', GRADLE_PROPS)
        self._mkfile(f'build.gradle', (TEMPLATES / "tpl-build.gradle").read_text())
        self._mkfile(f'gradle/dependencies.gradle', (TEMPLATES / "tpl-dependencies.gradle").read_text())

    def _download_ext(self, extension: str):
        resp = get(f'https://raw.githubusercontent.com/yorevs/hspylib/master/gradle/{extension}')
        assert resp.status_code == HttpCode.OK, f'Unable to download {extension}'
        self._mkfile(f'gradle/{extension}', resp.body)

    def _init_git(self):
        self._mkfile(f'resources/log/.gitkeep', '')
        self._mkfile(f'.gitignore', (TEMPLATES / "tpl.gitignore").read_text())
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
    Main().INSTANCE.run(sys.argv[1:])
