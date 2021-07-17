#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   hspylib.app.cfman.src.main.core
      @file: cf_manager.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""
import sys
from time import sleep
from typing import List, Optional

from cfman.src.main.core.cf import CloudFoundry
from cfman.src.main.core.cf_application import CFApplication
from cfman.src.main.core.cf_endpoint import CFEndpoint
from cfman.src.main.exception.exceptions import CFConnectionError, CFExecutionError, CFAuthenticationError
from hspylib.core.config.app_config import AppConfigs
from hspylib.core.enums.http_code import HttpCode
from hspylib.core.tools.commons import get_by_key_or_default, syserr, sysout
from hspylib.modules.cli.tui.extra.mchoose import mchoose
from hspylib.modules.cli.tui.extra.minput.minput import MenuInput, minput
from hspylib.modules.cli.tui.extra.mselect import mselect
from hspylib.modules.cli.tui.menu.menu_utils import MenuUtils
from hspylib.modules.fetch.fetch import head


class CFManager:
    """Represents the cloud foundry manager application and it's functionalities"""

    CF_ACTIONS = [
        'Logs',
        'Restart',
        'Restage',
        'Status',
        'Start',
        'Stop',
        'Target',
    ]

    @staticmethod
    def _abort():
        sys.exit(1)

    @staticmethod
    def _allow_multiple(action: str) -> bool:
        """Checks whether the action allows multiple apps selection or not"""
        return action.lower() not in ['logs', 'target']

    @staticmethod
    def _is_callable(action: str) -> bool:
        """Checks whether the action is callable or not"""
        return action.lower() not in ['status', 'target']

    def __init__(self, options: dict):
        self.configs = AppConfigs.INSTANCE
        self.options = options
        self.cf = CloudFoundry()
        self.api = get_by_key_or_default(self.options, 'api')
        self.username = get_by_key_or_default(self.options, 'username')
        self.password = get_by_key_or_default(self.options, 'password')
        self.org = get_by_key_or_default(self.options, 'org')
        self.space = get_by_key_or_default(self.options, 'space')
        self.apps = None
        self.done = False

    def run(self) -> None:
        """Execute main cf manager routines"""
        sysout('%GREEN%Checking CloudFoundry authorization...')
        if self.cf.connect():
            sysout('%GREEN%Already authorized to CloudFoundry!')
        else:
            authorized = False
            sysout('%YELLOW%Not authorized to CloudFoundry, login required...')
            while not authorized:
                if not self.api:
                    sleep(1)
                    self._select_endpoint()
                if not self.username or not self.password:
                    sleep(1)
                    self._require_credentials()
                sysout(f'%GREEN%Authorizing {self.username}@{self.api}...')
                authorized = self._authorize()
                if not authorized:
                    self.password = None
                    sleep(1)
            sysout('%GREEN%Successfully authorized!')

        self._loop_actions()

    def _get_apps(self, refresh: bool = False) -> List[CFApplication]:
        """Retrieve all cf applications under the target/org"""
        if refresh or not self.apps:
            sysout(f'%GREEN%Retrieving {self.space} applications ...')
            apps = self.cf.apps()
            apps = list(map(CFApplication.of, apps if apps else []))
            if not apps:
                if "OK" not in self.cf.last_result:
                    raise CFExecutionError(f'Unable to retrieve applications: => {self.cf.last_result}')
                sysout('%YELLOW%No apps found')
            self.apps = apps

        return self.apps

    def _select_endpoint(self) -> None:
        """Select the PCF endpoint to connect to"""
        filename = f'{self.configs.resource_dir()}/api_endpoints.txt'
        with open(filename, 'w+') as f_hosts:
            endpoints = list(map(lambda x: CFEndpoint(x.split(',')), f_hosts.readlines()))
            if len(endpoints) > 0:
                selected = mselect(endpoints, title='Please select an endpoint')
                if not selected:
                    self._abort()
                sysout(f"%GREEN%Connecting to endpoint: {selected}...")
                try:
                    response = head(selected.host)
                    if response.status_code and HttpCode.OK:
                        self.api = selected.host
                    else:
                        syserr(f'Failed to connect to API ({response.status_code}): {selected}')
                        self._abort()
                except Exception as err:
                    raise CFConnectionError(f'Failed to connect to API => {selected.host}') from err
            else:
                syserr(f"No endpoint yet configured. Please create the file {filename} "
                       f"with at least one endpoint configured and try again.")
                self._abort()

    def _require_credentials(self) -> None:
        """Promp the user for PCF credentials"""
        self.username = self.options['username'] if 'username' in self.options else self.username
        self.password = self.options['password'] if 'password' in self.options else self.password
        form_fields = MenuInput.builder() \
            .field().label('Username').value(self.username).build() \
            .field().label('Password').itype('password').value(self.password).build() \
            .build()
        result = minput(form_fields, title='Please type your Cloud Foundry credentials')
        if result:
            self.username = result.username
            self.password = result.password
        else:
            self._abort()

    def _authorize(self) -> bool:
        """Send an authorization request to PCF"""
        if not self.cf.api(self.api):
            raise CFExecutionError(f'Unable to set API: => {self.cf.last_result}')
        if not self.cf.auth(self.username, self.password):
            raise CFAuthenticationError(f'Unable to authenticate to => {self.api}')

        return True

    def _set_org(self) -> None:
        """Set the active organization"""
        if not self.org:
            sysout('%YELLOW%Checking organization...')
            orgs = self.cf.orgs()
            if not orgs:
                raise CFExecutionError(f'Unable to retrieve organizations: => {self.cf.last_result}')
            self.org = mselect(orgs, title='Please select the organization')
            if not self.org:
                self._abort()
            else:
                self._target()

    def _set_space(self) -> None:
        """Set the active space"""
        if not self.space:
            sysout('%YELLOW%Checking space...')
            spaces = self.cf.spaces()
            if not spaces:
                raise CFExecutionError(f'Unable to retrieve spaces: => {self.cf.last_result}')
            self.space = mselect(spaces, title='Please select a space')
            if not self.space:
                self._abort()
            else:
                self._target()

    def _choose_apps(self) -> Optional[List[CFApplication]]:
        """Choose multiple PCF apps from the available list"""
        if not self.apps:
            self.apps = self._get_apps()
        return mchoose(self.apps, checked=False, title='Please choose the applications you want to manage')

    def _select_app(self) -> Optional[CFApplication]:
        """Select a single PCF app from the available list"""
        if not self.apps:
            self.apps = self._get_apps()
        return mselect(self.apps, title='Please select the application you want to manage')

    def _target(self) -> None:
        """Send a target request to PCF"""
        sysout(f"%GREEN%Targeting ORG={self.org} and SPACE={self.space}...")
        if not self.cf.target(org=self.org, space=self.space):
            raise CFExecutionError(f"Unable to target ORG: {self.org} => {self.cf.last_result}")

    def _loop_actions(self) -> None:
        """Wait for the user interactions"""
        while not self.done:
            if self.org and self.space and not self.cf.is_targeted():
                self._target()
            else:
                self._set_org()
                self._set_space()

            if not self.org or not self.space or not self.cf.is_targeted():
                raise CFExecutionError(f"Unable to target ORG={self.org}  SPACE={self.space} => {self.cf.last_result}")

            action = mselect(CFManager.CF_ACTIONS, 'Please select an action to perform')

            if not action:
                self.done = True
            else:
                if self._is_callable(action):
                    self._perform_callable(action)
                else:
                    if action.lower() == 'status':
                        self._display_app_status()
                    elif action.lower() == 'target':
                        self.space = self.org = self.apps = None
                        self.cf.targeted = {'org': None, 'space': None, 'targeted': False}
                        continue

                    MenuUtils.wait_enter()

    def _display_app_status(self):
        """Display select apps status"""
        apps = self._get_apps(refresh=True)
        if len(apps) > 0:
            sysout("{}  {}  {}  {}  {}  {}".format(
                'Name'.ljust(CFApplication.max_name_length),
                'State'.ljust(7), 'Inst'.ljust(5), 'Mem'.ljust(4),
                'Disk'.ljust(4), 'URLs',
            ))
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
                self._perform(action, app=app.name, org=self.org, space=self.space)

    def _perform(self, action: str, **kwargs):
        """Perform the selected PCF action"""
        sysout(f'%GREEN%Performing {action.lower()} {str(kwargs)}...')
        method_to_call = getattr(self.cf, action.lower())
        sysout(method_to_call(**kwargs))
