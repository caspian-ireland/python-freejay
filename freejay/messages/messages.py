"""Messages to support communication between application components."""


import typing
import time
import dataclasses
from enum import Enum, auto


class PressRelease(Enum):
    """Enum for press or release (e.g. button or key action)."""

    PRESS = auto()
    RELEASE = auto()


class Component(Enum):
    """Enum for components."""

    MIXER = auto()
    LEFT_DECK = auto()
    RIGHT_DECK = auto()
    DOWNLOAD = auto()


class Element(Enum):
    """Enum for elements (part of a component)."""

    CUE = auto()
    PLAY_PAUSE = auto()
    NUDGE = auto()
    STOP = auto()
    JOG = auto()
    LOAD = auto()
    DOWNLOAD = auto()
    CROSSFADER = auto()


class Source(Enum):
    """Enum for message sources."""

    MAIN_WINDOW = auto()
    PLAYER_VIEW = auto()
    PLAYER_MODEL = auto()
    DOWNLOAD_VIEW = auto()
    DOWNLOAD_MODEL = auto()
    KEY_MAPPER = auto()
    MIXER = auto()


class Trigger(Enum):
    """Enum for message trigger events."""

    BUTTON = auto()
    KEY = auto()
    SLIDER = auto()
    DATA_INPUT = auto()
    DATA_OUTPUT = auto()
    EXCEPTION = auto()
    TEXT_ENTRY = auto()


class Type(Enum):
    """Enum for message types."""

    BUTTON = auto()
    KEY = auto()
    DATA = auto()


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
