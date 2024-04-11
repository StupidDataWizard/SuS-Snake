class EventHandler:
    registered_events = {}

    # bound method via decorator to an event
    @staticmethod
    def register(event_type, key=None):
        def decorator(func):
            EventHandler.registered_events.setdefault(event_type, []).append([func, key])
        return decorator

    # call method if registered event is fired
    @staticmethod
    def notify(event):
        observers = EventHandler.registered_events[event.type] if event.type in EventHandler.registered_events else []
        for observer in observers:
            # handle event by key
            if observer[1] is not None:
                if event.unicode != observer[1]:
                    continue
            observer[0](event)

