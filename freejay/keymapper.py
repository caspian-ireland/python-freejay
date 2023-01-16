"""
Keymapper implements keybindings, mapping key event messages into action messages.
"""

from freejay import messages as mes
from freejay import produce_consume as prodcon

# TODO: Better way of storing this
keybindings = {
    "q": {
        "name": "cue-left",
        "content_type": mes.Button,
        "type": mes.Type.BUTTON,
        "content": {
            "component": mes.Component.LEFT_DECK,
            "element": mes.Element.CUE,
        },
    },
    "w": {
        "name": "play_pause-left",
        "content_type": mes.Button,
        "type": mes.Type.BUTTON,
        "content": {
            "component": mes.Component.LEFT_DECK,
            "element": mes.Element.PLAY_PAUSE,
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
            keybinding = self.keybindings[message.content.sym]
        else:
            raise TypeError("KeyMapper only handles Messages with content type 'Key'.")
        newmessage = mes.Message(
            sender=message.sender,
            type=keybinding["type"],
            content=keybinding["content_type"](
                press_release=message.content.press_release,
                **keybinding["content"],
            ),
        )

        self.send_message(newmessage)

    def on_message_recieved(self, message: mes.Message):
        """Call `map` method.

        Implement consumer protocol. On message recieved call `map` method.

        Args:
            message (mes.Message): Message with content type 'Key' to be mapped.
        """
        self.map(message)
