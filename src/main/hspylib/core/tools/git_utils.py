"""
  @package: deployer
   @script: git_utils.py
  @purpose: Provides some git utilities.
  @created: Nov 14, 2019
   @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior
   @mailto: yorevs@hotmail.com
     @site: https://github.com/yorevs/homesetup
  @license: Please refer to <https://opensource.org/licenses/MIT>
"""

from hspylib.modules.cli.vt100.terminal import Terminal


class GitUtils:

    @staticmethod
    def top_level_dir():
        return Terminal.shell_exec('git rev-parse --show-toplevel')

    @staticmethod
    def current_branch():
        return Terminal.shell_exec('git symbolic-ref --short HEAD')

    @staticmethod
    def changelog(from_tag, to_tag):
        return Terminal.shell_exec(f'git log --oneline --pretty=format:%h %ad %s --date=short {from_tag}^..{to_tag}^')

    @staticmethod
    def unreleased():
        latest_tag = Terminal.shell_exec('git describe --tags --abbrev=0 HEAD^')
        return Terminal.shell_exec(f'git log --oneline --pretty=format:%h %ad %s --date=short {latest_tag}..HEAD')

    @staticmethod
    def release_date(tag_name):
        return Terminal.shell_exec(f'git log -1 --format=%ad --date=short {tag_name}')

    @staticmethod
    def tag_list():
        return Terminal.shell_exec('git tag')


if __name__ == '__main__':
    GitUtils.unreleased()
