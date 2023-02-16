import pytest
from freejay.message_dispatcher import handler
from freejay.messages import messages as mes


@pytest.fixture
def cb_class_f():
    class CallbackClass:
        def __init__(self):
            self.return_val = None

        def do_nothing_cb(self, message: mes.Message):
            pass

        def do_something_cb(self, message: mes.Message[mes.Button]):
            self.return_val = message.content.element

    return CallbackClass()


@pytest.fixture
def handler_f(cb_class_f):
    t_handler = handler.Handler()

    t_handler.register_handler(
        cb_class_f.do_nothing_cb,
        component=mes.Component.LEFT_DECK,
        element=mes.Element.CUE,
    )

    t_handler.register_handler(
        cb_class_f.do_something_cb,
        component=mes.Component.LEFT_DECK,
        element=mes.Element.PLAY_PAUSE,
    )

    t_handler.register_handler(
        cb_class_f.do_something_cb,
        component=mes.Component.RIGHT_DECK,
        element=mes.Element.CUE,
    )

    return t_handler


def test_register_handler(cb_class_f, handler_f):

    actual = dict(handler_f.cb_dict)
    expected = {
        mes.Component.LEFT_DECK: {
            mes.Element.CUE: cb_class_f.do_nothing_cb,
            mes.Element.PLAY_PAUSE: cb_class_f.do_something_cb,
        },
        mes.Component.RIGHT_DECK: {mes.Element.CUE: cb_class_f.do_something_cb},
    }

    assert actual == expected


def test_calls_correct_cb(handler_f, cb_class_f):

    msg1 = mes.Message(
        sender=mes.Sender(source=mes.Source.PLAYER_VIEW, trigger=mes.Trigger.BUTTON),
        content=mes.Button(
            press_release=mes.PressRelease.PRESS,
            component=mes.Component.LEFT_DECK,
            element=mes.Element.CUE,
        ),
    )

    msg2 = mes.Message(
        sender=mes.Sender(source=mes.Source.PLAYER_VIEW, trigger=mes.Trigger.BUTTON),
        content=mes.Button(
            press_release=mes.PressRelease.PRESS,
            component=mes.Component.LEFT_DECK,
            element=mes.Element.PLAY_PAUSE,
        ),
    )

    msg3 = mes.Message(
        sender=mes.Sender(source=mes.Source.PLAYER_VIEW, trigger=mes.Trigger.BUTTON),
        content=mes.Button(
            press_release=mes.PressRelease.PRESS,
            component=mes.Component.RIGHT_DECK,
            element=mes.Element.CUE,
        ),
    )

    handler_f(msg1)
    assert cb_class_f.return_val is None

    handler_f(msg2)
    assert cb_class_f.return_val is mes.Element.PLAY_PAUSE

    handler_f(msg3)
    assert cb_class_f.return_val is mes.Element.CUE


def test_no_match_logs_warning(handler_f, cb_class_f, caplog):

    msg1 = mes.Message(
        sender=mes.Sender(source=mes.Source.PLAYER_VIEW, trigger=mes.Trigger.BUTTON),
        content=mes.Button(
            press_release=mes.PressRelease.PRESS,
            component=mes.Component.LEFT_DECK,
            element=mes.Element.CUE,
        ),
    )

    msg2 = mes.Message(
        sender=mes.Sender(source=mes.Source.PLAYER_VIEW, trigger=mes.Trigger.BUTTON),
        content=mes.Button(
            press_release=mes.PressRelease.PRESS,
            component=mes.Component.MIXER,
            element=mes.Element.PLAY_PAUSE,
        ),
    )

    handler_f(msg1)
    handler_f(msg2)
    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == "WARNING"
    assert "No callback registered for component" in caplog.text
