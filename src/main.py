#!/usr/bin/env python

import signal

from main.hspylib.core.config.app_config import AppConfigs

AppConfigs().logger().info(AppConfigs.INSTANCE)


def exit_app(sig=None, frame=None):
    print(frame or '', end='')
    print('\033[2J\033[H')
    print('Done.')
    print('')
    exit(sig)


class Main:
    def __init__(self):
        self.configs = AppConfigs.INSTANCE

    def run(self):
        pass


# Application entry point
if __name__ == "__main__":
    signal.signal(signal.SIGINT, exit_app)
    Main().run()
    exit_app(0)
