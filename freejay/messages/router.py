"""Message Routing to route messages depending on some condition."""

import typing
import logging
from freejay.messages import messages
from freejay.messages import produce_consume as prodcon

logger = logging.getLogger(__name__)

# Type variable representing function that accepts a message
# and returns True/False based on some logic.
RouteCondition = typing.TypeVar(
    "RouteCondition", bound=typing.Callable[[messages.Message], bool]
)


class MessageRouter(prodcon.Consumer):
    """
    Message router to route messages based on meeting some condition.

    Routes are added using the `register_route()` method. Each route
    consists of a condition and a target consumer. The condition is configured
    as a callback function accepting a message as input and returning a boolean.
    The consumer is a target object implementing the 'Consumer' protocol.

    Note: message will be routed using the first matching condition only.
    """

    def __init__(self):
        """Construct a MessageRouter object."""
        self.routes = []

    def register_route(self, condition: RouteCondition, consumer: prodcon.Consumer):
        """Register a new route.

        Args:
            condition (RouteCondition): Callback accepting a message and returning
                a boolean. If true, message is routed to consumer.
            consumer (prodcon.Consumer): Target consumer to route message to.
        """
        self.routes.append({"condition": condition, "consumer": consumer})

    def on_message_recieved(self, message: messages.Message):
        """Check route conditions and send to target consumer.

        Args:
            message (messages.Message): Message to route
        """
        logger.debug(f"Routing message: {message}")
        for route in self.routes:
            if route["condition"](message):
                return route["consumer"](message)
