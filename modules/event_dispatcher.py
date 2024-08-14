class EventDispatcher:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EventDispatcher, cls).__new__(cls)
            cls._instance._subscribers = {}
        return cls._instance

    def subscribe(self, event_type, callback):
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)

    def publish(self, event_type, *args, **kwargs):
        if event_type in self._subscribers:
            for callback in self._subscribers[event_type]:
                callback(*args, **kwargs)
