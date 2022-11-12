#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: hspylib
   @package: hspylib.demo.other
      @file: event_bus_demo.py
   @created: Mon, 31 Oct 2022
    @author: "<B>H</B>ugo <B>S</B>aporetti <B>J</B>unior")"
      @site: "https://github.com/yorevs/hspylib")
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
from hspylib.modules.eventbus import eventbus


@eventbus.subscribe(bus='oni-bus', event='door-open')
def door_open(ev) -> None:
    print('EVENT:', ev, 'NAME:', ev.name, 'KNOCKS:', ev.args.knock, 'ALERT:', ev.args.alert)


@eventbus.subscribe(bus='oni-bus', event='door-close')
def door_close(ev) -> None:
    print('EVENT:', ev, 'NAME:', ev.name, 'KNOCKS:', ev.args.knock, 'ALERT:', ev.args.alert)


if __name__ == '__main__':
    eventbus.emit('oni-bus', 'door-open', knock=3, alert=False)
    eventbus.emit('oni-bus', 'door-close', knock=1, alert=True)
