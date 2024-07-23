#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib
   @package: hspylib.core.tools
      @file: fluid.py
   @created: Fri, 5 Jan 2024
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright (c) 2024, HomeSetup
"""

from functools import partial
from typing import Callable

from hspylib.core.namespace import Namespace
from hspylib.modules.eventbus.eventbus import EventBus, emit


class FluidEvent:
    """Provide a 'Fluid' event base class."""

    def __init__(self, name: str, **kwargs):
        self.name = name
        for key, val in kwargs.items():
            setattr(self, key, val)

    def __str__(self):
        return f"FluidEvent-{self.name}::({', '.join(vars(self))})"

    def emit(self, bus_name: str, event_name: str, **kwargs) -> None:
        """Wrapper to the Event's emit method."""
        ...

    def subscribe(self, cb_event_handler: Callable) -> None:
        """Wrapper to the EventBus's subscribe method."""
        ...


class FluidEventBus:
    """Provide a 'Fluid' event bus base class."""

    def __init__(self, bus_name: str, **kwargs):
        self.name = bus_name
        self.bus = EventBus.get(bus_name)
        for key, evt in kwargs.items():
            fn_emit: Callable = partial(emit, bus_name, evt.name, **vars(evt))
            fn_subscribe: Callable = partial(self.bus.subscribe, evt.name, cb_event_handler=evt.cb_event_handler)
            setattr(evt, "emit", fn_emit)
            setattr(evt, "subscribe", fn_subscribe)
        self.events: Namespace = Namespace(f"FluidEventBus::{bus_name}", True, **kwargs)

    def __str__(self):
        return f"FluidEventBus-{self.bus.name}::({self.events})"
