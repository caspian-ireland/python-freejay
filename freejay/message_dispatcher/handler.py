"""
Message Handling.

The Handler class can register callback functions that are assigned to specific types
of messages. When a matching message is recieved, the message is passed to the
appropriate callback function.
"""

import typing
import logging
import collections
from freejay.messages import messages as mes


logger = logging.getLogger(__name__)


class InfiniteDict(collections.defaultdict):
    """Infinitely recursing default dictionary."""

    def __init__(self):
        """Construct InfiniteDict."""
        collections.defaultdict.__init__(self, self.__class__)


class Handler:
    """
    Message Handler.

    Callback functions can be registered for combinations of message Component and
    Elements using the `register_handler()` method.

    The `handle()` method will try to match a message to a registered callback. If
    successful the message is passed to the callback function. A `__call__()` method
    wrapping `handle()` is included for convenience.
    """

    def __init__(self):
        """Construct Handler."""
        self.cb_dict = InfiniteDict()

    def register_handler(
        self,
        callback: typing.Callable[[mes.Message], None],
        component: mes.Component,
        element: mes.Element,
    ):
        """Register a callback function.

        Args:
            callback (typing.Callable[[Message], None]): Callback function accepting
                a Message object.
            component (Component): A message Component used to lookup the callback.
            element (Element): A message Element used to lookup the callback.
        """
        self.cb_dict[component][element] = callback

    def handle(
        self,
        message: typing.Union[
            mes.Message[mes.Button],
            mes.Message[mes.ValueButton],
            mes.Message[mes.SetValue],
        ],
    ):
        """Handle a message.

        handle will try to find a registered callback using the message component
        and element. If found the message is passed to the callback function.

        Note: Currently only supports messages with content type 'Button', 'ValueButton'
        or 'SetValue'.

        Args:
            message (Message): A message to be handled.
        """
        # search for correct callback
        try:
            self.cb_dict[message.content.component][message.content.element](message)
        except (KeyError, TypeError):
            logger.warning(
                f"No callback registered for component {str(message.content.component)}"
                f"and element {message.content.element}"
            )

    def __call__(
        self,
        message: typing.Union[
            mes.Message[mes.Button],
            mes.Message[mes.ValueButton],
            mes.Message[mes.SetValue],
        ],
    ):
        """
        Handle a message. Wraps the `handle()` method for convenience.

        Args:
            message (Message): A message to be handled.
        """
        self.handle(message)


# Extendible Version DRAFT ###

# class Handler:
#     def __init__(self):
#         self.cb_dict = InfiniteDict()
#         self.types = {
#             mes.Type.BUTTON: {
#                 "register": self.register_button,
#                 "handle": self.handle_button,
#             },
#             mes.Type.VALUE_BUTTON: {
#                 "register": self.register_value_button,
#                 "handle": self.handle_value_button,
#             },
#             mes.Type.SET_VALUE: {
#                 "register": self.register_set_value,
#                 "handle": self.handle_set_value,
#             },
#         }

#     def register_handler(self, type, callback, **kwargs):
#         self.types[type]["register"](callback, **kwargs)

#     def handle(self, message: mes.Message):
#         # search for correct callback
#         self.types[mes.Type.BUTTON]["handle"](message)

#     def register_button(self, callback, component, element):

#         self.cb_dict[mes.Type.BUTTON][component][element] = callback

#     def register_value_button(self, callback, component, element):

#         self.cb_dict[mes.Type.VALUE_BUTTON][component][element] = callback

#     def register_set_value(self, callback, component):

#         self.cb_dict[mes.Type.SET_VALUE][component] = callback

#     def handle_button(self, message: mes.Message[mes.Button]):
#         self.cb_dict[message.type][message.content.component][message.content.element](
#             message
#         )
