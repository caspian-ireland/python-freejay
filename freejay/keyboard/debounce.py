"""Functionality for Keyboard Debouncing."""

import typing
import collections
from threading import Timer
from freejay.messages import produce_consume as prodcon
from freejay.messages import messages as mes


class Debouncer(object):
    """
    Debounces key events so that press-and-hold works.

    Credit: Based on https://github.com/adamheins/tk-debouncer
    """

    def __init__(
        self,
        pressed_cb: typing.Callable[[typing.Any], None],
        released_cb: typing.Callable[[typing.Any], None],
        released_timeout: float = 0.05,
    ):
        """Construct debouncer object.

        Args:
            pressed_cb (typing.Callable[[typing.Any], None]): Callback for debounced
                'press' event.
            released_cb (typing.Callable[[typing.Any], None]): Callback for debounced
                'release' event.
            released_timeout (float, optional): How long to wait for new event before
                key release is accepted as true. Defaults to 0.05.
        """
        self.key_pressed = False
        self.key_released_timer = None
        self.released_timeout = released_timeout
        self.pressed_cb = pressed_cb
        self.released_cb = released_cb

    def _key_released_timer_cb(self, event):
        """
        Call key release callback on timer expiry.

        Called when the timer expires for a key up event,
        signifying that a key press has actually ended.
        """
        self.key_pressed = False
        self.released_cb(event)

    def pressed(self, event):
        """Key pressed callback."""
        # If timer set by up is active, cancel it, because the press is still
        # active.
        if self.key_released_timer:
            self.key_released_timer.cancel()
            self.key_released_timer = None

        # If the key is not currently pressed, mark it so and call the callback.
        if not self.key_pressed:
            self.key_pressed = True
            self.pressed_cb(event)

    def released(self, event):
        """Key released callback."""
        # Set a timer. If it is allowed to expire (not reset by another down
        # event), then we know the key has been released for good.
        self.key_released_timer = Timer(
            self.released_timeout, self._key_released_timer_cb, [event]
        )
        self.key_released_timer.start()


class KeyBoardDebouncer:
    """Debounces key events from multiple keys."""

    def __init__(
        self,
        getkey: typing.Callable[[typing.Any], str],
        pressed_cb: typing.Callable[[typing.Any], None],
        released_cb: typing.Callable[[typing.Any], None],
    ):
        """Construct KeyBoardDebouncer.

        Args:
            getkey (typing.Callable[[typing.Any], str]): function to extract the key
                from an event object. The key is used to track event press/release.
            pressed_cb (typing.Callable[[typing.Any], None]): Callback for debounced
                'press' event.
            released_cb (typing.Callable[[typing.Any], None]): Callback for debounced
                'release' event.
        """
        # Create a default dictionary that adds a Debouncer object
        # for each key.
        self.debouncer: typing.Dict[typing.Any, Debouncer]
        self.debouncer = collections.defaultdict(
            lambda: Debouncer(
                pressed_cb=pressed_cb,
                released_cb=released_cb,
            )
        )

        self.getkey = getkey

    def pressed(self, event):
        """Key pressed callback."""
        self.debouncer[self.getkey(event)].pressed(event)

    def released(self, event):
        """Key released callback."""
        self.debouncer[self.getkey(event)].released(event)


class MessageDebouncer(prodcon.Producer, prodcon.Consumer):
    """
    Debounce (Key) Messages.

    Wraps KeyBoardDebouncer and implements the Producer and Consumer
    protocols to listen for incoming messages and send debounced messages.

    Message is parsed for the key (str) which is used by KeyBoardDebouncer to
    create the debouncer for the key. When a message is recieved, it is parsed
    for press/release and directed to the appropriate method.
    On debounced press/release, the message is dispatched.
    """

    def __init__(self):
        """Construct MessageDebouncer."""
        self.debouncer = KeyBoardDebouncer(
            getkey=lambda m: m.content.sym,
            pressed_cb=self.send_message,
            released_cb=self.send_message,
        )

    def on_message_recieved(self, message: mes.Message[mes.Key]):
        """Direct incoming messages to the appropriate callback.

        Args:
            message (mes.Message[mes.Key]): Key Message.
        """
        if message.content.press_release == mes.PressRelease.PRESS:
            self.debouncer.pressed(message)
        else:
            self.debouncer.released(message)
