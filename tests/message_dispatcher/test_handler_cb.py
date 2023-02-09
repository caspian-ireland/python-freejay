import pytest
from unittest import mock
from freejay.message_dispatcher import handler_cb
from freejay.messages import messages as mes


# Construct message for use in tests
@pytest.fixture
def message_f():
    msg = mes.Message(
        sender=mes.Sender(source=mes.Source.PLAYER_UI, trigger=mes.Trigger.KEY),
        content=mes.Key(press_release=mes.PressRelease.PRESS, sym="q"),
        type=mes.Type.KEY,
    )
    return msg


def test_make_button_cb_returns_callable():
    test_cb = handler_cb.make_button_cb(mock.Mock(), mock.Mock())
    assert callable(test_cb)


def test_make_data_cb_returns_callable():
    test_cb = handler_cb.make_data_cb(mock.Mock())
    assert callable(test_cb)


def test_make_button_cb_cb_calls_correct():
    mocker1 = mock.Mock()
    mocker2 = mock.Mock()
    test_cb = handler_cb.make_button_cb(mocker1, mocker2)

    msg = mes.Message(
        sender=mes.Sender(source=mes.Source.PLAYER_UI, trigger=mes.Trigger.BUTTON),
        content=mes.Button(
            press_release=mes.PressRelease.PRESS,
            component=mes.Component.LEFT_DECK,
            element=mes.Element.CUE,
            data={"value": 1},
        ),
    )

    # Button press calls mocker1
    test_cb(msg)
    mocker1.assert_called_once_with(value=1)
    mocker2.assert_not_called()

    # button release calls mocker2
    msg.content.press_release = mes.PressRelease.RELEASE
    test_cb(msg)
    mocker1.assert_called_once()
    mocker2.assert_called_once()


def test_make_button_cb_cb_no_release():
    mocker = mock.Mock()
    test_cb = handler_cb.make_button_cb(mocker)

    msg = mes.Message(
        sender=mes.Sender(source=mes.Source.PLAYER_UI, trigger=mes.Trigger.BUTTON),
        content=mes.Button(
            press_release=mes.PressRelease.PRESS,
            component=mes.Component.LEFT_DECK,
            element=mes.Element.CUE,
        ),
    )

    # Button press calls mocker
    test_cb(msg)
    mocker.assert_called_once()

    # Button release does nothing
    msg.content.press_release = mes.PressRelease.RELEASE
    test_cb(msg)
    mocker.assert_called_once()


def test_make_button_cb_cb_calls_correct_no_data():
    mocker1 = mock.Mock()
    mocker2 = mock.Mock()
    test_cb = handler_cb.make_button_cb(mocker1, mocker2)

    msg = mes.Message(
        sender=mes.Sender(source=mes.Source.PLAYER_UI, trigger=mes.Trigger.BUTTON),
        content=mes.Button(
            press_release=mes.PressRelease.PRESS,
            component=mes.Component.LEFT_DECK,
            element=mes.Element.CUE,
        ),
    )

    # Button press calls mocker1
    test_cb(msg)
    mocker1.assert_called_once_with()
    mocker2.assert_not_called()

    # button release calls mocker2
    msg.content.press_release = mes.PressRelease.RELEASE
    test_cb(msg)
    mocker1.assert_called_once()
    mocker2.assert_called_once_with()
