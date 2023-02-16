"""Create Application."""

import logging
from .view import make_view
from .model import make_model
from .controller import make_controller


logger = logging.getLogger(__name__)


class App:
    """
    Main Application Class.

    Initialise model, view and controller.
    """

    def __init__(self):
        """Construct App."""
        self.view = make_view()
        self.model = make_model()
        self.controller = make_controller(model=self.model, view=self.view)

    def start(self):
        """Start App."""
        self.controller.work_manager.start()
        self.view.tkroot.mainloop()


def make_app():
    """
    Configure and start the application.
    """
    app = App()
    app.start()
