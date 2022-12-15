#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.app.cfman.core
      @file: cf_manager.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
from cfman.core.cf import CloudFoundry
from cfman.core.cf_application import CFApplication
from cfman.core.cf_endpoint import CFEndpoint
from cfman.exception.exceptions import CFAuthenticationError, CFConnectionError, CFExecutionError
from hspylib.core.enums.http_code import HttpCode
from hspylib.core.tools.commons import file_is_not_empty, str_to_bool, syserr, sysout
from hspylib.modules.cache.ttl_cache import TTLCache
from hspylib.modules.cli.tui.mchoose import mchoose
from hspylib.modules.cli.tui.minput.minput import MenuInput, minput
from hspylib.modules.cli.tui.mselect import mselect
from hspylib.modules.cli.tui.menu.menu_utils import MenuUtils
from hspylib.modules.fetch.fetch import head
from time import sleep
from typing import List, Optional

import sys


class CFManager:
    """Represents the cloud foundry manager application and it's functionalities"""

    CF_ACTIONS = ["Logs", "Restart", "Restage", "Status", "Start", "Stop", "Target"]

    @staticmethod
    def _abort():
        sys.exit(1)

    @staticmethod
    def _allow_multiple(action: str) -> bool:
        """Checks whether the action allows multiple apps selection or not"""
        return action.lower() not in ["logs", "target"]

    @staticmethod
    def _is_callable(action: str) -> bool:
        """Checks whether the action is callable or not"""
        return action.lower() not in ["status", "target"]

    def __init__(self, api: str, org: str, space: str, username: str, password: str, refresh: str, cf_endpoints: str):
        assert file_is_not_empty(cf_endpoints), f"CF Endpoints file {cf_endpoints} is empty or does not exist !"
        self._cf = CloudFoundry()
        self._cache = TTLCache()
        self._api = api
        self._org = org
        self._space = space
        self._username = username
        self._password = password
        self._refresh = str_to_bool(refresh or "false")
        self._cf_endpoints_file = cf_endpoints
        self._cf_apps = None
        self._done = False

    def run(self) -> None:
        """Execute main cf manager routines"""
        sysout("%GREEN%Checking CloudFoundry authorization...")
        if self._cf.connect():
            sysout("%GREEN%Already authorized to CloudFoundry!")
        else:
            authorized = False
            sysout("%YELLOW%Not authorized to CloudFoundry, login required...")
            while not authorized:
                if not self._api:
                    sleep(1)
                    self._select_endpoint()
                if not self._username or not self._password:
                    sleep(1)
                    self._require_credentials()
                sysout(f"%GREEN%Authorizing {self._username}@{self._api}...")
                authorized = self._authorize()
                if not authorized:
                    self._password = None
                    sleep(1)
            sysout("%GREEN%Successfully authorized!")

        self._loop_actions()

    def _get_apps(self) -> List[CFApplication]:
        """Retrieve all cf applications under the target/org"""
        sysout(f'%GREEN%Retrieving applications from space: "{self._space}"...')
        if self._refresh or not (apps := self._cache.read(f"cf-apps-{self._space}")):
            apps = self._cf.apps()
            self._cache.save(f"cf-apps-{self._space}", apps)
        cf_apps = list(map(CFApplication.of, apps if apps else []))
        if not cf_apps:
            if "OK" not in self._cf.last_result:
                raise CFExecutionError(f"Unable to retrieve applications: => {self._cf.last_result}")
            sysout(f"%YELLOW%No apps found for space {self._space}")
        self._cf_apps = cf_apps

        return self._cf_apps

    def _select_endpoint(self) -> None:
        """Select the PCF endpoint to connect to"""
        try:
            with open(self._cf_endpoints_file, "r", encoding="utf-8") as f_hosts:
                endpoints = list(map(lambda l: CFEndpoint(l.split(",")), f_hosts.readlines()))
                if len(endpoints) > 0:
                    selected = mselect(endpoints, title="Please select an endpoint")
                    if not selected:
                        self._abort()
                    sysout(f"%GREEN%Connecting to endpoint: {selected}...")
                    try:
                        response = head(selected.host)
                        if response.status_code and HttpCode.OK:
                            self._api = selected.host
                        else:
                            syserr(f"Failed to connect to API ({response.status_code}): {selected}")
                            self._abort()
                    except Exception as err:
                        raise CFConnectionError(f"Failed to connect to API => {selected.host}") from err
                else:
                    syserr(
                        f"No endpoint yet configured. Please create the file {self._cf_endpoints_file} "
                        f"with at least one endpoint configured and try again."
                    )
                    self._abort()
        except IndexError:
            syserr(
                f"{self._cf_endpoints_file} "
                f"has invalid cf endpoints format. Please use: <alias>, <url>, <protected [true,false]>"
            )
            self._abort()

    def _require_credentials(self) -> None:
        """Prompt the user for PCF credentials"""
        # fmt: off
        form_fields = (
            MenuInput.builder()
                .field()
                    .label("Username")
                    .value(self._username)
                    .build()
                .field()
                    .label("Password")
                    .itype("password")
                    .value(self._password)
                    .build()
            .build()
        )
        # fmt: on
        result = minput(form_fields, title="Please type your Cloud Foundry credentials")
        if result:
            self._username = result.username
            self._password = result.password
        else:
            self._abort()

    def _authorize(self) -> bool:
        """Send an authorization request to PCF"""
        if not self._cf.api(self._api):
            raise CFExecutionError(f"Unable to set API: => {self._cf.last_result}")
        if not self._cf.auth(self._username, self._password):
            raise CFAuthenticationError(f"Unable to authenticate to => {self._api}")

        return True

    def _set_org(self) -> None:
        """Set the active organization"""
        if not self._org:
            sysout("%YELLOW%Checking organization...")
            orgs = self._cf.orgs()
            if not orgs:
                raise CFExecutionError(f"Unable to retrieve organizations: => {self._cf.last_result}")
            self._org = mselect(orgs, title="Please select the organization")
            if not self._org:
                self._abort()
            else:
                self._target()

    def _set_space(self) -> None:
        """Set the active space"""
        if not self._space:
            sysout("%YELLOW%Checking space...")
            if self._refresh or not (spaces := self._cache.read(f"cf-spaces-{self._org}")):
                spaces = self._cf.spaces()
                self._cache.save(f"cf-spaces-{self._org}", spaces)
            if not spaces:
                raise CFExecutionError(f"Unable to retrieve spaces: => {self._cf.last_result}")
            self._space = mselect(spaces, title="Please select a space")
            if not self._space:
                self._abort()
            else:
                self._target()

    def _choose_apps(self) -> Optional[List[CFApplication]]:
        """Choose multiple PCF apps from the available list"""
        if not self._cf_apps:
            self._cf_apps = self._get_apps()
        return mchoose(self._cf_apps, checked=False, title="Please choose the applications you want to manage")

    def _select_app(self) -> Optional[CFApplication]:
        """Select a single PCF app from the available list"""
        if not self._cf_apps:
            self._cf_apps = self._get_apps()
        return mselect(self._cf_apps, title="Please select the application you want to manage")

    def _target(self) -> None:
        """Send a target request to PCF"""
        sysout(f"%GREEN%Targeting ORG={self._org} and SPACE={self._space}...")
        if not self._cf.target(org=self._org, space=self._space):
            raise CFExecutionError(f"Unable to target ORG: {self._org} => {self._cf.last_result}")

    def _loop_actions(self) -> None:
        """Wait for the user interactions"""
        while not self._done:
            if self._org and self._space and not self._cf.is_targeted():
                self._target()
            else:
                self._set_org()
                self._set_space()

            if not self._org or not self._space or not self._cf.is_targeted():
                raise CFExecutionError(
                    f"Unable to target ORG={self._org}  SPACE={self._space} => {self._cf.last_result}"
                )

            action = mselect(CFManager.CF_ACTIONS, "Please select an action to perform")

            if not action:
                self._done = True
            else:
                if self._is_callable(action):
                    self._perform_callable(action)
                else:
                    if action.lower() == "status":
                        self._display_app_status()
                    elif action.lower() == "target":
                        self._space = self._org = self._cf_apps = None
                        self._cf.targeted = {"org": None, "space": None, "targeted": False}
                        continue

                    MenuUtils.wait_enter()

    def _display_app_status(self) -> None:
        """Display select apps status"""
        apps = self._get_apps()
        if len(apps) > 0:
            # pylint: disable=consider-using-f-string
            sysout(
                "%WHITE%{}  {}  {}  {}  {}  {}".format(
                    "Name".ljust(CFApplication.max_name_length),
                    "State".ljust(7),
                    "Instances".ljust(10),
                    "Mem".ljust(4),
                    "Disk".ljust(4),
                    "URLs",
                )
            )
            for app in apps:
                app.print_status()

    def _perform_callable(self, action):
        """Perform the selected callable action"""
        if self._allow_multiple(action.lower()):
            apps = self._choose_apps()
        else:
            app = self._select_app()
            apps = [app] if app else None
        if apps:
            for app in apps:
                self._perform(action, app=app.name, org=self._org, space=self._space)

    def _perform(self, action: str, **kwargs):
        """Perform the selected PCF action"""
        sysout(f"%GREEN%Performing {action.lower()} {str(kwargs)}...")
        method_to_call = getattr(self._cf, action.lower())
        sysout(method_to_call(**kwargs))
