"""
  @package: deployer
   @script: versioner.py
  @purpose: Provides an engine to handle app versions.
  @created: Nov 14, 2019
   @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior
   @mailto: yorevs@hotmail.com
     @site: https://github.com/yorevs/homesetup
  @license: Please refer to <https://opensource.org/licenses/MIT>
"""
import fileinput
import os
from typing import List

from hspylib.core.meta.singleton import Singleton
from hspylib.core.tools.commons import run_dir
from versioner.src.main.entity.version import Version
from versioner.src.main.enums.extension import Extension
from versioner.src.main.exception.exceptions import MissingExtensionError


class Versioner(metaclass=Singleton):
    """
        Labels:
            MAJOR version when you make incompatible API changes.
            MINOR version when you add functionality in a backwards compatible manner.
            PATCH version when you make backwards compatible bug fixes.

        @Additional labels for pre-release and build metadata are available as extensions to the
                    MAJOR.MINOR.PATCH format.

        Extensions:
            SNAPSHOT => STABLE => RELEASE
    """

    def __init__(self, initial_version: str, search_dir: str, files: List[str]):
        self.initial_version = initial_version
        self.version = Version.of(initial_version)
        self.cb_handler = {
            'major': self.major,
            'minor': self.minor,
            'patch': self.patch,
            'release': self.promote,
        }
        self.search_dir = search_dir if search_dir else run_dir()
        self.files = self._assert_exist([f"{search_dir}/{f}" for f in files])

    def promote(self) -> Version:
        """ Promote the current version in the order: SNAPSHOT->STABLE->RELEASE """
        self._assert_state()
        if self.version.state and self.version.state != Extension.RELEASE:
            self.version.state = Extension.STABLE if self.version.state == Extension.SNAPSHOT else Extension.RELEASE
            print(f"Version has been promoted to {self.version}")
        return self.version

    def demote(self) -> Version:
        """ Demote the current version in the order: RELEASE->STABLE->SNAPSHOT """
        self._assert_state()
        if self.version.state and self.version.state != Extension.SNAPSHOT:
            self.version.state = Extension.STABLE if self.version.state == Extension.RELEASE else Extension.SNAPSHOT
            print(f"Version has been demoted to {self.version}")
        return self.version

    def major(self) -> Version:
        """ Update current major part of the version """
        self.version.major += 1
        self.version.minor = 0
        self.version.patch = 0
        self.version.state = Extension.SNAPSHOT if self.version.state else None
        print(f"Major has been updated to {self.version}")
        return self.version

    def minor(self) -> Version:
        """ Update current minor part of the version """
        self.version.minor += 1
        self.version.patch = 0
        self.version.state = Extension.SNAPSHOT if self.version.state else None
        print(f"Minor has been updated to {self.version}")
        return self.version

    def patch(self) -> Version:
        """ Update current patch part of the version """
        self.version.patch += 1
        self.version.state = Extension.SNAPSHOT if self.version.state else None
        print(f"Patch has been updated to {self.version}")
        return self.version

    def _assert_state(self):
        if not self.version.state:
            raise MissingExtensionError(
                f"Version {self.version} is not promotable/demotable. Required extension, one of {Extension.names()}")

    def _assert_exist(self, files: List[str]) -> List[str]:
        assert files and all(os.path.exists(path) for path in files), \
            "All files must exist in \"{}\" and be writable: {}".format(self.search_dir, files)
        return files

    def save(self):
        for filename in self.files:
            with fileinput.FileInput(filename, inplace=True, backup='.bak') as file:
                for line in file:
                    print(line.replace(self.initial_version, str(self.version)), end='')
