from time import sleep
from typing import List

from cfman.core.cf import CloudFoundry
from cfman.core.cf_application import Application
from cfman.core.cf_endpoint import Endpoint
from hspylib.core.config.app_config import AppConfigs
from hspylib.core.tools.commons import sysout, get_or_default
from hspylib.ui.cli.menu.extra.mchoose import mchoose
from hspylib.ui.cli.menu.extra.minput import MenuInput, minput
from hspylib.ui.cli.menu.extra.mselect import mselect


class CFManager(object):
    """Represents the cloud foundry manager and it's functionalities"""

    CF_ACTIONS = [
        'Start',
        'Stop',
        'Restart',
        'Restage',
        'Logs'
    ]

    @staticmethod
    def __allow_multiple__(action: str) -> bool:
        return action not in ['logout', 'target', 'logs', 'ssh']

    def __init__(self, options: dict):
        self.log = AppConfigs.INSTANCE.logger()
        self.configs = AppConfigs.INSTANCE
        self.options = options
        self.cf = CloudFoundry()
        self.api = get_or_default(self.options, 'api')
        self.username = get_or_default(self.options, 'username')
        self.password = get_or_default(self.options, 'password')
        self.org = get_or_default(self.options, 'org')
        self.space = get_or_default(self.options, 'space')
        self.apps = None
        self.done = False

    def run(self):
        if self.cf.connected:
            sysout('Already connected to CF!')
        else:
            sysout('Not connected to CF, login required...')
            if not self.api:
                self.__select_api__()
            if not self.username or not self.password:
                sleep(0.5)
                self.__require_credentials__()
            sysout(f'Logging in {self.username}@{self.api}...')
            self.__do_login__()
            sysout('Successfully logged in!')

        self.__loop_actions__()

    def exit_handler(self, signum=0, frame=None) -> None:
        """
        Handle interruptions to shutdown gracefully
        :param signum: The signal number or the exit code
        :param frame: The frame raised by the signal
        """
        if frame is not None:
            self.log.warn('Signal handler hooked signum={} frame={}'.format(signum, frame))
            exit_code = 3
        else:
            self.log.info('Exit handler called')
            exit_code = signum
        sysout('')
        exit(exit_code)

    def get_apps(self) -> List[Application]:
        apps = self.cf.apps()
        apps = list(map(Application.of, apps if apps else []))
        if not apps:
            raise Exception('Unable to retrieve applications')
        return apps

    def __select_api__(self):
        with open('{}/api_endpoints.txt'.format(self.configs.resource_dir()), 'r+') as f_hosts:
            endpoints = list(map(lambda x: Endpoint(x.split(',')), f_hosts.readlines()))
            selected = mselect(endpoints, title='Please select an endpoint')
            if not selected:
                self.exit_handler()
            self.api = selected.host

    def __require_credentials__(self):
        self.username = self.options['username'] if 'username' in self.options else None
        self.password = self.options['password'] if 'password' in self.options else None
        form_fields = MenuInput.builder() \
            .field().label('Username').kind('any').value(self.username).build() \
            .field().label('Password').kind('any').mode('password').value(self.password).build() \
            .build()
        result = minput(form_fields, title='Please type your PCF credentials')
        if result:
            self.username = result[0].value
            self.password = result[1].value
        else:
            self.exit_handler()

    def __do_login__(self) -> None:
        result = self.cf.api(self.api)
        if not result:
            raise Exception(f'Unable to set API: => {result}')
        result = self.cf.auth(self.username, self.password)
        if not result:
            raise Exception(f'Unable to authenticate: => {result}')

    def __select_org__(self) -> None:
        if not self.org:
            orgs = self.cf.orgs()
            if not orgs:
                raise Exception(f'Unable to retrieve organizations: => {str(orgs)}')
            self.org = mselect(orgs, title='Please select the organization')
        self.cf.target(org=self.org)

    def __select_space__(self) -> None:
        if not self.space:
            spaces = self.cf.spaces()
            if not spaces:
                raise Exception(f'Unable to retrieve spaces: => {str(spaces)}')
            self.space = mselect(spaces, title='Please select a space')
        self.cf.target(space=self.space)

    def __choose_apps__(self) -> None:
        apps = self.get_apps()
        self.apps = mchoose(apps, checked=False, title='Please choose the applications you want to manage')

    def __select_app__(self):
        apps = self.get_apps()
        sel_app = mselect(apps, title='Please select the application you want to manage')
        self.apps = [sel_app] if sel_app else None

    def __loop_actions__(self) -> None:

        while not self.done:
            if self.org and self.space:
                ret_status, ret_val = self.cf.target(org=self.org, space=self.space)
                self.log.info(ret_val)
            else:
                self.__select_org__()
                self.__select_space__()

            if not self.org or not self.space:
                raise Exception(f"Unable to target ORG: {self.org}  SPACE: {self.space}")

            action = mselect(CFManager.CF_ACTIONS, 'Please select an action to perform')

            if not action:
                self.done = True
            else:
                if not self.apps:
                    if self.__allow_multiple__(action.lower()):
                        self.__choose_apps__()
                    else:
                        self.__select_app__()
                if len(self.apps) > 0:
                    for app in self.apps:
                        self.__perform__(action, app=app.name, org=self.org, space=self.space)

        self.exit_handler()

    def __perform__(self, action: str, **kwargs):
        method_to_call = getattr(self.cf, action.lower())
        sysout(f'Performing {action.lower()} ...')
        result = method_to_call(**kwargs)
        sysout(result)
        sleep(0.5)
