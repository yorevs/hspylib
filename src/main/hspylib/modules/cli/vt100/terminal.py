import logging as log
import select
import subprocess
from abc import ABC
from time import sleep

from hspylib.core.tools.commons import syserr


class Terminal(ABC):
    
    @staticmethod
    def shell_exec(*cmd_args, **kwargs) -> str:
        try:
            log.info(f"Executing shell command: {' '.join(*cmd_args)}")
            result = subprocess.run(*cmd_args, **kwargs).stdout
            log.debug(f"Execution result: {result}")
            result = str(result).strip() if result else None
        except subprocess.CalledProcessError as err:
            log.debug(f'Failed => {str(err)}')
            syserr(str(err))
            result = None
        
        return result
    
    @staticmethod
    def shell_poll(*cmd_args, **kwargs) -> None:
        try:
            log.info(f"Polling shell command: {' '.join(*cmd_args)}")
            with(subprocess.Popen(*cmd_args, **kwargs)) as file:
                process = select.poll()
                process.register(file.stdout)
                line = None
                while line != 'FAILED':
                    if process.poll(1):
                        line = file.stdout.readline().decode("utf-8").strip()
                        print(line)
                    sleep(1)
        except InterruptedError:
            pass
        except Exception as err:
            log.debug(f'Failed => {str(err)}')
            syserr(str(err))
