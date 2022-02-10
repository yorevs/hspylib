#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   hspylib.main.hspylib.addons.appman
      @file: appman.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

import os
from typing import List

from hspylib.addons.appman.app_extension import AppExtension
from hspylib.addons.appman.app_type import AppType
from hspylib.core.enums.http_code import HttpCode
from hspylib.core.metaclass.singleton import Singleton
from hspylib.core.tools.commons import get_path, syserr, sysout
from hspylib.core.tools.preconditions import check_argument
from hspylib.core.tools.text_tools import camelcase
from hspylib.modules.cli.application.application import Application
from hspylib.modules.cli.vt100.terminal import Terminal
from hspylib.modules.fetch.fetch import get

HERE = get_path(__file__)


class AppManager(metaclass=Singleton):
    """HSPyLib application manager that helps creating HSPyLib based applications and widgets"""

    # The directory containing all template files
    TEMPLATES = (HERE / "templates")

    # The general gradle properties
    GRADLE_PROPS = """
project.ext.set("projectVersion", "{}")
project.ext.set("pythonVersion", "3")
project.ext.set("pyrccVersion", "5")
project.ext.set("author", "YourUser")
project.ext.set("mailTo", "YourEmail")
project.ext.set("siteUrl", "YourSiteUrl")
"""

    def __init__(self, parent_app: Application):
        self._parent_app = parent_app
        self._app_name = None
        self._app_dir = None
        self._init_gradle_flag = False
        self._init_git_flag = False

    def create(self, app_name: str, app_type: AppType, app_ext: List[AppExtension], dest_dir: str) -> None:
        """Create the application based on the parameters"""
        sysout(f'Creating app: {app_name} -> {dest_dir} ...')
        try:
            check_argument(os.path.exists(dest_dir), 'Destination not found: {}', dest_dir)
            self._app_name = app_name
            if app_type == AppType.APP:
                self._app_dir = f'{dest_dir}/{app_name}'
                self._create_app(app_name, app_ext)
            elif app_type == AppType.WIDGET:
                self._app_dir = f'{dest_dir}'
                self._create_widget(app_name)
            elif app_type == AppType.QT_APP:
                self._app_dir = f'{dest_dir}/{app_name}'
                self._create_qt_app(app_name, app_ext)
        except OSError as err:
            syserr(f"Creation of the application {dest_dir}/{app_name} failed")
            syserr(str(err))
        else:
            sysout(f"Successfully created the {app_type.value} {app_name}")

    def _create_app(self, app_name: str, extensions: List[AppExtension]) -> None:
        """Create a Simple HSPyLib application"""
        sysout(f'Application: {app_name}')
        self._create_base_app_struct(app_name)
        self._mkfile('src/main/__main__.py', (self.TEMPLATES / "tpl-main.py").read_text())
        self._mkfile('src/main/usage.txt', (self.TEMPLATES / "tpl-usage.txt").read_text())
        self._apply_extensions(extensions, app_name)

    def _create_qt_app(self, app_name: str, extensions: List[AppExtension]) -> None:
        """Create an HSPyLib QT application"""
        sysout(f'QT Application: {app_name}')
        self._create_base_app_struct(app_name)
        self._mkdir('src/main/resources/forms')
        self._mkfile('src/main/resources/forms/main_qt_view.ui', (self.TEMPLATES / "tpl-main_qt_view.ui").read_text())
        self._mkfile('src/main/__main__.py', (self.TEMPLATES / "tpl-main-qt.py").read_text())
        self._apply_extensions(extensions, app_name)

    def _create_base_app_struct(self, app_name):
        """Create HSPyLib application structure"""
        self._mkdir()
        self._mkfile('README.md', f'# {app_name}')
        self._mkfile('MANIFEST.in')
        self._mkdir('src')
        self._mkdir('src/test')
        self._mkfile('src/test/test_main.py', (self.TEMPLATES / "tpl-test_main.py").read_text())
        self._mkdir('src/test/resources')
        self._mkdir('src/test/resources/log')
        self._mkfile('src/test/resources/application-test.properties', '# Main test application property file')
        self._mkdir('src/main')
        self._mkfile('src/main/.version', '0.1.0')
        self._mkdir('src/main/resources')
        self._mkfile('src/main/resources/application.properties', '# Main application property file')
        self._mkdir('src/main/resources/log')
        self._mkfile('.env', '# Type in here the environment variables your app requires')
        self._mkfile('run.sh', (self.TEMPLATES / "tpl-run.sh").read_text())
        os.chmod(f'{self._app_dir}/run.sh', 0o755)

    def _apply_extensions(self, extensions: List[AppExtension], app_name: str):
        """Apply the selected extensions to the app"""
        if AppExtension.GRADLE in extensions:
            sysout('Applying gradle extensions')
            self._init_gradle(app_name)
        if AppExtension.GIT in extensions:
            sysout('Initializing git repository')
            self._init_git()

    def _create_widget(self, app_name: str) -> None:
        """Create an HSPyLib Widget application"""
        widget_name = camelcase(app_name).replace('_', '').replace(' ', '')
        sysout(f'Widget: {widget_name}')
        self._mkfile(
            f"widget_{app_name.lower()}.py",
            (self.TEMPLATES / "tpl-widget.py").read_text().replace('_WIDGET_NAME_', f"{widget_name}")
        )

    def _mkdir(self, dirname: str = '') -> None:
        """Create a directory from the destination path, or the destination path itself"""
        dir_path = f"{self._app_dir}/{dirname}"
        sysout(f'  |- {dir_path}')
        os.mkdir(dir_path)

    def _mkfile(self, filename: str, contents: str = '') -> None:
        """Create a file from the destination path with the specified contents"""
        file_path = f"{self._app_dir}/{filename}"
        sysout(f'  |- {file_path}')
        with open(f'{file_path}', 'w') as fh:
            fh.write(contents)

    def _init_gradle(self, app_name: str) -> None:
        """Initialize the as a gradle project"""
        sysout('Initializing gradle project')
        result = Terminal.shell_exec(
            f"gradle init --project-name {app_name} --type basic --dsl groovy", cwd=self._app_dir)
        sysout('Gradle execution result: {}'.format(result))
        sysout('Downloading gradle extensions')
        self._download_ext('badges.gradle')
        self._download_ext('build-info.gradle')
        self._download_ext('docker.gradle')
        self._download_ext('oracle.gradle')
        self._download_ext('pypi-publish.gradle')
        self._download_ext('python.gradle')
        version_string = '.'.join(map(str, self._parent_app.VERSION))
        self._mkfile('properties.gradle', self.GRADLE_PROPS.format(version_string).strip())
        self._mkfile(
            'build.gradle', (self.TEMPLATES / "tpl-build.gradle").read_text().replace('%APP_NAME%', self._app_name)
        )
        self._mkfile('gradle/dependencies.gradle', (self.TEMPLATES / "tpl-dependencies.gradle").read_text())
        result = Terminal.shell_exec(
            './gradlew build', cwd=self._app_dir)
        sysout('Gradle execution result: {}'.format(result))

    def _download_ext(self, extension: str) -> None:
        """Download a gradle extension from the HSPyLib repository"""
        resp = get(f'https://raw.githubusercontent.com/yorevs/hspylib/master/gradle/{extension}')
        check_argument(resp.status_code == HttpCode.OK, 'Unable to download {}', extension)
        self._mkfile(f'gradle/{extension}', resp.body)

    def _init_git(self) -> None:
        """Initialize a git repository for the project"""
        self._mkfile('src/main/resources/log/.gitkeep')
        self._mkfile('.gitignore', (self.TEMPLATES / "tpl.gitignore").read_text())
        sysout('Initializing git repository')
        result = Terminal.shell_exec(
            'git init', cwd=self._app_dir)
        sysout('Git init result: {}'.format(result))
        sysout('Creating first commit')
        Terminal.shell_exec(
            'git add .', cwd=self._app_dir)
        result = Terminal.shell_exec(
            'git commit -m "First commit [@HSPyLib]"', cwd=self._app_dir)
        sysout('Git commit result: {}'.format(result))
