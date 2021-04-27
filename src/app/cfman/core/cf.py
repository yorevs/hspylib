import logging as log
import select
import subprocess
from time import sleep
from typing import List, Any

from hspylib.core.meta.singleton import Singleton
from hspylib.core.tools.commons import syserr


class CloudFoundry(metaclass=Singleton):
    """Cloud Foundry command line tool python wrapper"""

    def __init__(self):
        self.connected = False
        self.targeted = {'org': None, 'space': None, 'targeted': False}
        self.last_result = None

    def is_targeted(self):
        return self.targeted['org'] and self.targeted['space'] and self.targeted['targeted']

    # Before getting started:
    def connect(self) -> bool:
        """Attempt to connect to CloudFoundry"""
        if not self.connected:
            self.connected = "FAILED" not in self.__exec__('orgs')
        return self.connected

    def api(self, api: str) -> bool:
        """Set or view target api url"""
        params = ['api', api]
        return "FAILED" not in self.__exec__(*params)

    def auth(self, username: str, password: str) -> bool:
        """Authorize a CloudFoundry user"""
        params = ['auth', username, password]
        return "FAILED" not in self.__exec__(*params)

    def target(self, **kwargs) -> dict:
        """Set or view the targeted org or space"""
        params = ['target']
        if 'org' in kwargs and kwargs['org']:
            params.append('-o')
            params.append(kwargs['org'])
            self.targeted['org'] = kwargs['org']
        if 'space' in kwargs and kwargs['space']:
            params.append('-s')
            params.append(kwargs['space'])
            self.targeted['space'] = kwargs['space']
        self.targeted['targeted'] = "FAILED" not in self.__exec__(*params)

        return self.targeted

    # Space management
    def spaces(self) -> List[str]:
        """List all spaces in an org"""
        all_spaces = self.__exec__('spaces').split('\n')
        return all_spaces[3:] if all_spaces and "FAILED" not in all_spaces else None

    # Org management
    def orgs(self) -> List[str]:
        """List all orgs"""
        all_orgs = self.__exec__('orgs').split('\n')
        return all_orgs[3:] if all_orgs and "FAILED" not in all_orgs else None

    # Application lifecycle:
    def apps(self) -> List[str]:
        """List all apps in the target space"""
        all_apps = self.__exec__('apps').split('\n')
        return all_apps[4:] if all_apps and "FAILED" not in all_apps else None

    def start(self, **kwargs) -> str:
        """Start an app"""
        return self.__exec__('start', kwargs['app'])

    def stop(self, **kwargs) -> str:
        """Stop an app"""
        return self.__exec__('stop', kwargs['app'])

    def restart(self, **kwargs) -> str:
        """Stop all instances of the app, then start them again. This causes downtime."""
        return self.__exec__('restart', kwargs['app'])

    def restage(self, **kwargs) -> str:
        """Recreate the app's executable artifact using the latest pushed app files and the latest environment
        (variables, service bindings, buildpack, stack, etc.). This action will cause app downtime."""
        return self.__exec__('restage', kwargs['app'])

    def logs(self, **kwargs):
        """Tail or show recent logs for an app"""
        self.__poll__('logs', kwargs['app'])

    # Subprocess helper
    def __exec__(self, *cmd_args) -> Any:
        try:
            args = list(cmd_args)
            args.insert(0, 'cf')
            log.info('Executing PCF command: {}'.format(' '.join(args)))
            result = subprocess.run(args, capture_output=True, text=True).stdout
            log.debug('Success! Execution result: {}'.format(result))
            result = str(result).strip() if result else None
        except subprocess.CalledProcessError as err:
            log.debug(f'Failed => {str(err)}')
            syserr(str(err))
            result = None
        self.last_result = result

        return result

    # Subprocess helper
    def __poll__(self, *cmd_args):
        try:
            args = list(cmd_args)
            args.insert(0, 'cf')
            log.info('Polling PCF command: {}'.format(cmd_args))
            file = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            process = select.poll()
            process.register(file.stdout)
            line = None
            while "FAILED" != line:
                if process.poll(1):
                    line = file.stdout.readline().decode("utf-8").strip()
                    print(line)
                sleep(1)
        except Exception as err:
            log.debug(f'Failed => {str(err)}')
            syserr(str(err))
