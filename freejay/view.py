"""Application View."""

import customtkinter as ctk
from freejay.tk import tk_components
from freejay.tk import tk_player
from freejay.tk import tk_download
from freejay.tk import tk_mixer
from freejay.messages import messages as mes


class View:
    """
    View.

    Constructs and contains the view objects.
    """

    def __init__(self):
        """Construct View."""
        self.tkroot = tk_components.TkRoot()
        self.tkmain = tk_components.TkMain(
            self.tkroot, parent=self.tkroot, source=mes.Source.MAIN_WINDOW
        )

        self.left_deck = tk_player.TkDeck(
            tkroot=self.tkroot,
            parent=self.tkmain.frame,
            source=mes.Source.PLAYER_VIEW,
            component=mes.Component.LEFT_DECK,
        )
        self.right_deck = tk_player.TkDeck(
            tkroot=self.tkroot,
            parent=self.tkmain.frame,
            source=mes.Source.PLAYER_VIEW,
            component=mes.Component.RIGHT_DECK,
        )

        self.mixer = tk_mixer.TkCrossfader(
            tkroot=self.tkroot,
            parent=self.tkmain.frame,
            source=mes.Source.MIXER,
            component=mes.Component.MIXER,
        )

        self.download = tk_download.TkDownload(
            tkroot=self.tkroot,
            parent=self.tkmain.frame,
            source=mes.Source.DOWNLOAD_VIEW,
            component=mes.Component.DOWNLOAD,
        )


def make_view() -> View:
    """
    Construct and Configure the View.

    Returns:
        View: View
    """
    # CTk settings
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    # Create View
    view = View()

    # Configure layout
    view.tkroot.geometry("1200x300")
    view.tkroot.grid_rowconfigure(0, weight=1)
    view.tkroot.grid_columnconfigure(0, weight=1)
    view.tkmain.frame.grid(row=0, column=0)
    view.tkmain.frame.grid_rowconfigure((0, 1, 2), weight=1)
    view.tkmain.frame.grid_columnconfigure((0, 1), weight=1)
    view.download.frame.grid(row=0, column=0, columnspan=2, sticky="ew")
    view.left_deck.frame.grid(row=1, column=0, sticky="w")
    view.right_deck.frame.grid(row=1, column=1, sticky="e")
    view.mixer.frame.grid(row=2, column=0, columnspan=2)

    return view
