#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib
   @package: demo.other
      @file: event_bus_demo.py
   @created: Mon, 31 Oct 2022
    @author: "<B>H</B>ugo <B>S</B>aporetti <B>J</B>unior
      @site: "https://github.com/yorevs/hspylib")
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright·(c)·2024,·HSPyLib
"""
from hspylib.modules.eventbus import eventbus


@eventbus.subscribe(bus="oni-bus", events="door-open")
def door_open(ev) -> None:
    print("EVENT:", ev, "NAME:", ev.name, "KNOCKS:", ev.args.knock, "ALERT:", ev.args.alert)


@eventbus.subscribe(bus="oni-bus", events="door-close")
def door_close(ev) -> None:
    print("EVENT:", ev, "NAME:", ev.name, "KNOCKS:", ev.args.knock, "ALERT:", ev.args.alert)


class BusMonitor:

    @staticmethod
    @eventbus.subscribe(bus="oni-bus", events=["door-open", "door-close"])
    def db_open_close(ev) -> None:
        print(f"ROCKS!!!", "EVENT:", ev, "NAME:", ev.name, "KNOCKS:", ev.args.knock, "ALERT:", ev.args.alert)


if __name__ == "__main__":
    eventbus.emit("oni-bus", "door-open", knock=3, alert=False)
    eventbus.emit("oni-bus", "door-close", knock=1, alert=True)
