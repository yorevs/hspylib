#!/usr/bin/env python3
import signal

from hspylib.core.config.app_config import AppConfigs
from hspylib.core.meta.singleton import Singleton


class Main(metaclass=Singleton):
    def __init__(self):
        self.configs = AppConfigs()
        self.configs.logger().info(self.configs)

    @staticmethod
    def run():
        with open("welcome.txt") as fh:
            print(fh.read(), end='')
        with open("main/.version") as fh:
            print("Version " + fh.read())

    @staticmethod
    def exit_app(sig=None, frame=None):
        print(frame or '', end='')
        print('%ED2%%HOM%')
        exit(sig)


# Application entry point
if __name__ == "__main__":
    signal.signal(signal.SIGINT, Main.exit_app)
    Main().run()
    Main.exit_app(0)
