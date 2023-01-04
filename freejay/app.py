import tkinter as tk
import queue
import threading
import mpv
from freejay import djplayer, player, route
from freejay import events, keybindings, debounce, control


class Deck:
    def __init__(self, main, event_router, target):
        self.main = main

        self.frame = tk.Frame(main)
        self.frame.pack()
        self.target = target
        self.event_router = event_router
        self.main.bind("<KeyPress>", lambda event: self.key_press(event))
        self.main.bind("<KeyRelease>", lambda event: self.key_release(event))
        self.play_btn = tk.Button(self.frame, text="play")
        self.play_btn.pack()
        self.play_btn.bind(
            "<ButtonPress-1>",
            lambda event: self.button_press(events.Action.PlayPause, 0),
        )

    def button_event(self, type, press_release, action, value):
        event = events.Event(
            type=type,
            payload={
                "press_release": press_release,
                "target": self.target,
                "action": action,
                "value": value,
            },
        )
        self.send_event(event)

    def button_press(self, action, value):
        self.button_event(
            type=events.EventType.ButtonPress,
            press_release=events.PressRelease.Press,
            action=action,
            value=value,
        )

    def button_release(self, action, value):
        self.button_event(
            type=events.EventType.ButtonRelease,
            press_release=events.PressRelease.Release,
            action=action,
            value=value,
        )

    def key_event(self, type, press_release, key):
        event = events.Event(
            type=type, payload={"press_release": press_release, "key": key}
        )
        self.send_event(event)

    def key_press(self, tkevent):
        self.key_event(
            type=events.EventType.KeyPressRaw,
            press_release=events.PressRelease.Press,
            key=tkevent.keysym,
        )

    def key_release(self, tkevent):
        self.key_event(
            type=events.EventType.KeyReleaseRaw,
            press_release=events.PressRelease.Release,
            key=tkevent.keysym,
        )

    def send_event(self, event):
        self.event_router.route(event)


if __name__ == "__main__":
    loc = "/Users/Caspian/Downloads/Aladdin  DJ Aphrodite - We Enter (Heavenly Remix 1994).mp4"
    left_player = djplayer.DJPlayer(player=player.PlayerMpv(player=mpv.MPV()))
    left_player.load(loc)
    main = tk.Tk()
    q = queue.Queue()
    event_router = route.EventRouter()
    key_event_mapper = keybindings.KeyEventMapper(keybindings.keybindings)

    debouncer_key_cb = debounce.make_debouncer_key_cb(
        event_router=event_router, key_event_mapper=key_event_mapper
    )

    debouncer = debounce.KeyBoardDebouncer(
        keyfunc=lambda event: event.payload.key,
        pressed_cb=debouncer_key_cb,
        released_cb=debouncer_key_cb,
    )

    event_router.routetable = route.make_routetable(
        keybindings=keybindings.keybindings, debouncer=debouncer, q=q
    )

    deck = Deck(main, event_router=event_router, target=events.Target.LeftDeck)

    t = threading.Thread(target=control.workcycle, args=(left_player, q))
    t.daemon = True
    t.start()

    main.mainloop()
