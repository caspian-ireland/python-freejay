"""
Functions to generate callback functions for the message handler.
"""

import typing
from freejay.messages import messages as mes

# from freejay import djplayer


def make_button_cb(
    press_cb: typing.Callable[..., None],
    release_cb: typing.Optional[typing.Callable[..., None]] = None,
) -> typing.Callable[[mes.Message[mes.Button]], None]:
    """Make Button callback.

    Helper function to make a callback function for messages with
    Button content. If message represents a button press, the press callback is
    called, and visa versa for release callback if provided. The 'content.data'
    dictionary is unpacked and passed as keyword args to the callback function.

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
        factories.make_button_cb() for more details.

        Args:
            message (mes.Message[mes.Button]): Message with Button content.
        """
        if message.content.press_release == mes.PressRelease.PRESS:
            press_cb(**message.content.data)
        elif (
            message.content.press_release == mes.PressRelease.RELEASE
            and release_cb is not None
        ):
            release_cb()

    return callback


def make_data_cb(
    cb: typing.Callable[..., None]
) -> typing.Callable[[mes.Message[mes.Data]], None]:
    """Make Data callback.

    Helper function to make a callback function for messages with
    Data content. The message 'content.data' attribute is unpacked and passed as
    keyword arguments to the callback functions.

    Args:
        cb (typing.Callable[..., None]): Callback function.

    Returns:
        typing.Callable[[mes.Message[mes.Data]], None]: Callback function.
    """

    def callback(message: mes.Message[mes.Data]) -> None:
        """Message[Data] callback function.

        The messages 'content.data' attribute is unpacked and passed as
        keyword arguments.

        Args:
            message (mes.Message[mes.Data]): Message with 'Data' content.
        """
        cb(**message.content.data)

    return callback
