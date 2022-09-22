#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: main.modules.eventbus
      @file: eventbus.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

from typing import Any, Callable, List

from hspylib.core.tools.commons import syserr
from hspylib.modules.eventbus.event import Event


class EventBus:
    """TODO"""

    _buses = {}
    _subscribers = {}
    _events: List[Event] = []

    @classmethod
    def get(cls, bus_name: str) -> Any:
        """TODO"""
        if bus_name in cls._buses:
            return cls._buses[bus_name]
        bus_instance = EventBus(bus_name)
        cls._buses[bus_name] = bus_instance
        return bus_instance

    @classmethod
    def _get_subscriber(cls, bus_name: str, event_name: str) -> Any:
        """TODO"""
        cache_key = f'{bus_name}.{event_name}'
        if cache_key in cls._subscribers:
            return cls._subscribers[cache_key]
        subscriber = {'callbacks': []}
        cls._subscribers[cache_key] = subscriber
        return subscriber

    def __init__(self, name: str):
        self.name = name

    def subscribe(self, event_name: str, cb_event_handler: Callable) -> None:
        """TODO"""
        subscriber = self._get_subscriber(self.name, event_name)
        subscriber['callbacks'].append(cb_event_handler)

    def emit(self, event_name: str, **kwargs) -> None:
        """TODO"""
        self._events.append(Event(event_name, **kwargs))
        while len(self._events) > 0:
            event = self._events.pop()
            cache_key = f"{self.name}.{event.name}"
            subscribers = self._subscribers[cache_key] if cache_key in self._subscribers else None
            if subscribers and len(subscribers['callbacks']) > 0:
                for callback in subscribers['callbacks']:
                    try:
                        callback(event)
                    except TypeError as err:
                        syserr(f"{self.__class__.__name__}::emit Callback invocation failed - {str(err)}")
