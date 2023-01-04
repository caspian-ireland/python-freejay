import typing
from freejay import messages
from freejay import produce_consume as prodcon


RouteCondition = typing.TypeVar(
    "RouteCondition", bound=typing.Callable[[messages.Message], bool]
)


class MessageRouter(prodcon.Consumer):
    def __init__(self):
        self.routes = []

    def register_route(self, condition: RouteCondition, consumer: prodcon.Consumer):
        self.routes.append({"condition": condition, "consumer": consumer})

    def on_message_recieved(self, message: messages.Message):
        for route in self.routes:
            if route["condition"](message):
                return route["consumer"](message)


# def make_message_router(queue, debouncer):

#     message_router = MessageRouter()
#     message_router.register_route(
#         condition=lambda m: m
#         in (
#             messages.Type.BUTTON,
#             messages.Type.SET_VALUE,
#             messages.Type.VALUE_BUTTON,
#         ),
#         consumer=queue,
#     )
#     message_router.register_route(
#         condition=lambda m: m in (messages.Type.KEY), consumer=debouncer
#     )

#     return message_router
