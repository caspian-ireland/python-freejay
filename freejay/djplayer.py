"""Contains Audio Player Functionality.

The DJPlayer module holds the DJPlayer class, representing a DJ
audio player.
"""

import os
import errno
import logging
import functools
import time
import typing
from mpv import MPV

TCallable = typing.TypeVar("TCallable", bound=typing.Callable)
logger = logging.getLogger(__name__)


class MPVLoadError(Exception):
    """
    Exception raised for MPV load error.
    Likely due to incompatible file format.
    """

    def __init__(self, filename, message="MPV Could not load file."):
        self.filename = filename
        super().__init__(message)


def _check_file_loaded(func: TCallable) -> TCallable:
    """Decorator to check file is loaded before running DJPlayer methods.

    Args:
        func (TCallable): DJPlayer method

    Returns:
        TCallable: DJPlayer method wrapped with conditional statement.
    """

    @functools.wraps(func)
    def wrapper_check_file_loaded(self, *args, **kwargs):
        if self.filename:
            return func(self, *args, **kwargs)

        logger.info("File not loaded.")
        return None

    return typing.cast(TCallable, wrapper_check_file_loaded)


def mpv_log_handler(loglevel: str, component: str, message: str) -> None:
    """Convert mpv log events into log events

    Args:
        loglevel (str): Log level. Currently supported levels are: 'trace', 'debug',
            'warn', 'error', 'fatal'. All others will be raised as `logging.ERROR`.
        component (str): mpv component raising log event
        message (str): Log message
    """
    mpv_log_levels = {
        "fatal": logging.FATAL,
        "error": logging.ERROR,
        "warn": logging.WARN,
        "info": logging.INFO,
        "debug": logging.DEBUG,
        "trace": logging.DEBUG,
    }
    logger.log(
        mpv_log_levels.get(loglevel, logging.ERROR), "MPV-%s: %s", component, message
    )


class DJPlayer:
    """DJ Media player powered by MPV.

    Attributes:
        speed (float): The playback speed.
        filename (str): Audio file loaded in player.
        __speed(float): Playback speed.
        __playing(bool): Is audio currently playing?
        __cue_mode (bool): Is the player in cue mode?
        __time_cue (float): The cue point.
        __player(MPV): Media player.

    Methods:
        load(filename): Load a file into the deck
        play_pause(): Play or pause the track.
        stop(): Stop the track and return to start.
        cue_press(): Represents cue button press.
        cue_release(): Represents cue button release.
        nudge_press(amount): Represents pitch nudge press.
        nudge_release(): Represents pitch nudge release.
        jog(amount): Jog (relative seek) the track by amount.
    """

    def __init__(
        self, log_handler: typing.Callable[[str, str, str], None] | None = None
    ):

        """
        Args:
            log_handler(Callable | None, optional): A function to handle log events or
                None (Default). If none, MPV log events are not handled.
        """

        self.filename = ""
        self.__speed = 1.0
        self.__playing = False
        self.__cue_mode = True
        self.__time_cue = 0.0
        self.__player = MPV(log_handler=log_handler)

    def load(self, filename: str):

        """Load an audio file into the player

        Args:
            filename(str): path to audio file

        Raises:
            FileNotFoundError: If file `filename` cannot be found.
            MPVLoadError: If the file `filename` cannot be loaded by MPV
                media player. Likely due to incompatible file format.
        """

        # If the file is playing, do nothing and log a warning.
        if self.__playing:
            logger.warning("Track is still playing!")
        else:

            if not os.path.exists(filename):
                logger.error("File %s could not be found.", filename)
                raise FileNotFoundError(
                    errno.ENOENT, os.strerror(errno.ENOENT), filename
                )

            self.__pause()
            self.__cue_mode = True
            self.__player.play(filename=filename)
            time.sleep(0.1)

            # Dirty workaround to check if file succesfully loaded.
            # See issue https://github.com/jaseg/python-mpv/issues/194
            if self.__player.path:
                logger.info("File %s loaded.", filename)
                self.filename = filename
                self.__time_cue = self.__player.time_start
            else:
                self.filename = ""
                self.__time_cue = 0.0
                logger.error("File %s could not be loaded.", filename)
                raise MPVLoadError(filename)

    @_check_file_loaded
    def play_pause(self):
        """Play or pause the track."""
        if not self.__playing:
            self.__play()
        # If in cue mode and playing then user is cueing the track
        # and playback should continue
        else:
            if not self.__cue_mode:
                self.__pause()

        self.__cue_mode = False

    def __play(self):
        self.__player.pause = False
        self.__playing = True

    def __pause(self):
        self.__player.pause = True
        self.__playing = False

    @_check_file_loaded
    def stop(self):
        """Stop playback and return to start of track."""
        self.__pause()
        self.__cue_mode = True
        self.__player.seek(self.__player.time_start, reference="absolute")

    @_check_file_loaded
    def cue_press(self):
        """Imitates cue button press (see method `cue_release` for release)"""
        # Cue behaviour uses the `__cue_mode` attribute to track whether the
        # player is in cue mode. Cue mode is activated when the user calls the
        # `cue_press` or `stop` methods, and is deactivated when the user calls the
        # `play_pause` method. In cue mode, `cue_press` will set the cue point and
        # start the track playing. When not in cue mode, `cue_press` will set the
        # cue point and pause the track. This mimics mainstream DJ software behaviour.
        # Note if track is playing, `cue_press` will not set the cue point.
        if not self.__playing:
            self.__time_cue = self.__player.time_pos

        if self.__cue_mode:
            self.__play()
        else:
            self.__pause()

        self.__cue_mode = True

    @_check_file_loaded
    def cue_release(self):
        """Imitates cue button release (see method `cue_press` for press)"""
        if self.__cue_mode:
            self.__pause()
            self.__player.seek(amount=self.__time_cue, reference="absolute")

    @property
    def speed(self) -> float:
        """Playback speed"""
        return self.__speed

    @speed.setter  # When you set the speed, update it in the player too.
    def speed(self, speed: float):
        self.__player.speed = speed
        self.__speed = speed

    def nudge_press(self, amount: float = 0.15):
        """
        Pitch nudge start
        Nudge the track by temporarily changing the speed. Represents
        the start of the nudge, see also `nudge_release`.

        Args:
            amount(float): Nudge amount. Positive numbers represent speed
                increase and negative numbers represent speed decrease. E.g
                amount = -0.15 would decrease speed by 15%.

        Raises:
            ValueError if amount outside the range (-1, 1)
        """
        if not -1 < amount < 1:
            raise ValueError("Amount must be in the range (-1, 1).")
        self.__player.speed = self.__player.speed * (1 + amount)  # type: ignore

    def nudge_release(self):
        """Pitch nudge stop. See also `nudge_press`"""
        self.__player.speed = self.speed

    def jog(self, amount: float = 10.0):
        """Jog the track

        Args:
            amount(float): Number of seconds to jog. Positive numbers
                represent forward, negative numbers represent backwards.
        """
        self.__player.seek(amount, reference="relative")
        self.__cue_mode = False
