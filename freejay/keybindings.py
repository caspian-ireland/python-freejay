from freejay import messages as mes

keybindings = {
    "q": {
        "name": "cue-left",
        "content": mes.Button,
        "type": mes.Type.BUTTON,
        "component": mes.Component.LEFT_DECK,
        "element": mes.Element.CUE,
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


class KeyMapper:
    def __init__(self, keybindings):
        self.keybindings = keybindings

    def map(self, message: mes.Message):
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

        return newmessage
