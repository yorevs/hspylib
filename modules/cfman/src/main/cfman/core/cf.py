#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.app.cfman.core
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
from hspylib.modules.cli.vt100.terminal import Terminal


class CloudFoundry(metaclass=Singleton):
    """Cloud Foundry command line tool python wrapper"""

    def __init__(self) -> None:
        self.connected = False
        self.targeted = {"org": None, "space": None, "targeted": False}
        self.last_result = None
        self.last_exit_code = None

    def is_targeted(self) -> bool:
        return self.targeted["org"] and self.targeted["space"] and self.targeted["targeted"]

    # Before getting started:
    def connect(self) -> bool:
        """Attempt to connect to CloudFoundry"""
        if not self.connected:
            result = self._exec("orgs")
            self.connected = result and "FAILED" not in str(result)
        return self.connected

    def api(self, api: str | None = None) -> Optional[str]:
        """Set or view target api url"""
        result = self._exec(f"api {api or ''}")
        return result if "FAILED" not in str(result) else None

    def auth(self, username: str, password: str) -> bool:
        """Authorize a CloudFoundry user"""
        result = self._exec(f"auth {username} {password}")
        return result and "FAILED" not in str(result)

    def target(self, **kwargs) -> dict:
        """Set or view the targeted org or space"""
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
        """List all spaces from organization"""
        all_spaces = self._exec("spaces").split("\n")
        return all_spaces[3:] if all_spaces and "FAILED" not in str(all_spaces) else None

    # Org management
    def orgs(self) -> List[str]:
        """List all organizations"""
        all_orgs = self._exec("orgs").split("\n")
        return all_orgs[3:] if all_orgs and "FAILED" not in str(all_orgs) else None

    # Application lifecycle:
    def apps(self) -> List[str]:
        """List all applications from targeted space"""
        all_apps = self._exec("apps").split("\n")
        return all_apps[4:] if all_apps and "FAILED" not in str(all_apps) else None

    def start(self, **kwargs) -> str:
        """Start an app"""
        return self._exec(f"start {kwargs['app']}")

    def stop(self, **kwargs) -> str:
        """Stop an app"""
        return self._exec(f"stop {kwargs['app']}")

    def restart(self, **kwargs) -> str:
        """Stop all instances of the app, then start them again. This causes downtime."""
        return self._exec(f"restart {kwargs['app']}")

    def restage(self, **kwargs) -> str:
        """Recreate the app's executable artifact using the latest pushed app files and the latest environment
        (variables, service bindings, buildpack, stack, etc.). This action will cause app downtime."""
        return self._exec(f"restage {kwargs['app']}")

    def logs(self, **kwargs) -> None:
        """Tail or show recent logs for an app"""
        return self._exec(f"logs {kwargs['app']} {'--recent' if 'recent' in kwargs else ''}")

    def _exec(self, cmd_line: str, pool: bool = False) -> Optional[str]:
        """TODO"""
        if pool:
            Terminal.shell_poll(f"cf {cmd_line}")
            return None
        self.last_result, self.last_exit_code = Terminal.shell_exec(f"cf {cmd_line}")
        return self.last_result
