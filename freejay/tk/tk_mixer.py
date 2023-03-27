"""Tkinter components for mixer View."""

import typing
import tkinter as tk
import customtkinter as ctk
from freejay.messages import messages as mes
from .tk_components import TkComponent, TkRoot


class TkCrossfader(TkComponent):
    """Tk widget for the crossfader."""

    def __init__(
        self,
        tkroot: TkRoot,
        parent: typing.Any,
        source: mes.Source,
        component: mes.Component,
    ):
        """Construct Crossfader Tk widget.

        Args:
            tkroot (TkRoot): toot tk widget
            parent (typing.Any): parent Tk widget
            source (mes.Source): source used for messages.
            component (mes.Component): component used for messages.
        """
        super().__init__(tkroot=tkroot, parent=parent, source=source)
        self.component = component
        self.__position = 0.5

        # Configure Tk frame
        self.frame = ctk.CTkFrame(parent)
        self.frame.grid_rowconfigure((0), weight=1)
        self.frame.grid_columnconfigure((0), weight=1)
        self.frame.grid(padx=15, pady=15)

        # Slider for controlling crossfader
        self.crossfader_slider = ctk.CTkSlider(
            master=self.frame,
            progress_color="transparent",
            from_=0,
            to=1,
            command=self.slider_cb,
            number_of_steps=50,
        )

        # Arrange Tk elements
        self.crossfader_slider.grid(
            row=0, column=0, padx=5, pady=5, sticky=(tk.E, tk.W)
        )

    @property
    def position(self) -> float:
        """Get the position."""
        return self.__position

    @position.setter
    def position(self, value: float):
        """Set the position.

        When the position has changed value, a message is sent to the controller.

        Args:
            value (float): xfader position.
        """
        if value != self.__position:
            self.__position = value
            self.send_message(self.make_message(value))

    def slider_cb(self, value: float):
        """Slider Callback.

        Helper function to facilitate updating the position
        on callback from the Tk slider widget.

        Args:
            value (float): xfader position.
        """
        self.position = value

    def make_message(self, value: float) -> mes.Message[mes.Data]:
        """Construct a message to send to the controller.

        Args:
            value (float): xfader position.

        Returns:
            mes.Message[mes.Data]: Data Message to send.
        """
        msg = mes.Message(
            sender=mes.Sender(source=self.source, trigger=mes.Trigger.SLIDER),
            content=mes.Data(
                component=self.component,
                element=mes.Element.CROSSFADER,
                data={"position": value},
            ),
        )
        return msg
