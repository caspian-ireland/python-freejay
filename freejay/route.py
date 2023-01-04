import typing
from freejay import messages
from freejay import produce_consume as prodcon


# Condition function
# Listener

RouteCondition = typing.TypeVar(
    "RouteCondition", bound=typing.Callable[[messages.Message], bool]
)


class MessageRouter(prodcon.Consumer):
    def __init__(self):
        self.routes = []

    def register_route(self, condition: RouteCondition, consumer: prodcon.Consumer):
        self.routes.append({"condition": condition, "consumer": consumer})

    def on_message_recieved(self, message: messages.Message):
        for condition, consumer in self.routes:
            if condition(message):
                consumer(message)
                break


def make_message_router(queue, debouncer):

    message_router = MessageRouter()
    message_router.register_route(
        condition=lambda m: m
        in (
            messages.Type.BUTTON,
            messages.Type.SET_VALUE,
            messages.Type.VALUE_BUTTON,
        ),
        consumer=queue,
    )
    message_router.register_route(
        condition=lambda m: m in (messages.Type.KEY), consumer=debouncer
    )

    return message_router


# class MessageRouter:
#     def __init__(self):
#         pass

#     @property
#     def routetable(self):
#         return self.__routetable

#     @routetable.setter
#     def routetable(self, val):
#         event_route = {v["events"]: k for k, v in val.items()}
#         event_route = {e: v for k, v in event_route.items() for e in k}
#         route_callback = {k: v["callback"] for k, v in val.items()}
#         self.event_route = event_route
#         self.route_callback = route_callback
#         self.__routetable = val

#     def route(self, message: messages.Message):
#         route_name = self.event_route[message.type]
#         route_callback = self.route_callback[route_name]
#         route_callback(message)


# def make_queue_route_cb(q):
#     def queue_route_cb(message):
#         q.put(message)

#     return queue_route_cb


# def make_debouncer_route_cb(keybindings, debouncer):
#     def debouncer_route_cb(event):
#         allowed_keys = keybindings.keys()
#         if event.payload.key in allowed_keys:
#             if event.payload.press_release == events.PressRelease.Press:
#                 debouncer.key_press(event)
#             elif event.payload.press_release == events.PressRelease.Release:
#                 debouncer.key_release(event)

#     return debouncer_route_cb


# def make_debouncer_key_cb(key_event_mapper, event_router):
#     def debouncer_key_cb(event):

#         event_type_map = {
#             events.EventType.KeyPressRaw: events.EventType.KeyPress,
#             events.EventType.KeyReleaseRaw: events.EventType.KeyRelease,
#         }
#         event.type = event_type_map[event.type]
#         event = key_event_mapper.map(event)
#         event_router.route(event)

#     return debouncer_key_cb


# def make_routetable(keybindings, debouncer, q):

#     routetable = {
#         "queue": {
#             "callback": make_queue_route_cb(q=q),
#             "types": (
#                 messages.Type.BUTTON,
#                 messages.Type.SET_VALUE,
#                 messages.Type.VALUE_BUTTON,
#             ),
#         },
#         "debouncer": {
#             "callback": make_debouncer_route_cb(
#                 keybindings=keybindings, debouncer=debouncer
#             ),
#             "types": messages.Type.KEY,
#         },
#     }

#     return routetable
