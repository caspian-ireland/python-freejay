"""Mixer callback functions."""

import typing
from freejay.message_dispatcher import handler
from freejay.messages import messages as mes
from freejay.player.mixer import Mixer


def make_crossfader_callback(
    mixer: Mixer,
) -> typing.Callable[[mes.Message[mes.Data]], None]:
    """Make a crossfader callback.

    Returned function is a closure that has access to the mixer instance. If called
    on a message, the mixers crossfader position is set to the value in the recieved
    message.

    Args:
        mixer (Mixer): mixer Model to call.

    Returns:
        typing.Callable[[mes.Message[mes.Data]], None]: Callback function.
    """

    def callback(message: mes.Message[mes.Data]):
        """Crossfader callback.

        Args:
            message (mes.Message[mes.Data]): Message with crossfader position.
        """
        mixer.crossfader.position = message.content.data["position"]

    return callback


def register_mixer_cb(
    handler: handler.Handler,
    mixer: Mixer,
):
    """Register the crossfader callback with a message handler.

    Args:
        handler (handler.Handler): message handler.
        mixer (Mixer): mixer model.
    """
    handler.register_handler(
        callback=make_crossfader_callback(mixer),
        component=mes.Component.MIXER,
        element=mes.Element.CROSSFADER,
    )
