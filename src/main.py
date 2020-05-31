#!/usr/bin/env python

import signal


def exit_app(sig=None, frame=None):
    print(frame)
    print('\033[2J\033[H')
    print('Done.')
    print('')
    exit(sig)


# Application entry point
if __name__ == "__main__":
    signal.signal(signal.SIGINT, exit_app)
    exit_app(0)
