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
from hspylib.core.meta.singleton import Singleton
from versioner.src.main.entity.version import Version
from versioner.src.main.enums.extension import Extension


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

    def __init__(self):
        self.cb_handler = {
            'major': self.major,
            'minor': self.minor,
            'patch': self.patch,
            'release': self.promote,
        }

    @classmethod
    def promote(cls, version: Version) -> Version:
        """ Promote the current version in the order: SNAPSHOT->STABLE->RELEASE """
        if version.state and version.state != Extension.RELEASE:
            version.state = Extension.STABLE if version.state == Extension.SNAPSHOT else Extension.RELEASE
            print(f"Version has been promoted to {version}")
        return version

    @classmethod
    def demote(cls, version: Version) -> Version:
        """ Demote the current version in the order: RELEASE->STABLE->SNAPSHOT """
        if version.state and version.state != Extension.SNAPSHOT:
            version.state = Extension.STABLE if version.state == Extension.RELEASE else Extension.SNAPSHOT
            print(f"Version has been demoted to {version}")
        return version

    @classmethod
    def major(cls, version: Version) -> Version:
        """ Update current major part of the version """
        version.major += 1
        version.minor = 0
        version.patch = 0
        version.state = Extension.SNAPSHOT
        print(f"Major has been updated to {version}")
        return version

    @classmethod
    def minor(cls, version: Version) -> Version:
        """ Update current minor part of the version """
        version.minor += 1
        version.patch = 0
        version.state = Extension.SNAPSHOT
        print(f"Minor has been updated to {version}")
        return version

    @classmethod
    def patch(cls, version: Version) -> Version:
        """ Update current patch part of the version """
        version.patch += 1
        version.state = Extension.SNAPSHOT
        print(f"Patch has been updated to {version}")
        return version
