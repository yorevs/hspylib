#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.main.hspylib.addins.appman
      @file: appman.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

import os
from typing import Any

from hspylib.core.enums.enumeration import Enumeration
from hspylib.core.enums.http_code import HttpCode
from hspylib.core.meta.singleton import Singleton
from hspylib.core.tools.commons import get_path, syserr, sysout
from hspylib.modules.cli.vt100.terminal import Terminal
from hspylib.modules.fetch.fetch import get

HERE = get_path(__file__)


class AppManager(metaclass=Singleton):
    """TODO"""
    
    # The directory containing all template files
    TEMPLATES = (HERE / "templates")
    
    GRADLE_PROPS = """
project.ext.set("projectVersion", "{}")
project.ext.set("pythonVersion", "3")
project.ext.set("pyrccVersion", "5")
project.ext.set("author", "YourUser")
project.ext.set("mailTo", "YourEmail")
project.ext.set("siteUrl", "YourSiteUrl")
"""
    
    class AppType(Enumeration):
        """Possible application creation type"""
        BASIC = 1
        GRADLE = 2
        GIT = 4
        ALL = 8
    
    def __init__(self, parent: Any):
        self.parent = parent
        self.app_name = None
        self.app_dir = None
        self.init_gradle = False
        self.init_git = False
    
    def create_app(self, app_name: str, app_type: AppType, dest_dir: str) -> None:
        """Create the application based on the parameters"""
        sysout(f'Creating app: {app_name} -> {dest_dir} ...')
        try:
            assert os.path.exists(dest_dir), f'Destination not found: {dest_dir}'
            self.app_name = app_name
            self.app_dir = f'{dest_dir}/{app_name}'
            sysout(f'App: {app_name}')
            self._mkdir('')
            self._mkdir('src')
            self._mkdir('src/test')
            self._mkfile('src/test/test_main.py', (self.TEMPLATES / "tpl-test_main.py").read_text())
            self._mkdir('src/main')
            self._mkfile('src/main/__main__.py', (self.TEMPLATES / "tpl-main.py").read_text())
            self._mkfile('src/main/.version', '0.1.0')
            self._mkfile('src/main/usage.txt', (self.TEMPLATES / "tpl-usage.txt").read_text())
            self._mkdir('src/main/resources')
            self._mkdir('src/test/resources')
            self._mkfile('src/main/resources/application.properties', '# Main application property file')
            self._mkfile('src/test/resources/application-test.properties', '# Main test application property file')
            self._mkdir('src/main/resources/log')
            self._mkdir('src/test/resources/log')
            self._mkfile('README.md', f'# {app_name}')
            self._mkfile('MANIFEST.in')
            # TODO Create setup.py
            self._mkfile('.env', '# Type in here the environment variables your app requires')
            self._mkfile('run-it.sh', (self.TEMPLATES / "tpl-run-it.sh").read_text())
            os.chmod(f'{self.app_dir}/run-it.sh', 0o755)
            if app_type in [AppManager.AppType.GRADLE, AppManager.AppType.ALL]:
                self._init_gradle(app_name)
            if app_type in [AppManager.AppType.GIT, AppManager.AppType.ALL]:
                self._init_git()
        except OSError as err:
            syserr(f"Creation of the application {dest_dir}/{app_name} failed")
            syserr(str(err))
        else:
            sysout(f"Successfully created the application {dest_dir}/{app_name}")
    
    def _mkdir(self, dirname: str) -> None:
        """Create a directory from the destination path"""
        dir_path = f"{self.app_dir}/{dirname}"
        sysout(f'  |- {dir_path}')
        os.mkdir(dir_path)
    
    def _mkfile(self, filename: str, contents: str = '') -> None:
        """Create a file from the destination path with the specified contents"""
        file_path = f"{self.app_dir}/{filename}"
        sysout(f'  |- {file_path}')
        with open(f'{file_path}', 'w') as fh:
            fh.write(contents)
    
    def _init_gradle(self, app_name: str) -> None:
        """Initialize the as a gradle project"""
        sysout('Initializing gradle project')
        result = Terminal.shell_exec(
            f"gradle init --project-name {app_name} --type basic --dsl groovy", cwd=self.app_dir)
        sysout('Gradle execution result: {}'.format(result))
        sysout('Downloading gradle extensions')
        self._download_ext('badges.gradle')
        self._download_ext('build-info.gradle')
        self._download_ext('docker.gradle')
        self._download_ext('oracle.gradle')
        self._download_ext('pypi-publish.gradle')
        self._download_ext('python.gradle')
        version_string = '.'.join(map(str, self.parent.VERSION))
        self._mkfile('properties.gradle', self.GRADLE_PROPS.format(version_string).strip())
        self._mkfile(
            'build.gradle', (self.TEMPLATES / "tpl-build.gradle").read_text().replace('%APP_NAME%', self.app_name)
        )
        self._mkfile('gradle/dependencies.gradle', (self.TEMPLATES / "tpl-dependencies.gradle").read_text())
        result = Terminal.shell_exec(
            './gradlew build', cwd=self.app_dir)
        sysout('Gradle execution result: {}'.format(result))
    
    def _download_ext(self, extension: str) -> None:
        """Download a gradle extension from the HSPyLib repository"""
        resp = get(f'https://raw.githubusercontent.com/yorevs/hspylib/master/gradle/{extension}')
        assert resp.status_code == HttpCode.OK, f'Unable to download {extension}'
        self._mkfile(f'gradle/{extension}', resp.body)
    
    def _init_git(self) -> None:
        """Initialize a git repository for the project"""
        self._mkfile('src/main/resources/log/.gitkeep')
        self._mkfile('.gitignore', (self.TEMPLATES / "tpl.gitignore").read_text())
        sysout('Initializing git repository')
        result = Terminal.shell_exec(
            'git init', cwd=self.app_dir)
        sysout('Git init result: {}'.format(result))
        sysout('Creating first commit')
        Terminal.shell_exec(
            'git add .', cwd=self.app_dir)
        result = Terminal.shell_exec(
            'git commit -m "First commit [@HSPyLib]"', cwd=self.app_dir)
        sysout('Git commit result: {}'.format(result))
