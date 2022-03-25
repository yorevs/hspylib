#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: main.tools
   @file: git_tools.py
  @created: Nov 14, 2019
   @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior
     @site: https://github.com/yorevs/homesetup
  @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

from hspylib.modules.cli.vt100.terminal import Terminal


class GitTools:
    """TODO"""

    @staticmethod
    def top_level_dir() -> str:
        """TODO"""
        return Terminal.shell_exec('git rev-parse --show-toplevel')

    @staticmethod
    def current_branch() -> str:
        """TODO"""
        return Terminal.shell_exec('git symbolic-ref --short HEAD')

    @staticmethod
    def changelog(from_tag: str, to_tag: str) -> str:
        """TODO"""
        return Terminal.shell_exec(f"git log --oneline --pretty='format:%h %ad %s' --date=short {from_tag}^..{to_tag}^")

    @staticmethod
    def unreleased() -> str:
        """TODO"""
        latest_tag = Terminal.shell_exec('git describe --tags --abbrev=0 HEAD^')
        return Terminal.shell_exec(f"git log --oneline --pretty='format:%h %ad %s' --date=short '{latest_tag}'..HEAD")

    @staticmethod
    def release_date(tag_name: str) -> str:
        """TODO"""
        return Terminal.shell_exec(f"git log -1 --pretty='format:%ad' --date=short {tag_name}")

    @staticmethod
    def tag_list() -> str:
        """TODO"""
        return Terminal.shell_exec("git log --tags --simplify-by-decoration --pretty='format:%ci %d'")

    @staticmethod
    def create_tag(version: str, commit_id: str = 'HEAD', description: str = None) -> str:
        """TODO"""
        return Terminal.shell_exec(f"git tag -a v{version} {commit_id} -m '{description or version}'")

    @staticmethod
    def search_logs(filter_by: str = '.*') -> str:
        """TODO"""
        return Terminal.shell_exec(f"git log --grep='{filter_by}' --pretty=format:'%h %ad %s' --date=short")

    @staticmethod
    def show_file(filename: str, commit_id: str = 'HEAD') -> str:
        return Terminal.shell_exec(f"git show {commit_id}:{filename}")
