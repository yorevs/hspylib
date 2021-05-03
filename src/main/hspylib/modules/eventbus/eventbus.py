from typing import Callable


class EventBus:
    _buses = {}
    _subscribers = {}
    _events = []

    @staticmethod
    def get(bus_name: str):
        if bus_name in EventBus._buses:
            return EventBus._buses[bus_name]
        else:
            bus_instance = EventBus(bus_name)
            EventBus._buses[bus_name] = bus_instance
            return bus_instance

    @staticmethod
    def __create_or_get(bus_name: str, event_name: str):
        cache_key = '{}.{}'.format(bus_name, event_name)
        if cache_key in EventBus._subscribers:
            return EventBus._subscribers[cache_key]
        else:
            subscriber = {'callbacks': []}
            EventBus._subscribers[cache_key] = subscriber
            return subscriber

    def __init__(self, name: str):
        self.name = name

    def subscribe(self, event_name: str, cb_event_handler: Callable):
        subscriber = EventBus.__create_or_get(self.name, event_name)
        subscriber['callbacks'].append(cb_event_handler)

    def emit(self, event_name: str, **kwargs):
        self._events.append({'event': event_name, 'kwargs': kwargs})
        while len(self._events) > 0:
            event = self._events.pop()
            cache_key = '{}.{}'.format(self.name, event['event'])
            subscribers = self._subscribers[cache_key] if cache_key in self._subscribers else None
            if subscribers and len(subscribers['callbacks']) > 0:
                for callback in subscribers['callbacks']:
                    callback(event['kwargs'])
