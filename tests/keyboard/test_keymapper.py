import pytest
from freejay.messages import messages as mes
from freejay.messages import produce_consume as prodcon
from freejay.keyboard import keymapper


# Simple class that implements
# the consumer protocol
@pytest.fixture
def consumer_f():
    class ConsumerFixture(prodcon.Consumer):
        def init(self):
            self.message = None

        def on_message_recieved(self, message):
            self.message = message

    return ConsumerFixture()


# Construct message for use in tests
@pytest.fixture
def message_f():
    msg = mes.Message(
        sender=mes.Sender(source=mes.Source.PLAYER_VIEW, trigger=mes.Trigger.KEY),
        content=mes.Key(press_release=mes.PressRelease.PRESS, sym="q"),
        type=mes.Type.KEY,
    )
    return msg


@pytest.fixture
def keybindings_f():
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
    return keybindings


@pytest.fixture
def key_mapper_f(keybindings_f):
    key_mapper = keymapper.KeyMapper(keybindings=keybindings_f)
    return key_mapper


def test_key_mapper(key_mapper_f, message_f, consumer_f):
    consumer_f.listen(key_mapper_f)
    key_mapper_f(message_f)
    mapped_message = consumer_f.message
    assert mapped_message.content.element == mes.Element.CUE
