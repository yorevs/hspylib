import select
import subprocess
from time import sleep
from typing import List, Any

from hspylib.core.config.app_config import AppConfigs
from hspylib.core.meta.singleton import Singleton


class CloudFoundry(metaclass=Singleton):
    """TODO"""

    def __init__(self):
        self.log = AppConfigs.INSTANCE.logger()
        self.connected = "FAILED" not in self.__exec__('orgs')

    # Before getting started:
    def api(self, api: str) -> bool:
        params = ['api', api]
        return "FAILED" not in self.__exec__(*params)

    def auth(self, username: str, password: str):
        params = ['auth', username, password]
        return "FAILED" not in self.__exec__(*params)

    def target(self, **kwargs) -> bool:
        """Set or view the targeted org or space"""
        params = ['target']
        if 'org' in kwargs:
            params.append('-o')
            params.append(kwargs['org'])
        if 'space' in kwargs:
            params.append('-s')
            params.append(kwargs['space'])

        return "FAILED" not in self.__exec__(*params)

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

    def logs(self, **kwargs) -> str:
        """Tail or show recent logs for an app"""
        return self.__poll__('logs', kwargs['app'])

    def ssh(self, **kwargs) -> str:
        """SSH to an application container instance"""
        return self.__poll__('ssh', kwargs['app'])

    # Subprocess helper
    def __exec__(self, *cmd_args) -> Any:
        args = list(cmd_args)
        args.insert(0, 'cf')
        self.log.info('Executing PCF command: {}'.format(' '.join(args)))
        result = subprocess.run(args, capture_output=True, text=True).stdout
        self.log.debug('Execution result: {}'.format(result))
        return str(result).strip() if result else None

    # Subprocess helper
    def __poll__(self, *cmd_args) -> Any:
        args = list(cmd_args)
        args.insert(0, 'cf')
        self.log.info('Polling PCF command: {}'.format(cmd_args))
        file = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process = select.poll()
        process.register(file.stdout)
        line = None
        while "FAILED" != line:
            if process.poll(1):
                line = file.stdout.readline().decode("utf-8").strip()
                print(line)
            sleep(1)
