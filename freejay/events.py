import dataclasses
import typing
from enum import Enum
import time


class EventType(Enum):
    ButtonPress = 0
    ButtonRelease = 1
    KeyPressRaw = 2
    KeyReleaseRaw = 3
    KeyPress = 4
    KeyRelease = 5


class PressRelease(Enum):
    Press = 1
    Release = 0


class Action(Enum):
    Cue = 0
    PlayPause = 1


class Target(Enum):
    Mixer = 0
    LeftDeck = 1
    RightDeck = 2


class KeyPayload:
    def __init__(self, key: str, press_release: PressRelease):
        self.press_release = press_release
        self.key = key

    def __repr__(self):
        return f"<{str(self.__class__.__name__)} {str(self.__dict__)}>"


class ActionPayload:
    def __init__(
        self,
        press_release: PressRelease,
        target: Target,
        action: Action,
        value: typing.Optional[typing.Union[bool, int, float]],
    ):
        self.press_release = press_release
        self.target = target
        self.action = action
        self.value = value

    def __repr__(self):
        return f"<{str(self.__class__.__name__)} {str(self.__dict__)}>"


EVENT_TYPES: typing.Dict[EventType, type] = {
    EventType.KeyPressRaw: KeyPayload,
    EventType.KeyReleaseRaw: KeyPayload,
    EventType.ButtonPress: ActionPayload,
    EventType.ButtonRelease: ActionPayload,
    EventType.KeyPress: ActionPayload,
    EventType.KeyRelease: ActionPayload,
}


class Event:
    def __init__(self, type: EventType, payload: typing.Dict[str, typing.Any]):
        if type not in EVENT_TYPES:
            raise ValueError("Invalid event type: %s" % type)
        self.type = type
        payload_class = EVENT_TYPES[type]
        try:
            self.payload = payload_class(**payload)
        except TypeError:
            raise ValueError("Invalid payload for event type %s" % type)
        self.dt = time.time()

    def __repr__(self):
        return f"<{str(self.__class__.__name__)} {str(self.__dict__)}>"
