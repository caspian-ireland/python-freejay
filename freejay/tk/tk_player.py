"""Tkinter components for player (deck)."""

import typing
import os
import customtkinter as ctk
from freejay.messages import messages as mes
from .tk_components import TkComponent, TkRoot


class TkDeckPlayControls(TkComponent):
    """Deck playback control frame."""

    def __init__(
        self,
        tkroot: TkRoot,
        parent: typing.Any,
        source: mes.Source,
        component: mes.Component,
    ):
        """Construct TkDeckPlayControls.

        Note: this is intended to be created by TkDeck.

        Args:
            tkroot (TkRoot): Top-level Tk widget.
            parent: Parent Tk widget.
            source (mes.Source): Message source.
            component (mes.Component): Message Component (LEFT_DECK or RIGHT_DECK)
        """
        super().__init__(tkroot=tkroot, parent=parent, source=source)
        self.component = component
        self.frame = ctk.CTkFrame(parent)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(tuple([i for i in range(7)]), weight=1)
        self.frame.grid(padx=30, pady=15)

        self.cue_btn = self.make_button(
            parent=self.frame,
            row=0,
            column=0,
            component=self.component,
            element=mes.Element.CUE,
            text="CUE",
            text_color="black",
        )

        self.play_btn = self.make_button(
            parent=self.frame,
            row=0,
            column=1,
            component=self.component,
            element=mes.Element.PLAY_PAUSE,
            image_path=os.path.join("assets", "icons", "icons8-play-96.png"),
        )

        self.jog_backward_large_valbtn = self.make_button(
            parent=self.frame,
            row=0,
            column=2,
            component=self.component,
            element=mes.Element.JOG,
            data_press={"value": -2},
            image_path=os.path.join("assets", "icons", "icons8-rewind-96.png"),
        )

        self.jog_backward_small_valbtn = self.make_button(
            parent=self.frame,
            row=0,
            column=3,
            component=self.component,
            element=mes.Element.JOG,
            data_press={"value": -0.1},
            image_path=os.path.join(
                "assets", "icons", "icons8-resume-button-96-rotated.png"
            ),
        )

        self.jog_forward_small_valbtn = self.make_button(
            parent=self.frame,
            row=0,
            column=4,
            component=self.component,
            element=mes.Element.JOG,
            data_press={"value": 0.1},
            image_path=os.path.join("assets", "icons", "icons8-resume-button-96.png"),
        )

        self.jog_forward_large_valbtn = self.make_button(
            parent=self.frame,
            row=0,
            column=5,
            component=self.component,
            element=mes.Element.JOG,
            data_press={"value": 2},
            image_path=os.path.join("assets", "icons", "icons8-fast-forward-96.png"),
        )

        self.stop_btn = self.make_button(
            parent=self.frame,
            row=0,
            column=6,
            component=self.component,
            element=mes.Element.STOP,
            image_path=os.path.join("assets", "icons", "icons8-stop-96.png"),
        )


class TkDeckPitchControls(TkComponent):
    """Deck pitch controls frame."""

    def __init__(
        self,
        tkroot: TkRoot,
        parent: typing.Any,
        source: mes.Source,
        component: mes.Component,
    ):
        """Construct TkDeckPitchControls.

        Note: this is intended to be created by TkDeck.

        Args:
            tkroot (TkRoot): Top-level Tk widget.
            parent: Parent Tk widget.
            source (mes.Source): Message source.
            component (mes.Component): Message Component (LEFT_DECK or RIGHT_DECK)
        """
        super().__init__(tkroot=tkroot, parent=parent, source=source)
        self.component = component
        self.frame = ctk.CTkFrame(parent)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure((0, 1), weight=1)
        self.frame.grid(padx=30, pady=15)

        self.nudge_backward_valbtn = self.make_button(
            parent=self.frame,
            row=0,
            column=0,
            component=self.component,
            element=mes.Element.NUDGE,
            data_press={"value": -0.05},
            image_path=os.path.join(
                "assets", "icons", "icons8-resume-button-96-rotated.png"
            ),
        )

        self.nudge_forward_valbtn = self.make_button(
            parent=self.frame,
            row=0,
            column=1,
            component=self.component,
            element=mes.Element.NUDGE,
            data_press={"value": 0.05},
            image_path=os.path.join("assets", "icons", "icons8-resume-button-96.png"),
        )


class TkDeckFileControls(TkComponent):
    """
    Deck file controls frame.

    Currently a simple 'load' button to load the most recently downloaded track.
    """

    def __init__(
        self,
        tkroot: TkRoot,
        parent: typing.Any,
        source: mes.Source,
        component: mes.Component,
    ):
        """Construct TkDeckFileControls.

        Note: this is intended to be created by TkDeck.

        Args:
            tkroot (TkRoot): Top-level Tk widget.
            parent: Parent Tk widget.
            source (mes.Source): Message source.
            component (mes.Component): Message Component (LEFT_DECK or RIGHT_DECK)
        """
        super().__init__(tkroot=tkroot, parent=parent, source=source)
        self.component = component
        self.frame = ctk.CTkFrame(parent)
        self.frame.grid_rowconfigure((0, 1), weight=1)
        self.frame.grid_columnconfigure((0, 1), weight=1)
        self.frame.grid(padx=10, pady=10)

        self.load_btn = self.make_button(
            parent=self.frame,
            row=0,
            column=1,
            component=self.component,
            element=mes.Element.LOAD,
            image_path=os.path.join("assets", "icons", "icons8-insert-96.png"),
        )


class TkDeck(TkComponent):
    """Deck (player) frame."""

    def __init__(
        self,
        tkroot: TkRoot,
        parent: typing.Any,
        source: mes.Source,
        component: mes.Component,
    ):
        """Construct TkDeck.

        Args:
            tkroot (TkRoot): Top-level Tk widget.
            parent: Parent Tk widget.
            source (mes.Source): Message source.
            component (mes.Component): Message Component (LEFT_DECK or RIGHT_DECK)
        """
        super().__init__(tkroot=tkroot, parent=parent, source=source)
        self.component = component
        self.frame = ctk.CTkFrame(parent)
        self.frame.grid_rowconfigure((0, 1), weight=1)
        self.frame.grid_columnconfigure((0, 1), weight=1)
        self.frame.grid(padx=15, pady=15)
        self.play_controls = TkDeckPlayControls(
            tkroot=tkroot, parent=self.frame, source=source, component=component
        )
        self.pitch_controls = TkDeckPitchControls(
            tkroot=tkroot, parent=self.frame, source=source, component=component
        )
        self.file_controls = TkDeckFileControls(
            tkroot=tkroot, parent=self.frame, source=source, component=component
        )

        self.play_controls.frame.grid(row=1, column=0, columnspan=2, sticky="W")
        self.pitch_controls.frame.grid(row=0, column=0, sticky="W")
        self.file_controls.frame.grid(row=0, column=1, sticky="ew")
