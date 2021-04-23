from time import sleep
from typing import List

from cfman.core.cf import CloudFoundry
from cfman.core.cf_application import CFApplication
from cfman.core.cf_endpoint import CFEndpoint
from hspylib.core.config.app_config import AppConfigs
from hspylib.core.enum.http_code import HttpCode
from hspylib.core.tools.commons import sysout, get_by_key_or_default
from hspylib.modules.fetch.fetch import head
from hspylib.ui.cli.menu.extra.mchoose import mchoose
from hspylib.ui.cli.menu.extra.minput import MenuInput, minput
from hspylib.ui.cli.menu.extra.mselect import mselect
from hspylib.ui.cli.menu.menu_utils import MenuUtils


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
    def __allow_multiple__(action: str) -> bool:
        return action.lower() not in ['logs', 'target']

    @staticmethod
    def __is_callable__(action: str) -> bool:
        return action.lower() not in ['status', 'target']

    def __init__(self, options: dict):
        self.log = AppConfigs.INSTANCE.logger()
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
            sysout('%YELLOW%Not authorized to CloudFoundry, login required...%NC%')
            if not self.api:
                sleep(0.5)
                self.__select_endpoint__()
            if not self.username or not self.password:
                sleep(0.5)
                self.__require_credentials__()
            sysout(f'%GREEN%Authorizing {self.username}@{self.api}...%NC%')
            self.__authorize__()
            sysout('%GREEN%Successfully authorized!%NC%')

        self.__loop_actions__()

    def __get_apps__(self) -> List[CFApplication]:
        sysout(f'%GREEN%Retrieving {self.space} applications ...%NC%')
        apps = self.cf.apps()
        apps = list(map(CFApplication.of, apps if apps else []))
        if not apps:
            if "OK" not in self.cf.last_result:
                raise Exception(f'Unable to retrieve applications: => {self.cf.last_result}')
            else:
                sysout('%YELLOW%No apps found%NC%')
        return apps or []

    def __select_endpoint__(self):
        with open('{}/api_endpoints.txt'.format(self.configs.resource_dir()), 'r+') as f_hosts:
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
                self.configs.logger().error(f'Failed to connect to API => {err}')
                MenuUtils.print_error('Failed to connect to API => ', selected.host)
                exit(0)

        MenuUtils.wait_enter()

    def __require_credentials__(self):
        self.username = self.options['username'] if 'username' in self.options else None
        self.password = self.options['password'] if 'password' in self.options else None
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

    def __authorize__(self) -> None:
        result = self.cf.api(self.api)
        if not result:
            raise Exception(f'Unable to set API: => {self.cf.last_result}')
        result = self.cf.auth(self.username, self.password)
        if not result:
            raise Exception(f'Unable to authenticate: => {self.cf.last_result}')

    def __set_org__(self) -> None:
        if not self.org:
            orgs = self.cf.orgs()
            if not orgs:
                raise Exception(f'Unable to retrieve organizations: => {self.cf.last_result}')
            self.org = mselect(orgs, title='Please select the organization')

    def __set_space__(self) -> None:
        if not self.space:
            spaces = self.cf.spaces()
            if not spaces:
                raise Exception(f'Unable to retrieve spaces: => {self.cf.last_result}')
            self.space = mselect(spaces, title='Please select a space')

    def __choose_apps__(self) -> None:
        apps = self.__get_apps__()
        self.apps = mchoose(apps, checked=False, title='Please choose the applications you want to manage')

    def __select_app__(self):
        apps = self.__get_apps__()
        sel_app = mselect(apps, title='Please select the application you want to manage')
        self.apps = [sel_app] if sel_app else None

    def __do_target__(self):
        sysout(f"%GREEN%Targeting ORG = {self.org} and SPACE = {self.space}...%NC%")
        if not self.cf.target(org=self.org, space=self.space):
            raise Exception(f"Unable to target ORG: {self.org} => {self.cf.last_result}")

    def __loop_actions__(self) -> None:

        while not self.done:
            if self.org and self.space and not self.cf.targeted:
                self.__do_target__()
            else:
                sysout('%YELLOW%Selecting organization...%NC%')
                self.__set_org__()
                sysout('%YELLOW%Selecting space...%NC%')
                self.__set_space__()
                if not self.cf.targeted:
                    self.__do_target__()

            if not self.org or not self.space or not self.cf.targeted:
                raise Exception(f"Unable to target ORG: {self.org}  SPACE: {self.space} => {self.cf.last_result}")

            action = mselect(CFManager.CF_ACTIONS, 'Please select an action to perform')

            if not action:
                self.done = True
            else:
                if self.__is_callable__(action):
                    if self.__allow_multiple__(action.lower()):
                        self.__choose_apps__()
                    else:
                        self.__select_app__()
                    if len(self.apps) > 0:
                        for app in self.apps:
                            self.__perform__(action, app=app.name, org=self.org, space=self.space)
                else:
                    if "status" == action.lower():
                        apps = self.__get_apps__()
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
                        self.cf.targeted = False
                        continue

                    MenuUtils.wait_enter()

    def __perform__(self, action: str, **kwargs):
        sysout(f'%GREEN%Performing {action.lower()} {str(kwargs)}...%NC%')
        method_to_call = getattr(self.cf, action.lower())
        sysout(method_to_call(**kwargs))
