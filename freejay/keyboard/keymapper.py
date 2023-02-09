"""
Keymapper implements keybindings, mapping key event messages into action messages.
"""

import logging
from freejay.messages import messages as mes
from freejay.messages import produce_consume as prodcon

logger = logging.getLogger(__name__)

# TODO: Better way of storing this
keybindings = {
    "q": {
        "name": "cue-left",
        "content_type": mes.Button,
        "content": {
            "component": mes.Component.LEFT_DECK,
            "element": mes.Element.CUE,
        },
    },
    "w": {
        "name": "play_pause-left",
        "content_type": mes.Button,
        "content": {
            "component": mes.Component.LEFT_DECK,
            "element": mes.Element.PLAY_PAUSE,
        },
    },
    "e": {
        "name": "nudge-slow-left",
        "content_type": mes.Button,
        "content": {
            "component": mes.Component.LEFT_DECK,
            "element": mes.Element.NUDGE,
            "data": {"value": -0.1},
        },
    },
    "r": {
        "name": "nudge-fast-left",
        "content_type": mes.Button,
        "content": {
            "component": mes.Component.LEFT_DECK,
            "element": mes.Element.NUDGE,
            "data": {"value": 0.1},
        },
    },
    "p": {
        "name": "stop-left",
        "content_type": mes.Button,
        "content": {
            "component": mes.Component.LEFT_DECK,
            "element": mes.Element.STOP,
        },
    },
}


class KeyMapper(prodcon.Consumer, prodcon.Producer):
    """
    Map key events using keybindings.

    KeyMapper listens for key messages and
    uses keybindings to translate into relevant
    messages that can be sent to another consumer.
    """

    def __init__(self, keybindings: dict):
        """Construct KeyMapper.

        Args:
            keybindings (dict): keybindings
        """
        self.keybindings = keybindings

    def map(self, message: mes.Message):
        """Map key message using keybindings.

        Args:
            message (mes.Message): Message with content type 'Key' to be mapped.

        Raises:
            TypeError: Message with type != 'Key'.
        """
        if isinstance(message.content, mes.Key):
            try:
                keybinding = self.keybindings[message.content.sym]
                newmessage = mes.Message(
                    sender=message.sender,
                    content=keybinding["content_type"](
                        press_release=message.content.press_release,
                        **keybinding["content"],
                    ),
                )

                self.send_message(newmessage)
            except KeyError as e:
                logger.info(f"No keybinding registered for {e}")

        else:
            raise TypeError("KeyMapper only handles Messages with content type 'Key'.")

    def on_message_recieved(self, message: mes.Message):
        """Call `map` method.

        Implement consumer protocol. On message recieved call `map` method.

        Args:
            message (mes.Message): Message with content type 'Key' to be mapped.
        """
        self.map(message)
