from _ctypes_test import func


class EventBus:
    __buses = {}
    __subscribers = {}
    __events = []

    @staticmethod
    def get(bus_name: str):
        if bus_name in EventBus.__buses:
            return EventBus.__buses[bus_name]
        else:
            bus_instance = EventBus(bus_name)
            EventBus.__buses[bus_name] = bus_instance
            return bus_instance

    @staticmethod
    def __create_or_get(bus_name: str, event_name: str):
        cache_key = '{}.{}'.format(bus_name, event_name)
        if cache_key in EventBus.__subscribers:
            return EventBus.__subscribers[cache_key]
        else:
            subscriber = {'callbacks': []}
            EventBus.__subscribers[cache_key] = subscriber
            return subscriber

    def __init__(self, name: str):
        self.name = name

    def subscribe(self, event_name: str, callback: func):
        subscriber = EventBus.__create_or_get(self.name, event_name)
        subscriber['callbacks'].append(callback)

    def emit(self, event_name: str, **kwargs):
        self.__events.append({'event': event_name, 'kwargs': kwargs})
        while len(self.__events) > 0:
            event = self.__events.pop()
            cache_key = '{}.{}'.format(self.name, event['event'])
            subscribers = self.__subscribers[cache_key] if cache_key in self.__subscribers else None
            if subscribers and len(subscribers['callbacks']) > 0:
                for callback in subscribers['callbacks']:
                    callback(event['kwargs'])
