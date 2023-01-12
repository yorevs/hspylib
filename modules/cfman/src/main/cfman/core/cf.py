#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib-CFMan
   @package: cfman.core
      @file: cf.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
import os
from typing import List, Optional

from hspylib.core.metaclass.singleton import Singleton
from hspylib.core.tools.commons import sysout
from hspylib.modules.cli.terminal import Terminal


class CloudFoundry(metaclass=Singleton):
    """Cloud Foundry command line tool python wrapper"""

    INSTANCE = None

    def __init__(self) -> None:
        self.connected = False
        self.targeted = {"org": None, "space": None, "targeted": False}
        self.last_result = None
        self.last_exit_code = None

    def is_targeted(self) -> bool:
        return self.targeted["org"] and self.targeted["space"] and self.targeted["targeted"]

    # Before getting started:
    def connect(self) -> bool:
        """Attempt to connect to CloudFoundry.
        """
        if not self.connected:
            result = self._exec("orgs")
            self.connected = result and "FAILED" not in str(result)
        return self.connected

    def api(self, url: str | None = None) -> Optional[str]:
        """Set or view target api url.
        :param url the cf API URL.
        """
        result = self._exec(f"api {url or ''}")
        return result if "FAILED" not in str(result) else None

    def auth(self, username: str, password: str) -> bool:
        """Authorize a CloudFoundry user.
        """
        result = self._exec(f"auth {username} {password}")
        return result and "FAILED" not in str(result)

    def target(self, **kwargs) -> dict:
        """Set or view the targeted org or space.
        Kwargs:
              org (str): the organization name.
            space (str): the space name.
        :param kwargs arbitrary cf command keyword arguments.
        """
        params = ["target"]
        if not kwargs and (parts := self._exec(" ".join(params)).split(os.linesep)):
            if len(parts) >= 4:
                org = parts[2].split(":")[1].strip()
                space = parts[3].split(":")[1].strip()
                self.targeted = {"org": org, "space": space, "targeted": True}
        else:
            if "org" in kwargs and kwargs["org"]:
                params.append("-o")
                params.append(kwargs["org"])
                self.targeted["org"] = kwargs["org"]
            if "space" in kwargs and kwargs["space"]:
                params.append("-s")
                params.append(kwargs["space"])
                self.targeted["space"] = kwargs["space"]
            result = self._exec(" ".join(params))
            self.targeted["targeted"] = result and "FAILED" not in str(result)

        return self.targeted

    # Space management
    def spaces(self) -> List[str]:
        """List all spaces from organization.
        """
        all_spaces = self._exec("spaces").split("\n")
        return all_spaces[3:] if all_spaces and "FAILED" not in str(all_spaces) else None

    # Org management
    def orgs(self) -> List[str]:
        """List all organizations.
        """
        all_orgs = self._exec("orgs").split("\n")
        return all_orgs[3:] if all_orgs and "FAILED" not in str(all_orgs) else None

    # Application lifecycle
    def apps(self) -> List[str]:
        """List all applications from targeted space.
        """
        all_apps = self._exec("apps").split("\n")
        return all_apps[4:] if all_apps and "FAILED" not in str(all_apps) else None

    # Application status
    def start(self, **kwargs) -> str:
        """Start an app.
        Kwargs:
            app (str): the application name.
        :param kwargs arbitrary cf command keyword arguments.
        """
        return self._exec(f"start {kwargs['app']}")

    # Application status
    def stop(self, **kwargs) -> str:
        """Stop an app.
        Kwargs:
            app (str): the application name.
        :param kwargs arbitrary cf command keyword arguments.
        """
        return self._exec(f"stop {kwargs['app']}")

    # Application status
    def restart(self, **kwargs) -> str:
        """Stop all instances of the app, then start them again. This causes downtime.
        Kwargs:
            app (str): the application name.
        :param kwargs arbitrary cf command keyword arguments.
        """
        return self._exec(f"restart {kwargs['app']}")

    # Application status
    def restage(self, **kwargs) -> str:
        """Recreate the app's executable artifact using the latest pushed app files and the latest environment
        (variables, service bindings, buildpack, stack, etc.). This action will cause app downtime.
        Kwargs:
            app (str): the application name.
        :param kwargs arbitrary cf command keyword arguments.
        """
        return self._exec(f"restage {kwargs['app']}")

    # Application logging
    def logs(self, **kwargs) -> None:
        """Tail or show recent logs for an app
        Kwargs:
            app (str): the application name.
               recent: dump recent logs instead of tailing.
        :param kwargs arbitrary cf command keyword arguments.
        """
        return self._exec(
            cmd_line=f"logs {kwargs['app']} {'--recent' if 'recent' in kwargs else ''}",
            poll=True
        )

    def _exec(self, cmd_line: str, poll: bool = False) -> Optional[str]:
        """Execute the cf command.
        :param cmd_line: the cf command line string
        :param poll: whether to poll or execute the command. If poll is set I/O events can be registered for any number
                     of file descriptors and the output will be continuously printed. If [ENTER] is hit, the polling
                     will terminate.
        """
        self.last_result = None

        if poll:
            sysout("%YELLOW%%EOL%Press [ENTER] to exit...%EOL%%NC%")
            Terminal.shell_poll(f"cf {cmd_line}")
        else:
            self.last_result, self.last_exit_code = Terminal.shell_exec(f"cf {cmd_line}")

        return self.last_result
