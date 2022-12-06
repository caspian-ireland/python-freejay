"""Contains Generic Audio Player Functionality.

The Player module holds the Player interface and implementations, representing a generic
audio player.
"""

import os
import errno
import logging
import functools
import typing
import abc
import retry
from mpv import MPV

TCallable = typing.TypeVar("TCallable", bound=typing.Callable)
logger = logging.getLogger(__name__)


"""Player Interface"""


class Player(abc.ABC):
    """Audio player interface."""

    @abc.abstractmethod
    def __init__(self, player):
        """Construct Player.

        Args:
            player: media player.

        """
        pass

    @property
    @abc.abstractmethod
    def speed(self) -> float:
        """Playback speed."""
        pass

    @speed.setter
    @abc.abstractmethod
    def speed(self, val: float):
        pass

    @property
    @abc.abstractmethod
    def time_start(self) -> float:
        """Start time of track."""
        pass

    @property
    @abc.abstractmethod
    def time_end(self) -> float:
        """End time of track."""
        pass

    @property
    @abc.abstractmethod
    def time_pos(self) -> float:
        """Time position of track."""
        pass

    @property
    @abc.abstractmethod
    def loaded(self) -> bool:
        """Is the player loaded with a track."""
        pass

    @property
    @abc.abstractmethod
    def playing(self) -> bool:
        """Is the track playing."""
        pass

    @abc.abstractmethod
    def load(self, filename: str):
        """Load a track.

        Args:
            filename (str): filename to load into player.
        """
        pass

    @abc.abstractmethod
    def play(self):
        """Play the track."""
        pass

    @abc.abstractmethod
    def pause(self):
        """Pause the track."""
        pass

    @abc.abstractmethod
    def seek(self, amount: float, reference: str = "absolute"):
        """Seek to a position in the track.

        Args:
            amount(float): Amount to seek in seconds.
            reference(str): Allowed values ('absolute', 'relative')
                Defaults to 'absolute'.

        """
        pass


class LoadError(Exception):
    """
    Exception raised for load error. Likely due to incompatible file format.
    """

    def __init__(self, filename: str, message: str = "Could not load file."):
        """Construct LoadError.

        Args:
            filename (str): The file that caused a load error
            message (str, optional): Exception message.
                Defaults to 'Could not load file.'.
        """
        self.filename = filename
        super().__init__(message)


class FileNotLoaded(Exception):
    """Exception raised for file not loaded.

    Used when a Player method requires a track to be loaded.
    """

    def __init__(self, message: str = "No file loaded."):
        """Construct FileNotLoaded.

        Args:
            message (str, optional): Exception message. Defaults to "No file loaded.".
        """
        super().__init__(message)


def _check_file_loaded(func: TCallable) -> TCallable:
    """Check file is loaded before running Player methods.

    Args:
        func (TCallable): Player method

    Returns:
        TCallable: Player method wrapped with conditional statement.
    """

    @functools.wraps(func)
    def wrapper_check_file_loaded(self, *args, **kwargs):
        if self.loaded:
            return func(self, *args, **kwargs)

        logger.error("File not loaded.")
        raise FileNotLoaded()

    return typing.cast(TCallable, wrapper_check_file_loaded)


"""MPV Implementation"""


def mpv_log_handler(loglevel: str, component: str, message: str) -> None:
    """Convert mpv log events into log events.

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


class PlayerMpv(Player):
    """DJ Media player powered by MPV.

    Attributes:
        speed (float): The playback speed.
        loaded(boo): Is the player loaded.
        time_start(float): The start time of the track.
        time_end(float): The end time of the track.
        time_pos(float): The current time of the track.
        playing(bool): Is the track playing.
        __player(MPV): Media player.

    Methods:
        load(filename): Load a file into the deck
        play(): Play the track.
        pause(): Pause the track.
        seek(amount, reference): Seek to a position in the track.
    """

    def __init__(self, player: MPV):
        """
        Construct PlayerMpv.

        Args:
            player(MPV): MPV audio player.
        """
        self.__player = player
        self.__playing = False

    def load(self, filename: str):
        """Load an audio file into the player.

        Args:
            filename(str): path to audio file

        Raises:
            FileNotFoundError: If file `filename` cannot be found.
            LoadError: If the file `filename` cannot be loaded by MPV
                media player. Likely due to incompatible file format.
        """
        if not os.path.exists(filename):
            logger.error("File %s could not be found.", filename)
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), filename)

        self.__playing = False
        self.__player.pause = True
        self.__player.play(filename=filename)
        self.__check_load_error(filename=filename)

    @retry.retry(exceptions=LoadError, tries=3, delay=0.1)
    def __check_load_error(self, filename):
        # Dirty workaround to check if file succesfully loaded.
        # See issue https://github.com/jaseg/python-mpv/issues/194
        if self.loaded:
            logger.info("File %s loaded.", filename)
        else:
            logger.error("File %s could not be loaded.", filename)
            raise LoadError(filename)

    @_check_file_loaded
    def play(self):
        """Play the track."""
        self.__player.pause = False
        self.__playing = True

    @_check_file_loaded
    def pause(self):
        """Pause the track."""
        self.__player.pause = True
        self.__playing = False

    @_check_file_loaded
    def seek(self, amount: float, reference: str = "absolute"):
        """Seek to a position in the track.

        Args:
            amount (float): Amount to seek in seconds
            reference (str, optional): Should seek be 'relative' or 'absolute'.
                Defaults to "absolute".

        Raises:
            ValueError: If reference not in ('relative', 'absolute') then ValueError
                is raised.
        """
        allowed_reference = ("absolute", "relative")
        if reference not in allowed_reference:
            raise ValueError(f"seek: reference must be one of {allowed_reference}.")

        self.__player.seek(amount=amount, reference=reference)

    @property
    def speed(self) -> float:
        """Playback speed."""
        return self.__player.speed

    @speed.setter  # When you set the speed, update it in the player too.
    def speed(self, val: float):
        self.__player.speed = val

    @property
    @_check_file_loaded
    def time_start(self) -> float:
        """Get the track start time."""
        return self.__player.time_start

    @property
    @_check_file_loaded
    def time_end(self) -> float:
        """Get the track end time."""
        return self.__player.duration

    @property
    @_check_file_loaded
    def time_pos(self) -> float:
        """Get the current time position."""
        return self.__player.time_pos

    @property
    def loaded(self) -> bool:
        """Is a track loaded."""
        if self.__player.path:
            return True
        else:
            return False

    @property
    def playing(self) -> bool:
        """Is the track playing."""
        return self.__playing
