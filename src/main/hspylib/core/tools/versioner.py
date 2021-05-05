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

import re
from os.path import exists

"""
Labels:
    MAJOR version when you make incompatible API changes.
    MINOR version when you add functionality in a backwards compatible manner.
    PATCH version when you make backwards compatible bug fixes.

@Additional labels for pre-release and build metadata are available as extensions to the MAJOR.MINOR.PATCH format.

Extensions:
    SNAPSHOT => STABLE => RELEASE
"""


class Versioner:
    """ TODO Comment it """

    def __init__(self, version_field, version_file):
        self.version = [0, 0, 0]
        self.release = 'SNAPSHOT'
        self.file = version_file
        self.field = version_field
        self.mappings = {
            'major': {'max_value': 100, 'upd_fn': self.update_major},
            'minor': {'max_value': 20, 'upd_fn': self.update_minor},
            'patch': {'max_value': 10, 'upd_fn': self.update_patch}
        }
        if self.field not in self.mappings:
            raise Exception('Invalid field \"{}\". Please use one of: {}'.format(self.field, self.mappings.keys()))

    def __str__(self):
        return '%d.%d.%03d-%s' % (self.version[0], self.version[1], self.version[2], self.release)

    def current(self):
        """ TODO Comment it """
        self.read_file()
        return self.__str__()

    def max_value(self, field):
        """ TODO Comment it """
        return self.mappings[field]['max_value'] if self.mappings[field]['max_value'] is not None else 0

    def reset(self):
        """ TODO Comment it """
        self.version = [0, 9, 0]

    def update_version(self):
        """ TODO Comment it """
        self.mappings[self.field]['upd_fn']()
        self.write_file()
        print('Version updated to {}'.format(self))

    def promote_release(self):
        """ TODO Comment it """
        if self.release != 'RELEASE':
            self.release = 'RELEASE' if self.release == 'STABLE' else 'STABLE'
            print('Version has been promoted to {}'.format(self))

    def demote_release(self):
        """ TODO Comment it """
        if self.release != 'SNAPSHOT':
            self.release = 'STABLE' if self.release == 'RELEASE' else 'SNAPSHOT'
            print('Version has been demoted to {}'.format(self))

    def update_patch(self):
        """ TODO Comment it """
        self.version[2] += 1
        if self.version[2] > self.max_value('patch'):
            self.update_minor()

    def update_minor(self):
        """ TODO Comment it """
        self.version[2] = 0
        self.version[1] += 1
        if self.version[1] > self.max_value('minor'):
            self.update_major()

    def update_major(self):
        """ TODO Comment it """
        self.version[2] = 0
        self.version[1] = 0
        self.version[0] += 1
        if self.version[0] > self.max_value('major'):
            raise Exception('Major number has reached it\'s maximum value of {}'.format(self.max_value('major')))

    def read_file(self):
        """ TODO Comment it """
        if not exists(self.file):
            self.reset()
            self.write_file()
        with open(self.file, 'r') as fh:
            contents = fh.read().strip()
            self.version = map(int, re.sub('[-.][A-Z]*$', '', contents).split('.'))
            self.release = re.sub('([0-9]+\\.?){3}[-.]', '', contents).upper()

    def write_file(self):
        """TODO Comment it """
        with open(self.file, 'w') as fh_version:
            fh_version.seek(0)
            fh_version.write(str(self))
            fh_version.truncate()
