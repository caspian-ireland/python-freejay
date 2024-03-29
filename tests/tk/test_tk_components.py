from freejay.tk import tk_components
from freejay.messages import messages as mes
from unittest.mock import Mock


def test_tk_component_send():

    msg = mes.Message(
        sender=mes.Sender(source=mes.Source.PLAYER_VIEW, trigger=mes.Trigger.BUTTON),
        content=mes.Button(
            mes.PressRelease.PRESS,
            component=mes.Component.LEFT_DECK,
            element=mes.Element.PLAY_PAUSE,
        ),
    )

    root_mock = Mock()
    component_t = tk_components.TkComponent(
        tkroot=root_mock, parent=root_mock, source=mes.Source.PLAYER_VIEW
    )
    component_t.send_message(msg)

    root_mock.send_message.assert_called_once_with(msg)


def test_tk_component_button():

    expected = mes.Message(
        sender=mes.Sender(source=mes.Source.PLAYER_VIEW, trigger=mes.Trigger.BUTTON),
        content=mes.Button(
            mes.PressRelease.PRESS,
            component=mes.Component.LEFT_DECK,
            element=mes.Element.PLAY_PAUSE,
        ),
    )

    root_mock = Mock()
    component_t = tk_components.TkComponent(
        tkroot=root_mock, parent=root_mock, source=mes.Source.PLAYER_VIEW
    )
    component_t.button_send(
        component=mes.Component.LEFT_DECK,
        element=mes.Element.PLAY_PAUSE,
        press_release=mes.PressRelease.PRESS,
    )

    # Get actual message passed to mock
    # Then set dt to zero to allow comparison
    actual = root_mock.send_message.call_args.args[0]
    actual.metadata["dt"] = 0
    expected.metadata["dt"] = 0

    assert actual == expected


def test_tk_component_key():

    expected = mes.Message(
        sender=mes.Sender(source=mes.Source.MAIN_WINDOW, trigger=mes.Trigger.KEY),
        content=mes.Key(mes.PressRelease.PRESS, sym="q"),
    )
    root_mock = Mock()
    tk_event = Mock()
    tk_event.keysym = "q"

    component_t = tk_components.TkComponent(
        tkroot=root_mock, parent=root_mock, source=mes.Source.MAIN_WINDOW
    )
    component_t.key_send(press_release=mes.PressRelease.PRESS, tkevent=tk_event)

    # Get actual message passed to mock
    # Then set dt to zero to allow comparison
    actual = root_mock.send_message.call_args.args[0]
    actual.metadata["dt"] = 0
    expected.metadata["dt"] = 0

    assert actual == expected
