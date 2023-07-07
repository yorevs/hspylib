#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib
   @package: clitt.utils
      @file: git_utils.py
   @created: Nov 14, 2019
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""
from clitt.core.term.terminal import Terminal
from hspylib.modules.application.exit_status import ExitStatus
from typing import Tuple


class GitTools:
    """TODO"""

    @staticmethod
    def top_level_dir() -> Tuple[str, ExitStatus]:
        """TODO"""
        return Terminal.shell_exec("git rev-parse --show-toplevel")

    @staticmethod
    def current_branch() -> Tuple[str, ExitStatus]:
        """TODO"""
        return Terminal.shell_exec("git symbolic-ref --short HEAD")

    @staticmethod
    def changelog(from_tag: str, to_tag: str) -> Tuple[str, ExitStatus]:
        """TODO"""
        return Terminal.shell_exec(f"git log --oneline --pretty='format:%h %ad %s' --date=short {from_tag}^..{to_tag}^")

    @staticmethod
    def unreleased() -> Tuple[str, ExitStatus]:
        """TODO"""
        latest_tag = Terminal.shell_exec("git describe --tags --abbrev=0 HEAD^")
        return Terminal.shell_exec(f"git log --oneline --pretty='format:%h %ad %s' --date=short '{latest_tag}'..HEAD")

    @staticmethod
    def release_date(tag_name: str) -> Tuple[str, ExitStatus]:
        """TODO"""
        return Terminal.shell_exec(f"git log -1 --pretty='format:%ad' --date=short {tag_name}")

    @staticmethod
    def tag_list() -> Tuple[str, ExitStatus]:
        """TODO"""
        return Terminal.shell_exec("git log --tags --simplify-by-decoration --pretty='format:%ci %d'")

    @staticmethod
    def create_tag(version: str, commit_id: str = "HEAD", description: str = None) -> Tuple[str, ExitStatus]:
        """TODO"""
        return Terminal.shell_exec(f"git tag -a v{version} {commit_id} -m '{description or version}'")

    @staticmethod
    def search_logs(filter_by: str = ".*") -> Tuple[str, ExitStatus]:
        """TODO"""
        return Terminal.shell_exec(f"git log --grep='{filter_by}' --pretty=format:'%h %ad %s' --date=short")

    @staticmethod
    def show_file(filename: str, commit_id: str = "HEAD") -> Tuple[str, ExitStatus]:
        return Terminal.shell_exec(f"git show {commit_id}:{filename}")
