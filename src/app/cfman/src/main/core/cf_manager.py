import logging as log
from time import sleep
from typing import List

from cfman.src.main.core.cf import CloudFoundry
from cfman.src.main.core.cf_application import CFApplication
from cfman.src.main.core.cf_endpoint import CFEndpoint
from hspylib.core.config.app_config import AppConfigs
from hspylib.core.enum.http_code import HttpCode
from hspylib.core.tools.commons import sysout, get_by_key_or_default, syserr
from hspylib.modules.fetch.fetch import head
from hspylib.modules.cli.menu.extra.mchoose import mchoose
from hspylib.modules.cli.menu.extra.minput import MenuInput, minput
from hspylib.modules.cli.menu.extra.mselect import mselect
from hspylib.modules.cli.menu.menu_utils import MenuUtils


class CFManager(object):
    """Represents the cloud foundry manager and it's functionalities"""

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
    def _allow_multiple(action: str) -> bool:
        return action.lower() not in ['logs', 'target']

    @staticmethod
    def _is_callable(action: str) -> bool:
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

    def run(self):
        sysout('%GREEN%Checking CloudFoundry authorization...%NC%')
        if self.cf.connect():
            sysout('%GREEN%Already authorized to CloudFoundry!%NC%')
        else:
            authorized = False
            sysout('%YELLOW%Not authorized to CloudFoundry, login required...%NC%')
            while not authorized:
                if not self.api:
                    sleep(1)
                    self._select_endpoint()
                if not self.username or not self.password:
                    sleep(1)
                    self._require_credentials()
                sysout(f'%GREEN%Authorizing {self.username}@{self.api}...%NC%')
                authorized = self.__authorize__()
                if not authorized:
                    self.password = None
                    sleep(1)
            sysout('%GREEN%Successfully authorized!%NC%')

        self._loop_actions()

    def _get_apps(self, refresh: bool = False) -> List[CFApplication]:
        if refresh or not self.apps:
            sysout(f'%GREEN%Retrieving {self.space} applications ...%NC%')
            apps = self.cf.apps()
            apps = list(map(CFApplication.of, apps if apps else []))
            if not apps:
                if "OK" not in self.cf.last_result:
                    raise Exception(f'Unable to retrieve applications: => {self.cf.last_result}')
                else:
                    sysout('%YELLOW%No apps found%NC%')
            self.apps = apps

        return self.apps

    def _select_endpoint(self):
        with open(f'{self.configs.resource_dir()}/api_endpoints.txt', 'r+') as f_hosts:
            endpoints = list(map(lambda x: CFEndpoint(x.split(',')), f_hosts.readlines()))
            selected = mselect(endpoints, title='Please select an endpoint')
            if not selected:
                exit(0)
            sysout(f'%GREEN%Connecting to endpoint: {selected}...%NC%')
            try:
                response = head(selected.host)
                if response.status_code and HttpCode.OK:
                    self.api = selected.host
                else:
                    raise Exception(f'Failed to connect to API ({response.status_code}): {selected}')
            except Exception as err:
                log.error(f'Failed to connect to API => {err}')
                syserr(f'Failed to connect to API => {selected.host}')
                exit(0)

    def _require_credentials(self):
        self.username = self.options['username'] if 'username' in self.options else self.username
        self.password = self.options['password'] if 'password' in self.options else self.password
        form_fields = MenuInput.builder() \
            .field().label('Username').kind('any').value(self.username).build() \
            .field().label('Password').kind('any').mode('password').value(self.password).build() \
            .build()
        result = minput(form_fields, title='Please type your Cloud Foundry credentials')
        if result:
            self.username = result[0].value
            self.password = result[1].value
        else:
            exit(0)

    def _authorize(self) -> bool:
        if not self.cf.api(self.api):
            raise Exception(f'Unable to set API: => {self.cf.last_result}')
        if not self.cf.auth(self.username, self.password):
            syserr(f'Unable to authenticate to => {self.api}')
            return False

        return True

    def _set_org(self) -> None:
        if not self.org:
            sysout('%YELLOW%Checking organization...%NC%')
            orgs = self.cf.orgs()
            if not orgs:
                raise Exception(f'Unable to retrieve organizations: => {self.cf.last_result}')
            self.org = mselect(orgs, title='Please select the organization')
            if not self.org:
                exit(1)
            else:
                self._do_target()

    def _set_space(self) -> None:
        if not self.space:
            sysout('%YELLOW%Checking space...%NC%')
            spaces = self.cf.spaces()
            if not spaces:
                raise Exception(f'Unable to retrieve spaces: => {self.cf.last_result}')
            self.space = mselect(spaces, title='Please select a space')
            if not self.space:
                exit(1)
            else:
                self._do_target()

    def _choose_apps(self) -> List[CFApplication]:
        if not self.apps:
            self.apps = self._get_apps()
        return mchoose(self.apps, checked=False, title='Please choose the applications you want to manage')

    def _select_app(self) -> CFApplication:
        if not self.apps:
            self.apps = self._get_apps()
        return mselect(self.apps, title='Please select the application you want to manage')

    def _do_target(self):
        sysout(f"%GREEN%Targeting ORG = {self.org} and SPACE = {self.space}...%NC%")
        if not self.cf.target(org=self.org, space=self.space):
            raise Exception(f"Unable to target ORG: {self.org} => {self.cf.last_result}")

    def _loop_actions(self) -> None:

        while not self.done:
            if self.org and self.space and not self.cf.is_targeted():
                self._do_target()
            else:
                self._set_org()
                self._set_space()

            if not self.org or not self.space or not self.cf.is_targeted():
                raise Exception(f"Unable to target ORG: {self.org}  SPACE: {self.space} => {self.cf.last_result}")

            action = mselect(CFManager.CF_ACTIONS, 'Please select an action to perform')

            if not action:
                self.done = True
            else:
                if self._is_callable(action):
                    if self._allow_multiple(action.lower()):
                        apps = self._choose_apps()
                    else:
                        apps = self._select_app()
                    if len(apps) > 0:
                        for app in apps:
                            self._perform(action, app=app.name, org=self.org, space=self.space)
                else:
                    if "status" == action.lower():
                        apps = self._get_apps(refresh=True)
                        if len(apps) > 0:
                            sysout("{}  {}  {}  {}  {}  {}".format(
                                'Name'.ljust(CFApplication.__max_name_length__),
                                'State'.ljust(7),
                                'Inst'.ljust(5),
                                'Mem'.ljust(4),
                                'Disk'.ljust(4),
                                'URLs',
                            ))
                            for app in apps:
                                app.print()
                    elif "target" == action.lower():
                        self.space = None
                        self.org = None
                        self.cf.targeted = {'org': None, 'space': None, 'targeted': False}
                        continue

                    MenuUtils.wait_enter()

    def _perform(self, action: str, **kwargs):
        sysout(f'%GREEN%Performing {action.lower()} {str(kwargs)}...%NC%')
        method_to_call = getattr(self.cf, action.lower())
        sysout(method_to_call(**kwargs))
