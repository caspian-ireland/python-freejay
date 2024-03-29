import pytest
import copy
from freejay.messages import router
from freejay.messages import messages
from freejay.messages import produce_consume as prodcon


# Simple class that implements
# the consumer protocol
@pytest.fixture
def consumer_fixture():
    class ConsumerFixture(prodcon.Consumer):
        def init(self):
            self.return_val = None

        def on_message_recieved(self, message):
            return self.return_val

    return ConsumerFixture()


# Construct message for use in tests
@pytest.fixture
def message_fixture():
    msg = messages.Message(
        sender=messages.Sender(
            source=messages.Source.PLAYER_VIEW, trigger=messages.Trigger.KEY
        ),
        content=messages.Key(press_release=messages.PressRelease.PRESS, sym="q"),
        type=messages.Type.KEY,
    )
    return msg


# Construct router with the
# consumer fixture to help test
# routing conditions
@pytest.fixture
def router_fixture(consumer_fixture):

    consumer_key = copy.copy(consumer_fixture)
    consumer_key.return_val = "key"

    consumer_button = copy.copy(consumer_fixture)
    consumer_button.return_val = "button"

    message_router = router.MessageRouter()

    message_router.register_route(
        condition=lambda m: m.type == messages.Type.KEY,
        consumer=consumer_key,
    )
    message_router.register_route(
        condition=lambda m: m.type == messages.Type.BUTTON,
        consumer=consumer_button,
    )

    return message_router


# Check that routing works as expected for different conditions
@pytest.mark.parametrize(
    "msg_type,expected",
    [
        (messages.Type.BUTTON, "button"),
        (messages.Type.KEY, "key"),
        (messages.Type.DATA, None),
    ],
)
def test_router(router_fixture, message_fixture, msg_type, expected):

    message_fixture.type = msg_type

    assert router_fixture(message=message_fixture) == expected
