"""
Player callback functions.

Callback functions are registered with the message handler. The handler
will check the content of incoming messages and call the appropriate callback,
changing the state of the audio player as required.
"""

import typing
from freejay.player import djplayer
from freejay.message_dispatcher import handler_cb
from freejay.message_dispatcher import handler
from freejay.messages import messages as mes


def make_cue_callback(
    player: djplayer.DJPlayer,
) -> typing.Callable[[mes.Message[mes.Button]], None]:
    """Make a 'cue' callback.

    Args:
        player (djplayer.DJPlayer): Player to 'cue' on callback.

    Returns:
        typing.Callable[[mes.Message[mes.Button]], None]: Callback function
    """
    callback = handler_cb.make_button_cb(
        press_cb=player.cue_press, release_cb=player.cue_release
    )
    return callback


def make_play_callback(
    player: djplayer.DJPlayer,
) -> typing.Callable[[mes.Message[mes.Button]], None]:
    """Make a 'play' callback.

    Args:
        player (djplayer.DJPlayer): Player to 'play' on callback.

    Returns:
        typing.Callable[[mes.Message[mes.Button]], None]: Callback function
    """
    callback = handler_cb.make_button_cb(press_cb=player.play_pause)
    return callback


def make_stop_callback(
    player: djplayer.DJPlayer,
) -> typing.Callable[[mes.Message[mes.Button]], None]:
    """Make a 'stop' callback.

    Args:
        player (djplayer.DJPlayer): Player to 'stop' on callback.

    Returns:
        typing.Callable[[mes.Message[mes.Button]], None]: Callback function
    """
    callback = handler_cb.make_button_cb(press_cb=player.stop)
    return callback


def make_nudge_callback(
    player: djplayer.DJPlayer,
) -> typing.Callable[[mes.Message[mes.Button]], None]:
    """Make a 'nudge' callback.

    Args:
        player (djplayer.DJPlayer): Player to 'nudge' on callback.

    Returns:
        typing.Callable[[mes.Message[mes.Button]], None]: Callback function
    """
    callback = handler_cb.make_button_cb(
        press_cb=player.nudge_press, release_cb=player.nudge_release
    )
    return callback


def make_jog_callback(
    player: djplayer.DJPlayer,
) -> typing.Callable[[mes.Message[mes.Button]], None]:
    """Make a 'jog' callback.

    Args:
        player (djplayer.DJPlayer): Player to 'jog' on callback.

    Returns:
        typing.Callable[[mes.Message[mes.Button]], None]: Callback function
    """
    callback = handler_cb.make_button_cb(press_cb=player.jog)
    return callback


def register_player_cb(
    handler: handler.Handler, player: djplayer.DJPlayer, component: mes.Component
):
    """Register player callbacks.

    Args:
        handler (handler.Handler): Message handler
        player (djplayer.DJPlayer): Player
        component (mes.Component): Component (e.g. LEFT_DECK, RIGHT_DECK)
    """
    handler.register_handler(
        callback=make_cue_callback(player),
        component=component,
        element=mes.Element.CUE,
    )
    handler.register_handler(
        callback=make_play_callback(player),
        component=component,
        element=mes.Element.PLAY_PAUSE,
    )
    handler.register_handler(
        callback=make_stop_callback(player),
        component=component,
        element=mes.Element.STOP,
    )
    handler.register_handler(
        callback=make_nudge_callback(player),
        component=component,
        element=mes.Element.NUDGE,
    )

    handler.register_handler(
        callback=make_jog_callback(player),
        component=component,
        element=mes.Element.JOG,
    )
