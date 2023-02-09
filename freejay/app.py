"""Create Application."""

import os
import logging
import mpv
import customtkinter as ctk
from freejay.tk import tk_components
from freejay.tk import tk_player
from freejay.messages import messages as mes
from freejay.message_dispatcher import worker
from freejay.messages import router
from freejay.keyboard import debounce
from freejay.player.djplayer import DJPlayer
from freejay.player.player import PlayerMpv
from freejay.message_dispatcher.handler import Handler
from freejay.keyboard.keymapper import KeyMapper, keybindings
from freejay.player import player_cb

logger = logging.getLogger(__name__)


def register_player_callbacks(
    handler: Handler, left_deck: DJPlayer, right_deck: DJPlayer
):
    """
    Register player callbacks.

    Args:
        handler (Handler): Message Handler
        left_deck (DJPlayer): Left Player
        right_deck (DJPlayer): Right Player
    """
    player_cb.register_player_cb(
        handler=handler, player=left_deck, component=mes.Component.LEFT_DECK
    )
    player_cb.register_player_cb(
        handler=handler, player=right_deck, component=mes.Component.RIGHT_DECK
    )


def register_message_routes(
    message_router: router.MessageRouter,
    server_queue: worker.QueueListener,
    debouncer: debounce.MessageDebouncer,
    keymapper: KeyMapper,
    tkroot: tk_components.TkRoot,
):
    """
    Register Message Routes.

    Application components communicate via messages and are connected
    using the 'Producer' and 'Consumer' protocols. This function registers
    those produce/consume relationships.

    Args:
        message_router (router.MessageRouter): Message router
        server_queue (worker.QueueListener): Message queue
        debouncer (debounce.MessageDebouncer): Message debouncer
        keymapper (KeyMapper): Keybindings mapper
        tkroot (tk_components.TkRoot): Tkinter top-level widget
    """
    # Register route for sending messages to the server_queue.
    message_router.register_route(
        condition=lambda m: m.type
        in (
            mes.Type.BUTTON,
            mes.Type.DATA,
        ),
        consumer=server_queue,
    )

    # Register route for sending messages to the message debouncer
    message_router.register_route(
        condition=lambda m: m.type == mes.Type.KEY, consumer=debouncer
    )

    # Debouncer sends messages to keymapper
    keymapper.listen(debouncer)
    # Tkroot and Keymapper send messages to message router
    message_router.listen(keymapper)
    message_router.listen(tkroot)


def make_app():
    """
    Configure and start the application.
    """
    # === Configure Tkinter application. ===

    # Create tkinter components
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    tkroot = tk_components.TkRoot()
    tkmain = tk_components.TkMain(
        tkroot, parent=tkroot, source=mes.Source.MAIN_WINDOW
    )  # noqa

    left_deck = tk_player.TkDeck(
        tkroot=tkroot,
        parent=tkmain.frame,
        source=mes.Source.PLAYER_UI,
        component=mes.Component.LEFT_DECK,
    )
    right_deck = tk_player.TkDeck(
        tkroot=tkroot,
        parent=tkmain.frame,
        source=mes.Source.PLAYER_UI,
        component=mes.Component.RIGHT_DECK,
    )

    # Configure layout
    tkroot.geometry("1200x300")
    tkroot.grid_rowconfigure(0, weight=1)
    tkroot.grid_columnconfigure(0, weight=1)
    tkmain.frame.grid(row=0, column=0)
    tkmain.frame.grid_rowconfigure(0, weight=1)
    tkmain.frame.grid_columnconfigure((0, 1), weight=1)
    left_deck.frame.grid(row=0, column=0, sticky="w")
    right_deck.frame.grid(row=0, column=1, sticky="e")

    # === Initialise backend components ===

    # Initialise Media Players
    left_player = DJPlayer(player=PlayerMpv(mpv.MPV()))

    left_player.load(filename=os.path.join("assets", "HoliznaCC0 - Mercury.mp3"))

    right_player = DJPlayer(player=PlayerMpv(mpv.MPV()))
    right_player.load(filename=os.path.join("assets", "HoliznaCC0 - Mercury.mp3"))

    # Initialise Messaging
    debouncer = debounce.MessageDebouncer()
    keymapper = KeyMapper(keybindings)
    message_router = router.MessageRouter()

    # Initialise Workers
    server_handler = Handler()
    ui_handler = Handler()
    work_streams = worker.WorkStreams()
    server_worker = worker.Worker(
        worker.WorkCycle(worker.QueueListener(), server_handler)
    )
    ui_worker = worker.Worker(worker.WorkCycle(worker.QueueListener(), ui_handler))
    work_streams.add_worker(worker=server_worker, name="server")
    work_streams.add_worker(worker=ui_worker, name="ui")

    # === Configure backend components ===

    register_player_callbacks(
        handler=server_handler, left_deck=left_player, right_deck=right_player
    )

    register_message_routes(
        message_router=message_router,
        server_queue=work_streams.get_queue("server"),
        debouncer=debouncer,
        keymapper=keymapper,
        tkroot=tkroot,
    )

    # === Start Application ===

    # Start workers
    work_streams.start()
    # Start tkinter
    tkroot.mainloop()
