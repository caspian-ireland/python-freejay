import logging
import tkinter as tk
from freejay import messages as mes
from freejay import produce_consume as prodcon
from freejay import tk_components

logger = logging.getLogger(__name__)


class TkMain(tk_components.TkComponent):
    def __init__(self, tkroot: tk_components.TkRoot):
        self.tkroot = tkroot
        self.frame = tk.Frame(tkroot)
        self.frame.pack()
        self.tkroot.bind(
            "<KeyPress>",
            lambda event: self.key(press_release=mes.PressRelease.PRESS, tkevent=event),
        )
        self.tkroot.bind(
            "<KeyRelease>",
            lambda event: self.key(
                press_release=mes.PressRelease.RELEASE, tkevent=event
            ),
        )


class TkDeck(tk_components.TkComponent):
    def __init__(self, tkroot: tk_components.TkRoot):
        self.tkroot = tkroot
        self.frame = tk.Frame(tkroot)
        self.frame.pack()
        self.play_btn = tk.Button(self.frame, text="play")
        self.play_btn.pack()
        self.play_btn.bind(
            "<ButtonPress-1>",
            lambda event: self.button(
                component=mes.Component.LEFT_DECK,
                element=mes.Element.PLAY_PAUSE,
                press_release=mes.PressRelease.PRESS,
            ),
        )
        self.play_btn.bind(
            "<ButtonRelease-1>",
            lambda event: self.button(
                component=mes.Component.LEFT_DECK,
                element=mes.Element.PLAY_PAUSE,
                press_release=mes.PressRelease.RELEASE,
            ),
        )


class Listener(prodcon.Consumer):
    def on_message_recieved(self, message):
        print(message)


if __name__ == "__main__":
    tkroot = tk_components.TkRoot()
    tkmain = TkMain(tkroot)
    left_deck = TkDeck(tkroot=tkroot)
    listener = Listener()
    listener.listen(tkroot)
    tkroot.mainloop()
