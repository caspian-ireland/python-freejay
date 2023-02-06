"""Create Application."""

import os
import logging
import mpv
from freejay import tk_components
from freejay import messages as mes
from freejay import worker
from freejay import router
from freejay import debounce
from freejay.djplayer import DJPlayer
from freejay.player import PlayerMpv
from freejay.handler import Handler
from freejay.keymapper import KeyMapper, keybindings
from freejay import player_cb

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
    queue: worker.QueueListener,
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
        queue (worker.QueueListener): Message queue
        debouncer (debounce.MessageDebouncer): Message debouncer
        keymapper (KeyMapper): Keybindings mapper
        tkroot (tk_components.TkRoot): Tkinter top-level widget
    """
    # Register route for sending messages to the queue.
    message_router.register_route(
        condition=lambda m: m.type
        in (
            mes.Type.BUTTON,
            mes.Type.SET_VALUE,
            mes.Type.VALUE_BUTTON,
        ),
        consumer=queue,
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
    tkroot = tk_components.TkRoot()
    tkmain = tk_components.TkMain(tkroot, source=mes.Source.MAIN_WINDOW)  # noqa
    left_deck = tk_components.TkDeck(
        tkroot=tkroot, source=mes.Source.PLAYER, component=mes.Component.LEFT_DECK
    )
    right_deck = tk_components.TkDeck(
        tkroot=tkroot, source=mes.Source.PLAYER, component=mes.Component.RIGHT_DECK
    )

    # Configure layout
    tkroot.grid_rowconfigure(1, weight=1)
    tkroot.grid_columnconfigure(0, weight=1)

    left_deck.frame.grid(row=0, column=0, sticky="ew")
    right_deck.frame.grid(row=0, column=1, sticky="ew")

    # === Initialise backend components ===
    left_player = DJPlayer(player=PlayerMpv(mpv.MPV()))

    left_player.load(filename=os.path.join("assets", "HoliznaCC0 - Mercury.mp3"))

    right_player = DJPlayer(player=PlayerMpv(mpv.MPV()))
    right_player.load(filename=os.path.join("assets", "HoliznaCC0 - Mercury.mp3"))

    handler = Handler()
    debouncer = debounce.MessageDebouncer()
    keymapper = KeyMapper(keybindings)
    message_router = router.MessageRouter()
    q = worker.QueueListener()
    worker_i = worker.Worker(worker.WorkCycle(q, handler))

    # === Configure backend components ===

    register_player_callbacks(
        handler=handler, left_deck=left_player, right_deck=right_player
    )

    register_message_routes(
        message_router=message_router,
        queue=q,
        debouncer=debouncer,
        keymapper=keymapper,
        tkroot=tkroot,
    )

    # === Start Application ===

    # Start workcycle
    worker_i.start()
    # Start tkinter
    tkroot.mainloop()
