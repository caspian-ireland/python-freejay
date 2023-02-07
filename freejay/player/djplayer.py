"""Contains DJ Audio Player Functionality.

The DJPlayer module holds the DJPlayer class, representing a DJ audio player.
"""

import logging
from freejay.player.player import IPlayer

logger = logging.getLogger(__name__)


class DJPlayer:
    """DJ audio player.

    Attributes:
        speed (float): The playback speed.
        filename (str): Audio file loaded in player.
        time_pos (float): Current time in track.
        time_cue (float): Cue point time in track.
        volume(float): The audio volume.
        __filename(str): Audio file loaded in player.
        __speed(float): Playback speed.
        __cue_mode (bool): Is the player in cue mode?
        __time_cue (float): The cue point.
        __nudge_value(float): Current pitch nudge value.
        __player(IPlayer): Audio player.

    Methods:
        load(filename): Load a file into the deck
        play_pause(): Play or pause the track.
        stop(): Stop the track and return to start.
        cue_press(): Represents cue button press.
        cue_release(): Represents cue button release.
        nudge_press(value): Represents pitch nudge press.
        nudge_release(): Represents pitch nudge release.
        jog(value): Jog (relative seek) the track by value.
        __nudge(value): Helper to apply pitch nudge.
    """

    def __init__(self, player: IPlayer):
        """
        Construct DJPlayerMpv.

        Args:
            player(IPlayer): Media player.
        """
        self.__filename = ""
        self.__speed = 1.0
        self.__cue_mode = True
        self.__time_cue = 0.0
        self.__nudge_value = 0.0
        self.__player = player

    def load(self, filename: str):
        """Load an audio file into the player.

        Args:
            filename(str): path to audio file

        Raises:
            FileNotFoundError: If file `filename` cannot be found.
            MPVLoadError: If the file `filename` cannot be loaded by MPV
                media player. Likely due to incompatible file format.
        """
        # If the file is playing, do nothing and log a warning.
        if self.__player.playing:
            logger.warning("Track is still playing!")
        else:
            self.__cue_mode = True
            self.__player.load(filename=filename)
            self.__filename = filename
            self.speed = 1.0
            self.__time_cue = self.__player.time_start

    def play_pause(self):
        """Play or pause the track."""
        if not self.__player.playing:
            self.__player.play()
        # If in cue mode and playing then user is cueing the track
        # and playback should continue
        else:
            if not self.__cue_mode:
                self.__player.pause()

        self.__cue_mode = False

    def stop(self):
        """Stop playback and return to start of track."""
        self.__player.pause()
        self.__cue_mode = True
        self.__player.seek(self.__player.time_start, reference="absolute")

    def cue_press(self):
        """Imitates cue button press (see method `cue_release` for release)."""
        # Cue behaviour uses the `__cue_mode` attribute to track whether the
        # player is in cue mode. Cue mode is activated when the user calls the
        # `cue_press` or `stop` methods, and is deactivated when the user calls the
        # `play_pause` method. In cue mode, `cue_press` will set the cue point and
        # start the track playing. When not in cue mode, `cue_press` will set the
        # cue point and pause the track. This mimics mainstream DJ software behaviour.
        # Note if track is playing, `cue_press` will not set the cue point.
        if not self.__player.playing:
            self.__time_cue = self.__player.time_pos

        if self.__cue_mode:
            self.__player.play()
        else:
            self.__player.pause()

        self.__cue_mode = True

    def cue_release(self):
        """Imitates cue button release (see method `cue_press` for press)."""
        if self.__cue_mode:
            self.__player.seek(amount=self.__time_cue, reference="absolute")
            if self.__player.playing:
                self.__player.pause()

    @property
    def speed(self) -> float:
        """Playback speed."""
        return self.__speed

    @speed.setter  # When you set the speed, update it in the player too.
    def speed(self, val: float):
        self.__speed = val
        self.__nudge(self.__nudge_value)

    @property
    def volume(self) -> float:
        """Playback volume."""
        return self.__player.volume

    @volume.setter
    def volume(self, val: float):
        self.__player.volume = val

    @property
    def filename(self) -> str:
        """Filename."""
        return self.__filename

    @property
    def time_pos(self) -> float:
        """Time position."""
        return self.__player.time_pos

    @property
    def time_cue(self) -> float:
        """Cue point time."""
        return self.__time_cue

    def nudge_press(self, value: float = 0.15):
        """
        Pitch nudge start.

        Nudge the track by temporarily changing the speed. Represents
        the start of the nudge, see also `nudge_release`.

        Args:
            value(float): Nudge value. Positive numbers represent speed
                increase and negative numbers represent speed decrease. E.g
                value = -0.15 would decrease speed by 15%.

        Raises:
            ValueError if value outside the range (-1, 1)
        """
        if not -1 < value < 1:
            raise ValueError("value must be in the range (-1, 1).")
        else:
            self.__nudge(value)
            self.__nudge_value = value

    def nudge_release(self):
        """Pitch nudge stop. See also `nudge_press`."""
        self.__nudge(0)
        self.__nudge_value = 0.0

    def __nudge(self, value):
        self.__player.speed = self.speed * (1 + value)

    def jog(self, value: float = 10.0):
        """Jog the track.

        Args:
            value(float): Number of seconds to jog. Positive numbers
                represent forward, negative numbers represent backwards.
        """
        self.__player.seek(value, reference="relative")
        self.__cue_mode = False
