from freejay import events


class EventRouter:
    def __init__(self):
        pass

    @property
    def routetable(self):
        return self.__routetable

    @routetable.setter
    def routetable(self, val):
        event_route = {v["events"]: k for k, v in val.items()}
        event_route = {e: v for k, v in event_route.items() for e in k}
        route_callback = {k: v["callback"] for k, v in val.items()}
        self.event_route = event_route
        self.route_callback = route_callback
        self.__routetable = val

    def route(self, event: events.Event):
        route_name = self.event_route[event.type]
        route_callback = self.route_callback[route_name]
        route_callback(event)


def make_queue_route_cb(q):
    def queue_route_cb(event):
        q.put(event)

    return queue_route_cb


def make_debouncer_route_cb(keybindings, debouncer):
    def debouncer_route_cb(event):
        allowed_keys = keybindings.keys()
        if event.payload.key in allowed_keys:
            if event.payload.press_release == events.PressRelease.Press:
                debouncer.key_press(event)
            elif event.payload.press_release == events.PressRelease.Release:
                debouncer.key_release(event)

    return debouncer_route_cb


def make_debouncer_key_cb(key_event_mapper, event_router):
    def debouncer_key_cb(event):

        event_type_map = {
            events.EventType.KeyPressRaw: events.EventType.KeyPress,
            events.EventType.KeyReleaseRaw: events.EventType.KeyRelease,
        }
        event.type = event_type_map[event.type]
        event = key_event_mapper.map(event)
        event_router.route(event)

    return debouncer_key_cb


def make_routetable(keybindings, debouncer, q):

    routetable = {
        "queue": {
            "callback": make_queue_route_cb(q=q),
            "events": (
                events.EventType.ButtonPress,
                events.EventType.ButtonRelease,
                events.EventType.KeyPress,
                events.EventType.KeyRelease,
            ),
        },
        "debouncer": {
            "callback": make_debouncer_route_cb(
                keybindings=keybindings, debouncer=debouncer
            ),
            "events": (
                events.EventType.KeyPressRaw,
                events.EventType.KeyReleaseRaw,
            ),
        },
    }

    return routetable
