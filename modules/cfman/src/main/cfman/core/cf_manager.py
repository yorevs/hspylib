#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib-CFMan
   @package: cfman.core
      @file: cf_manager.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
import sys
from functools import partial
from time import sleep
from typing import List, Optional, Tuple

import requests
from clitt.core.tui.mchoose import mchoose
from clitt.core.tui.menu.tui_menu_utils import TUIMenuUtils
from clitt.core.tui.minput.minput import MenuInput, minput
from clitt.core.tui.mselect import mselect
from hspylib.core.enums.http_code import HttpCode
from hspylib.core.preconditions import check_state
from hspylib.core.tools.commons import syserr, sysout
from hspylib.modules.cache.ttl_cache import TTLCache
from hspylib.modules.cli.vt100.vt_utils import clear_screen
from hspylib.modules.fetch.fetch import head
from retry import retry

from cfman.core.cf import CloudFoundry
from cfman.core.cf_application import CFApplication
from cfman.core.cf_blue_green_checker import CFBlueGreenChecker
from cfman.core.cf_endpoint import CFEndpoint
from cfman.exception.exceptions import CFAuthenticationError, CFConnectionError, CFExecutionError


class CFManager:
    """Responsible for the CloudFoundry application functionalities.
    """

    CFMAN_ACTIONS = [
        "Information", "Target", "Logs",
        "Start", "Stop", "Restart", "Restage",
        "Status", "Blue-Green-Check"
    ]

    @staticmethod
    def _abort():
        """Abort the execution and exit.
        """
        sys.exit(1)

    @staticmethod
    def _allow_multiple(action: str) -> bool:
        """Whether the action allows multiple application selection or not.
        :param action the action to check
        """
        return action.lower() in [
            "start", "stop", "restart", "restage"
        ]

    @staticmethod
    def _is_callable(action: str) -> bool:
        """Whether the provided action is callable or not.
        :param action the action to check
        """
        return action.lower() in [
            "logs", "start", "stop", "restart", "restage"
        ]

    @staticmethod
    def required_states(action: str) -> str | Tuple[str, str]:
        """Return the required application statue of the provided action
        :param action the action to check
        """
        match action:
            case "start":
                return "stopped"
            case "logs" | "stop" | "restart":
                return "started"
            case _:
                return "started", "stopped"

    def __init__(
        self,
        api: str,
        org: str,
        space: str,
        username: str,
        password: str,
        no_cache: str,
        cf_endpoints: str):

        self._cf = CloudFoundry()
        self._cache = TTLCache()
        self._api = api
        self._org = org
        self._space = space
        self._username = username
        self._password = password
        self._no_cache = no_cache or False
        self._cf_endpoints_file = cf_endpoints
        self._cf_apps = None
        self._done = False

    def __str__(self) -> str:
        return (
            f"%EOL%%GREEN%"
            f"{'-=' * 40} %EOL%"
            f"{self._api} %EOL%"
            f"{'--' * 40} %EOL%"
            f"{'USER:':>6} {self._username}%EOL%"
            f"{'ORG:':>6} {self._org}%EOL%"
            f"{'SPACE:':>6} {self._space}%EOL%"
            f"{'-=' * 40}")

    def __repr__(self) -> str:
        return str(self)

    @property
    def apps(self) -> List[CFApplication]:
        return self._get_apps() or []

    def run(self) -> None:
        """Run the main cf manager application flow.
        """
        sysout("%BLUE%Checking CloudFoundry authorization...")
        if self._cf.is_logged():
            self._api = self._cf.api()
            target = self._cf.target()
            self._username, self._org, self._space = target.user, target.org, target.space
            sysout("%YELLOW%Already authorized to CloudFoundry!")
        else:
            authorized = False
            sysout("%YELLOW%Unauthorized to CloudFoundry, login required...")
            sleep(2)
            while not authorized:
                if not self._api:
                    self._select_endpoint()
                if not self._username or not self._password:
                    self._prompt_credentials()
                sysout(f"%BLUE%Authorizing {self._username}@{self._api}...")
                authorized = self._authorize()
                if not authorized:
                    self._password = None
                    syserr("Not authorized !")
                    self._abort()
            sysout("%GREEN%Successfully authorized!")
        sysout(f"%HOM%%ED0%%WHITE%--- Target information ---%EOL%{self}")
        TUIMenuUtils.wait_keystroke()
        self._loop_actions()

    @retry(exceptions=CFConnectionError, tries=3, delay=2, backoff=3, max_delay=30)
    def _select_endpoint(self) -> None:
        """Select the PCF endpoint to connect to.
        """
        try:
            with open(self._cf_endpoints_file, "r", encoding="utf-8") as f_hosts:
                endpoints = list(map(lambda l: CFEndpoint(*l.strip().split(",")), f_hosts.readlines()))
                if len(endpoints) > 0:
                    selected = mselect(endpoints, title="Please select an endpoint")
                    if not selected:
                        self._abort()
                    sysout(f"%BLUE%Connecting to endpoint: {selected}...")
                    try:
                        response = head(selected.host)
                        if response.status_code and HttpCode.OK:
                            self._api = selected.host
                        else:
                            syserr(
                                CFConnectionError(
                                    f"Failed to contact CF API %EOL%"
                                    f"  Status: ({response.status_code}): {selected}"))
                            self._abort()
                    except requests.exceptions.ConnectionError as err:
                        syserr(
                            CFConnectionError(
                                f"Failed to connect to CloudFoundry API%EOL%"
                                f"  Host: '{selected.host}'%EOL%"
                                f"  => {err.__class__.__name__}"))
                        self._abort()
                else:
                    syserr(
                        CFExecutionError(
                            f"No endpoint yet configured. Please create the file \"{self._cf_endpoints_file}\" "
                            f"with at least one endpoint and try again!"))
                    self._abort()
        except (IndexError, FileNotFoundError) as err:
            syserr(
                CFExecutionError(
                    f"Endpoint file \"{self._cf_endpoints_file}\" is invalid: %EOL%"
                    f"  => {str(err)}! %EOL%"
                    f"Make sure it exists contains the following: %EOL%"
                    f"<alias>,<cf_api_url>,<protected [true|false]>%EOL%"))
            self._abort()

    def _prompt_credentials(self) -> None:
        """Prompt the user for his PCF credentials.
        """
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
        """Send an authorization request to PCF.
        """
        if not self._cf.api(self._api):
            raise CFExecutionError(f"Unable to set API: => {self._cf.last_output}")
        if not self._cf.auth(self._username, self._password):
            raise CFAuthenticationError(f"Unable to authenticate to => {self._api}")

        return True

    def _set_org(self) -> None:
        """Set the active PCF organization.
        """
        if not self._org:
            sysout(f"%BLUE%Retrieving all organizations from api: \"{self._api}\"...")
            if not (orgs := self._cf.orgs()):
                raise CFExecutionError(f"Unable to retrieve organizations: => {self._cf.last_output}")
            self._org = mselect(orgs, title="Please select the PCF organization")
            if not self._org:
                self._abort()
            else:
                self._target()

    def _set_space(self) -> None:
        """Set the active PCF space.
        """
        if not self._space:
            if self._no_cache or not (spaces := self._cache.read(f"cf-spaces-{self._org}")):
                sysout(f"%BLUE%Retrieving all spaces from org: \"{self._org}\"...")
                spaces = self._cf.spaces()
                self._cache.save(f"cf-spaces-{self._org}", spaces)
            if not spaces:
                raise CFExecutionError(f"Unable to retrieve org={self._org} spaces: => {self._cf.last_output}")
            self._space = mselect(spaces, title="Please select the PCF space")
            if not self._space:
                self._abort()
            else:
                self._target()

    def _get_apps(self) -> List[CFApplication]:
        """Retrieve all cf applications under the targeted org-space.
        """
        if self._no_cache or not (apps := self._cache.read(f"cf-apps-{self._space}")):
            sysout(f"%BLUE%Retrieving applications from space: \"{self._space}\"...")
            apps = self._cf.apps()
            sysout(f"%GREEN%Found {len(apps)} apps in space: \"{self._space}\"")
            self._cache.save(f"cf-apps-{self._space}", apps)
        if not apps:
            if "OK" not in self._cf.last_output:
                raise CFExecutionError(f"Unable to retrieve applications: => {self._cf.last_output}")
            syserr(f"%YELLOW%No applications found for space: \"{self._space}\"")
        cf_apps = list(map(CFApplication.of, apps if apps else []))
        self._cf_apps = cf_apps

        return self._cf_apps

    def _choose_apps(self, required_states: str | Tuple[str, str]) -> Optional[List[CFApplication]]:
        """Choose multiple PCF apps from the available list.
        :param required_states used to filter the apps to choose by the application state.
        """
        self._cf_apps = list(filter(lambda app: app.state.lower() in required_states, self.apps))
        if not self._cf_apps:
            return None
        return mchoose(self._cf_apps, checked=False, title="Please choose the applications you want to manage")

    def _select_app(self, required_states: str | Tuple[str, str]) -> Optional[CFApplication]:
        """Select a single PCF app from the available list.
        :param required_states used to filter the apps to choose by the application state.
        """
        self._cf_apps = list(filter(lambda app: app.state.lower() in required_states, self.apps))
        if not self._cf_apps:
            return None
        return mselect(self._cf_apps, title="Please select the application you want to manage")

    def _target(self) -> None:
        """Attempt to target to a PCF org-space.
        """
        if not self._cf.target(user=self._username, org=self._org, space=self._space):
            raise CFExecutionError(f"Unable to target ORG: {self._org} => {self._cf.last_output}")
        sleep(1)

    def _loop_actions(self) -> None:
        """Wait for the user interactions.
        """
        while self._assert_target():
            if not (action := mselect(CFManager.CFMAN_ACTIONS, "Please select an action to perform")):
                self._done = True
                return
            if self._is_callable(action):
                self._perform_callable(action)
            else:
                match action.lower():
                    case "status":
                        self._display_app_status()
                    case "target":
                        self._space = self._org = self._cf_apps = None
                        self._cf.clear_target()
                        continue
                    case "blue-green-check":
                        self._blue_green_check()
                    case "information":
                        sysout(f"%HOM%%ED0%%WHITE%--- Target information ---%EOL%{self}")

                TUIMenuUtils.wait_keystroke()

    def _assert_target(self) -> bool:
        if not self._org:
            self._set_org()
        if not self._space:
            self._set_space()
        if not self._cf.is_targeted():
            self._target()
        if not self._org or not self._space or not self._cf.is_targeted():
            raise CFExecutionError(
                f"Unable to target ORG={self._org}  SPACE={self._space} => {self._cf.last_output}"
            )
        return not self._done

    def _display_app_status(self) -> None:
        """Display all PCF space-application statuses.
        """
        apps = self.apps

        if len(apps) > 0:
            clear_screen()
            # fmt: off
            sysout(
                f"%BLUE%Listing '{self._org}::{self._space}' applications ...%EOL%%WHITE%"
                f"{'-=' * 60 + '%EOL%'}"
                f"{'Name':{CFApplication.max_name_length + 2}}"
                f"{'State':<9}{'Instances':<12}{'Mem':<6}{'Disk':<6}Routes%EOL%")
            # fmt: on
            list(map(CFApplication.print_status, apps))
            sysout('-=' * 60 + '%EOL%')

    def _blue_green_check(self) -> None:
        """Display all PCF space-application blue/green check.
        """
        if len(self.apps) > 0:
            clear_screen()
            sysout(f"%BLUE%Checking blue/green deployments ...%EOL%")
            CFBlueGreenChecker.check(self._org, self._space, self.apps)

    def _perform_callable(self, action: str) -> None:
        """Wrapper of the _perform method.
        :param action the action to perform.
        """
        act = action.lower()
        if self._allow_multiple(act):
            apps = self._choose_apps(self.required_states(act))
        else:
            app = self._select_app(self.required_states(act))
            apps = [app] if app else None
        if apps:
            perform = partial(self._perform, action=act, org=self._org, space=self._space)
            list(map(lambda a: perform(app=a.name), apps))

    def _perform(self, action: str, **kwargs) -> None:
        """Perform the selected PCF action.
        Kwargs:
              org (str): the PCF organization name.
            space (str): the PCF space name.
        :param kwargs arbitrary PCF action arguments.
        :param action the action to perform.
        """
        sysout(f"%BLUE%Performing {action} {str(kwargs)}...")
        action_method = getattr(self._cf, action)
        check_state(callable(action_method))
        sysout(action_method(**kwargs))
