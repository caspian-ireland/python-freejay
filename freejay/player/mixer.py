"""
Contains DJ Mixer Model.

This module currently contains the Mixer and Crossfader classes.
"""

import logging
import typing
from freejay.player.djplayer import DJPlayer

logger = logging.getLogger(__name__)


class Mixer:
    """
    DJ Mixer Model.

    Keeps a reference to the 'connected' left and right decks.
    Contains DJ Mixer functionality, currently just a crossfader.

    The general idea is that any functionality that requires co-ordination between
    players will sit here.

    Note: decision to be made as to whether EQ control becomes a player.DJPlayer
    feature, or a player.Mixer feature.
    """

    def __init__(self, left_deck: DJPlayer, right_deck: DJPlayer):
        """Construct Mixer.

        Args:
            left_deck (DJPlayer): Left Deck DJPlayer
            right_deck (DJPlayer): Right Deck DJPlayer
        """
        self.left_deck = left_deck
        self.right_deck = right_deck
        self.crossfader = Crossfader(self)


class Crossfader:
    """
    Crossfader Model.

    The Crossfader class models a DJ Mixer crossfader. Moving the crossfader position
    to the left (represented here as a position of 0.0) will result in the left deck
    having maximum volume and the right deck having zero volume. Moving the crossfader
    position over to the middle (position of 0.5) will be a blend of both decks and
    so on.

    The Crossfader curve describes relationship between deck volume and crossfader
    position. A low curve value will result in a gradual fade between the left and
    right deck, a high curve will result in an abrupt transition, useful for
    'scratching'.

    Note: Crossfader is not intended to be constructed directly, but rather
    by the Mixer class.
    """

    def __init__(self, mixer: Mixer):
        """Construct Crossfader.

        Args:
            mixer (Mixer): reference to parent mixer.
        """
        self.mixer = mixer
        self.__curve = 0.5
        self.__position = 0.5

    @property
    def position(self) -> float:
        """Position (getter)."""
        return self.__position

    @position.setter
    def position(self, value: float):
        """Position (setter).

        Args:
            value (float): position to set. Must be between 0 and 1.
        """
        if not 0 <= value <= 1:
            logger.error("Crossfader position must be between 0 and 1.")
            ValueError("Crossfader position must be between 0 and 1.")
        self.__position = value
        # Update deck volume levels
        level_left, level_right = self.calculate_levels(position=value)
        self.mixer.left_deck.volume = level_left * 100
        self.mixer.right_deck.volume = level_right * 100

    @property
    def curve(self) -> float:
        """Curve (getter)."""
        return self.__curve

    @curve.setter
    def curve(self, value: float):
        """Curve (setter).

        Args:
            value (float): value to set. Must be between 0 and 1.
        """
        if not 0 <= value <= 1:
            logger.error("Crossfader curve must be between 0 and 1.")
            ValueError("Crossfader curve must be between 0 and 1.")

        # Division by zero error on curve = 1
        if value == 1:
            value = 0.99
        self.__curve = value

    def calculate_levels(self, position: float) -> typing.Tuple[float, float]:
        """Calculate deck volume levels.

        Use the crossfader position and curve to calculate the required volume
        on each deck.

        Args:
            position (float): crossfader position.

        Returns:
            typing.Tuple[float, float]: (left deck volume, right deck volume)
        """
        level_left = min(1, 1 - ((position - self.__curve) / (1 - self.__curve)))
        level_right = min(1, 1 - ((1 - position - self.__curve) / (1 - self.__curve)))
        return (level_left, level_right)
