"""Messages to support communication between application components."""


# TODO- Not sure about the message 'sender' class.
# Should probably be replaced with a some sort of
# 'recipient' class as its really identifying where
# the message needs to end up (or at least the intended)
# action.

import typing
import time
import dataclasses
from enum import Enum


class PressRelease(Enum):
    """Enum for press or release (e.g. button or key action)."""

    PRESS = 1
    RELEASE = 0


class Component(Enum):
    """Enum for components."""

    MIXER = 0
    LEFT_DECK = 1
    RIGHT_DECK = 2
    DOWNLOAD = 3


class Element(Enum):
    """Enum for elements (part of a component)."""

    CUE = 0
    PLAY_PAUSE = 1
    NUDGE = 2
    STOP = 3
    JOG = 4
    DOWNLOAD = 5


class Source(Enum):
    """Enum for message sources."""

    MAIN_WINDOW = 0
    PLAYER_UI = 1
    PLAYER_SERVER = 2
    DOWNLOAD_UI = 3
    DOWNLOAD_SERVER = 3
    KEY_MAPPER = 4


class Trigger(Enum):
    """Enum for message trigger events."""

    BUTTON = 0
    KEY = 1
    DATA_INPUT = 2
    DATA_OUTPUT = 3


class Type(Enum):
    """Enum for message types."""

    BUTTON = 0
    KEY = 1
    DATA = 2


class Content:
    """Placeholder for Content class."""

    pass


@dataclasses.dataclass
class Key(Content):
    """Key message content."""

    press_release: PressRelease
    sym: str


@dataclasses.dataclass
class Button(Content):
    """Button message content."""

    press_release: PressRelease
    component: Component
    element: Element
    data: typing.Dict = dataclasses.field(default_factory=dict)

    def __post_init__(self):
        """
        Dataclass post init.

        If data is assigned none, replace with dict.
        """
        if self.data is None:
            self.data = dict()


@dataclasses.dataclass
class Data(Content):
    """Data message content."""

    component: Component
    element: Element
    data: typing.Dict = dataclasses.field(default_factory=dict)


@dataclasses.dataclass
class Sender:
    """Sender data class."""

    source: Source
    trigger: Trigger


T = typing.TypeVar("T", bound=Content)

_type_mapping = {
    "Key": Type.KEY,
    "Button": Type.BUTTON,
    "Data": Type.DATA,
}


@dataclasses.dataclass
class Message(typing.Generic[T]):
    """Message data class."""

    sender: Sender
    content: T
    type: typing.Optional[Type] = dataclasses.field(default=None)
    metadata: dict = dataclasses.field(default_factory=dict)

    def __post_init__(self):
        """
        Add automatically populated data.

        Adds message creation time to metadata under the key 'dt'.
        """
        self.metadata["dt"] = time.time()
        self.type = _type_mapping[type(self.content).__name__]
