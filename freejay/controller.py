"""Application Controller."""

import logging
from freejay.messages import messages as mes
from freejay.message_dispatcher import worker
from freejay.messages import router
from freejay.keyboard import debounce
from freejay.message_dispatcher.handler import Handler
from freejay.keyboard.keymapper import KeyMapper, keybindings
from freejay.controller_cb import player_cb
from freejay.controller_cb import download_cb
from freejay.controller_cb import mixer_cb
from .view import View
from .model import Model

logger = logging.getLogger(__name__)


def register_model_callbacks(handler: Handler, model: Model):
    """
    Register model callbacks.

    Args:
        handler (Handler): Message Handler
        model (Model): Model
    """
    player_cb.register_player_cb(
        handler=handler,
        player=model.left_deck,
        download_manager=model.download,
        component=mes.Component.LEFT_DECK,
    )
    player_cb.register_player_cb(
        handler=handler,
        player=model.right_deck,
        download_manager=model.download,
        component=mes.Component.RIGHT_DECK,
    )
    mixer_cb.register_mixer_cb(handler=handler, mixer=model.mixer)

    download_cb.register_download_model_cb(
        handler=handler, download_manager=model.download
    )


def register_view_callbacks(handler: Handler, view: View):
    """
    Register view callbacks.

    Args:
        handler (Handler): Message Handler
        view (View): View
    """
    download_cb.register_download_view_cb(handler=handler, download_view=view.download)


def register_view_message_routes(
    message_router: router.MessageRouter,
    model_queue: worker.QueueListener,
    debouncer: debounce.MessageDebouncer,
    keymapper: KeyMapper,
    view: View,
):
    """
    Register 'View' Message Routes.

    Application components communicate via messages and are connected
    using the 'Producer' and 'Consumer' protocols. This function registers
    those produce/consume relationships for messages coming from the app View.

    Args:
        message_router (router.MessageRouter): Message router
        model_queue (worker.QueueListener): Message queue
        debouncer (debounce.MessageDebouncer): Message debouncer
        keymapper (KeyMapper): Keybindings mapper
        view (View): View
    """
    # Register route for sending messages to the model_queue.
    message_router.register_route(
        condition=lambda m: m.type
        in (
            mes.Type.BUTTON,
            mes.Type.DATA,
        ),
        consumer=model_queue,
    )

    # Register route for sending messages to the message debouncer
    message_router.register_route(
        condition=lambda m: m.type == mes.Type.KEY, consumer=debouncer
    )

    # Debouncer sends messages to keymapper
    keymapper.listen(debouncer)
    # Tkroot and Keymapper send messages to message router
    message_router.listen(keymapper)
    message_router.listen(view.tkroot)


def register_model_message_routes(
    message_router: router.MessageRouter,
    view_queue: worker.QueueListener,
    model: Model,
):
    """
    Register 'Model' Message Routes.

    Application components communicate via messages and are connected
    using the 'Producer' and 'Consumer' protocols. This function registers
    those produce/consume relationships for messages coming from the Model.

    Args:
        message_router (router.MessageRouter): Message router
        view_queue (worker.QueueListener): Message queue
        model (Model): Model
    """
    # Register route for sending messages to the view_queue.
    message_router.register_route(
        condition=lambda m: m.type in (mes.Type.DATA,),
        consumer=view_queue,
    )

    # Message router listens to the Download manager.
    message_router.listen(model.download)


def make_workmanager() -> worker.WorkManager:
    """Create and Configure the workmanager.

    Creates two workers, one each for the model and view.

    Returns:
        WorkManager: Work Manager.
    """
    work_manager = worker.WorkManager()
    model_worker = worker.Worker(worker.WorkCycle(worker.QueueListener(), Handler()))
    view_worker = worker.Worker(worker.WorkCycle(worker.QueueListener(), Handler()))
    work_manager.add_worker(worker=model_worker, name="model")
    work_manager.add_worker(worker=view_worker, name="view")
    return work_manager


class Controller:
    """
    Controller.

    Constructs and contains the controller objects.
    """

    def __init__(self):
        """Construct Controller."""
        self.debouncer = debounce.MessageDebouncer()
        self.keymapper = KeyMapper(keybindings)
        self.model_message_router = router.MessageRouter()
        self.view_message_router = router.MessageRouter()
        self.work_manager = make_workmanager()


def make_controller(model: Model, view: View) -> Controller:
    """Construct and Configure the Controller.

    Creates the controller and configures messages routing and dispatching.

    Args:
        model (Model): Model
        view (View): View

    Returns:
        Controller: Controller
    """
    controller = Controller()

    register_model_callbacks(
        handler=controller.work_manager.get_handler("model"),
        model=model,
    )

    register_view_callbacks(
        handler=controller.work_manager.get_handler("view"), view=view
    )

    register_model_message_routes(
        message_router=controller.model_message_router,
        view_queue=controller.work_manager.get_queue("view"),
        model=model,
    )

    register_view_message_routes(
        message_router=controller.view_message_router,
        model_queue=controller.work_manager.get_queue("model"),
        debouncer=controller.debouncer,
        keymapper=controller.keymapper,
        view=view,
    )

    return controller
