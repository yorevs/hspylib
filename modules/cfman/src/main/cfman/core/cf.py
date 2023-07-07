#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib-CFMan
   @package: cfman.core
      @file: cf.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""
from clitt.core.term.terminal import Terminal
from collections import namedtuple
from hspylib.core.metaclass.singleton import Singleton
from hspylib.modules.application.exit_status import ExitStatus
from typing import List, Optional

CFTarget = namedtuple("CFTarget", ["user", "org", "space", "connected"])


class CloudFoundry(metaclass=Singleton):
    """Cloud Foundry command line tool wrapper."""

    INSTANCE = None

    @staticmethod
    def _get_part(parts: List[str], number: int) -> Optional[str]:
        """TODO"""
        ret_val = None
        if len(parts) > number:
            part = parts[number].split(":")
            ret_val = part[1].strip() if len(part) > 1 else None

        return ret_val

    @staticmethod
    def _check_result(result_str: str) -> Optional[str]:
        """TODO"""
        return result_str if result_str and "FAILED" not in str(result_str) else None

    def __init__(self) -> None:
        self._logged = False
        self._target = None
        self._last_output = None
        self._last_exit_code = None

    @property
    def last_output(self) -> str:
        return self._last_output

    @property
    def last_exit_code(self) -> ExitStatus:
        return self._last_exit_code

    def is_targeted(self) -> bool:
        """TODO"""
        return self._target and all(attr for attr in self._target)

    # Before getting started
    def is_logged(self) -> bool:
        """Checks whether it is connected to a CloudFoundry API endpoint."""
        if not self._logged:
            result = self._exec("orgs")
            self._logged = self._check_result(result) is not None
        return self._logged

    # Access management
    def api(self, url: str | None = None) -> Optional[str]:
        """Set or View targeted API url.
        :param url the cf API URL.
        """
        return self._check_result(self._exec(f"api {url or ''}"))

    # Authorization management
    def auth(self, username: str, password: str) -> bool:
        """Authorize a CloudFoundry user."""
        return self._check_result(self._exec(f"auth {username} {password}")) is not None

    # Target management
    def target(self, **kwargs) -> CFTarget:
        """Set or View the targeted ORG / SPACE.
        Kwargs:
          username(str): the logged username.
              org (str): the organization name.
            space (str): the space name.
        :param kwargs arbitrary CF command keyword arguments.
        """
        target_params = ["target"]
        if not kwargs and (parts := self._exec("target").splitlines()):
            if len(parts) >= 4:
                user = self._get_part(parts, 2)
                org = self._get_part(parts, 3)
                space = self._get_part(parts, 4)
                self._target = CFTarget(user, org, space, True)
        else:
            org = kwargs["org"] if "org" in kwargs else None
            space = kwargs["space"] if "space" in kwargs else None
            if org:
                target_params.append("-o")
                target_params.append(kwargs["org"])
            if space:
                target_params.append("-s")
                target_params.append(kwargs["space"])
            Terminal.echo(
                f"%BLUE%Targeting" f"{'  ORG=' + org if org else ''}" f"{'  SPACE=' + space if space else ''}" "..."
            )
            self._target = CFTarget(
                kwargs["user"] if "user" in kwargs else None,
                kwargs["org"] if "org" in kwargs else None,
                kwargs["space"] if "space" in kwargs else None,
                self._check_result(self._exec(" ".join(target_params))) is not None,
            )

        return self._target

    # Target management
    def clear_target(self) -> None:
        """Re-target for a new ORG/SPACE target."""
        self._target = None

    # Space management
    def spaces(self) -> Optional[List[str]]:
        """List all spaces from organization."""
        all_spaces = self._exec("spaces")
        return all_spaces.split("\n")[3:] if self._check_result(all_spaces) else None

    # Organization management
    def orgs(self) -> Optional[List[str]]:
        """List all organizations from API endpoint."""
        all_orgs = self._exec("orgs")
        return all_orgs.split("\n")[3:] if self._check_result(all_orgs) else None

    # Application action: Retrieve apps
    def apps(self) -> Optional[List[str]]:
        """List all applications from targeted ORG/SPACE."""
        all_apps = self._exec("apps")
        return all_apps.split("\n")[3:] if self._check_result(all_apps) else None

    # Application action: Start app
    def start(self, **kwargs) -> str:
        """Start an app.
        Kwargs:
            app (str): the application name.
        :param kwargs arbitrary CF command keyword arguments.
        """
        return self._exec(f"start {kwargs['app']}")

    # Application action: Stop app
    def stop(self, **kwargs) -> str:
        """Stop an app.
        Kwargs:
            app (str): the application name.
        :param kwargs arbitrary CF command keyword arguments.
        """
        return self._exec(f"stop {kwargs['app']}")

    # Application action: Restart app
    def restart(self, **kwargs) -> str:
        """Stop all instances of the app, then start them again. This causes downtime.
        Kwargs:
            app (str): the application name.
        :param kwargs arbitrary CF command keyword arguments.
        """
        return self._exec(f"restart {kwargs['app']}")

    # Application action: Restage app
    def restage(self, **kwargs) -> str:
        """Recreate the app's executable artifact using the latest pushed app files and the latest environment
        (variables, service bindings, buildpack, stack, etc.). This action will cause app downtime.
        Kwargs:
            app (str): the application name.
        :param kwargs arbitrary CF command keyword arguments.
        """
        return self._exec(f"restage {kwargs['app']}")

    # Application action: Retrieve logs
    def logs(self, **kwargs) -> None:
        """Tail or show recent logs for an app
        Kwargs:
            app (str): the application name.
               recent: dump recent logs instead of tailing.
        :param kwargs arbitrary CF command keyword arguments.
        """
        Terminal.clear()
        Terminal.set_auto_wrap(True)
        return self._exec(cmd_line=f"logs {kwargs['app']} {'--recent' if 'recent' in kwargs else ''}", poll=True)

    # Execution of a CF command
    def _exec(self, cmd_line: str, poll: bool = False) -> Optional[str]:
        """Execute the CF command.
        :param cmd_line: the cf command line string
        :param poll: whether to poll or execute the command. If poll is set I/O events can be registered for any number
                     of file descriptors and the output will be continuously printed. If [ENTER] is hit, the polling
                     will terminate.
        """
        self._last_output = None
        if poll:
            Terminal.echo("%YELLOW%%EOL%Press [ENTER] to exit...%EOL%%NC%")
            Terminal.shell_poll(f"cf {cmd_line}")
        else:
            self._last_output, self._last_exit_code = Terminal.shell_exec(f"cf {cmd_line}")

        return self._last_output
