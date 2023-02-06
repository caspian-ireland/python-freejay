"""
Functions to generate callback functions for the message handler.
"""

import typing
from freejay.messages import messages as mes

# from freejay import djplayer


def make_button_cb(
    press_cb: typing.Callable[[], None],
    release_cb: typing.Optional[typing.Callable[[], None]] = None,
) -> typing.Callable[[mes.Message[mes.Button]], None]:
    """Make Button callback.

    Helper function to make a callback function for messages with
    Button content. If message represents a button press, the press callback is
    called, and visa versa for release callback if provided.

    Args:
        press_cb (typing.Callable[[], None]): Callback on button press
        release_cb (typing.Optional[typing.Callable[[], None]], optional): Callback on
            button release. Defaults to None.

    Returns:
        typing.Callable[[mes.Message[mes.Button]], None]: Callback function.
    """

    def callback(message: mes.Message[mes.Button]) -> None:
        """Button callback function.

        The press_release attribute is accessed from an incoming message
        and a press callback or release callback is called. See
        handler_cb.make_button_cb() for more details.

        Args:
            message (mes.Message[mes.Button]): Message with Button content.
        """
        if message.content.press_release == mes.PressRelease.PRESS:
            press_cb()
        elif (
            message.content.press_release == mes.PressRelease.RELEASE
            and release_cb is not None
        ):
            release_cb()

    return callback


def make_value_button_cb(
    press_cb: typing.Callable[..., None],
    release_cb: typing.Optional[typing.Callable[..., None]] = None,
) -> typing.Callable[[mes.Message[mes.ValueButton]], None]:
    """Make ValueButton callback.

    Helper function to make a callback function for messages with
    ValueButton content. If message represents a button press, the press callback is
    called, and visa versa for release callback if provided. The 'content.value'
    attribute is passed to the 'value' argument of the callback functions.

    Args:
        press_cb (typing.Callable[..., None]): Callback on button press. Must
        have a 'value' parameter.
        release_cb (typing.Optional[typing.Callable[..., None]], optional): Callback on
            button release. Must have a 'value' parameter. Defaults to None.

    Returns:
        typing.Callable[[mes.Message[mes.ValueButton]], None]: Callback function.
    """

    def callback(message: mes.Message[mes.ValueButton]) -> None:
        """Value Button callback function.

        The press_release and value attributes are accessed from an incoming message
        and a press callback or release callback is called on the value argument. See
        handler_cb.make_value_button_cb() for more details.

        Args:
            message (mes.Message[mes.ValueButton]): Message with ValueButton content.
        """
        if message.content.press_release == mes.PressRelease.PRESS:
            press_cb(value=message.content.value)
        elif (
            message.content.press_release == mes.PressRelease.RELEASE
            and release_cb is not None
        ):
            release_cb(value=message.content.value)

    return callback


def make_set_value_cb(
    cb: typing.Callable[..., None]
) -> typing.Callable[[mes.Message[mes.SetValue]], None]:
    """Make SetValue callback.

    Helper function to make a callback function for messages with
    SetValue content. The message 'content.value' attribute is passed to the
    'value' argument of the callback functions.

    Args:
        cb (typing.Callable[..., None]): Callback SetValue. Must
        have a 'value' parameter.

    Returns:
        typing.Callable[[mes.Message[mes.SetValue]], None]: Callback function.
    """

    def callback(message: mes.Message[mes.SetValue]) -> None:
        """Set Value callback function.

        The messages 'content.value' attribute is passed to the 'value parameter'. See
        handler_cb.make_set_value_cb() for more details.

        Args:
            message (mes.Message[mes.SetValue]): Message with SetValue content.
        """
        cb(value=message.content.value)

    return callback
