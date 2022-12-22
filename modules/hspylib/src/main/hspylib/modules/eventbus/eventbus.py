#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: hspylib.modules.eventbus
      @file: eventbus.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

from typing import Any, Callable, Dict, List

from hspylib.core.exception.exceptions import HSBaseException
from hspylib.core.preconditions import check_argument
from hspylib.modules.eventbus.event import Event

EVENT_CALLBACK = Callable[[Event], None]


def subscribe(**kwargs) -> Callable:
    """Method decorator to subscribe to a given bus event."""

    def subscribe_closure(func) -> None:
        check_argument(
            func.__code__.co_argcount >= 1, "Subscriber callbacks require at least one parameter.")
        missing = next((p for p in ["bus", "event"] if p not in kwargs), None)
        check_argument(missing is None, f"Missing required parameter: '{missing}: str'.")
        EventBus.get(str(kwargs["bus"])).subscribe(str(kwargs["event"]), func)

    return subscribe_closure


def emit(bus_name: str, event_name: str, **kwargs) -> None:
    """Emit an event to the specified bus."""
    EventBus.get(bus_name).emit(event_name, **kwargs)


class EventBus:
    """Provide an eventbus pattern for events and subscribers."""

    _buses: Dict[str, Any] = {}
    _subscribers: Dict[str, Any] = {}
    _events: List[Event] = []

    @classmethod
    def get(cls, bus_name: str) -> "EventBus":
        """Return the bus instance referred to the specified bus name."""
        if bus_name in cls._buses:
            return cls._buses[bus_name]
        bus_instance = EventBus(bus_name)
        cls._buses[bus_name] = bus_instance
        return bus_instance

    @classmethod
    def _get_subscriber(cls, bus_name: str, event_name: str) -> Any:
        """Return the subscriber of the referred bus name and event name."""
        cache_key = f"{bus_name}.{event_name}"
        if cache_key in cls._subscribers:
            return cls._subscribers[cache_key]
        subscriber = {"callbacks": []}
        cls._subscribers[cache_key] = subscriber
        return subscriber

    def __init__(self, name: str):
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    def subscribe(self, event_name: str, cb_event_handler: EVENT_CALLBACK) -> None:
        """Subscribe to the specified event bus."""
        subscriber = self._get_subscriber(self.name, event_name)
        subscriber["callbacks"].append(cb_event_handler)

    def emit(self, event_name: str, **kwargs) -> None:
        """Emit an event to this bus."""
        self._events.append(Event(event_name, **kwargs))
        while len(self._events) > 0:
            event = self._events.pop()
            cache_key = f"{self.name}.{event.name}"
            subscribers = self._subscribers[cache_key] if cache_key in self._subscribers else None
            if subscribers and len(subscribers["callbacks"]) > 0:
                for callback in subscribers["callbacks"]:
                    try:
                        callback(event)
                    except Exception as err:
                        raise HSBaseException(
                            f"{self.__class__.__name__}::emit Callback invocation failed - {str(err)}"
                        ) from err
