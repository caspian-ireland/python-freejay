"""Tkinter app components."""

import typing
import tkinter as tk
import customtkinter as ctk
from freejay.messages import messages as mes
from freejay.messages import produce_consume as prodcon
from PIL import Image


class TkRoot(ctk.CTk, prodcon.Producer):
    """
    Tkinter app root.

    Extends the Tk toplevel widget with the producer interface.
    """

    pass


class TkComponent:
    """
    Tkinter app component.

    Intended to be extended by child classes, TkComponent provides functionality
    to create and send messages.

    The top level Tk widget (TkRoot) is registered at initialisation,
    which handles all messags dispatch.

    Currently supported message types:
        * Button
        * Key

    See methods docs for more details.
    """

    def __init__(self, tkroot: TkRoot, parent: typing.Any, source: mes.Source):
        """Construct TkComponent.

        Args:
            tkroot (TkRoot): Top level Tk widget.
            source (mes.Source): TkComponent message source.
        """
        self.tkroot = tkroot
        self.parent = parent
        self.source = source

    def button_send(
        self,
        component: mes.Component,
        element: mes.Element,
        press_release: mes.PressRelease,
    ) -> None:
        """Construct and send 'Button' message.

        Args:
            component (mes.Component): Message component
            element (mes.Element): Message Element
            press_release (mes.PressRelease): Press/Release
        """
        msg = mes.Message(
            sender=mes.Sender(
                source=self.source,
                trigger=mes.Trigger.BUTTON,
            ),
            content=mes.Button(
                press_release=press_release, component=component, element=element
            ),
        )
        self.send_message(msg)

    def key_send(self, press_release: mes.PressRelease, tkevent: tk.Event) -> None:
        """Construct and send 'Key' message.

        Args:
            press_release (mes.PressRelease): Press/Release
            tkevent (tk.Event): Key event generated by Tkinter.
        """
        msg = mes.Message(
            sender=mes.Sender(
                source=self.source,
                trigger=mes.Trigger.KEY,
            ),
            content=mes.Key(press_release=press_release, sym=tkevent.keysym),
        )
        self.send_message(msg)

    def value_button_send(
        self,
        component: mes.Component,
        element: mes.Element,
        press_release: mes.PressRelease,
        value: typing.Optional[typing.Union[bool, str, int, float]],
    ) -> None:
        """Construct and send 'ValueButton' message.

        Args:
            component (mes.Component): Message component
            element (mes.Element): Message Element
            press_release (mes.PressRelease): Press/Release
            value (str|int|float|bool): Value for button (optional).
        """
        msg = mes.Message(
            sender=mes.Sender(
                source=self.source,
                trigger=mes.Trigger.BUTTON,
            ),
            content=mes.ValueButton(
                press_release=press_release,
                component=component,
                element=element,
                value=value,
            ),
        )
        self.send_message(msg)

    def send_message(self, msg: mes.Message):
        """Send a message.

        Message is sent from the top level Tk widget.
        Args:
            msg (mes.Message): Message to send.
        """
        self.tkroot.send_message(msg)

    def make_button(
        self,
        parent,
        row: int,
        column: int,
        component: mes.Component,
        element: mes.Element,
        text: typing.Optional[str] = None,
        image_path: typing.Optional[str] = None,
        **kwargs
    ) -> ctk.CTkButton:

        if image_path:
            image = Image.open(image_path).resize((20, 20), Image.LANCZOS)
            photo_image = ctk.CTkImage(image)
        else:
            photo_image = None

        btn = ctk.CTkButton(parent, image=photo_image, text=text, **kwargs)
        btn.grid(row=row, column=column, padx=10, pady=10)
        btn.bind(
            "<ButtonPress-1>",
            lambda event: self.button_send(
                component=component,
                element=element,
                press_release=mes.PressRelease.PRESS,
            ),
        )
        btn.bind(
            "<ButtonRelease-1>",
            lambda event: self.button_send(
                component=component,
                element=element,
                press_release=mes.PressRelease.RELEASE,
            ),
        )
        return btn

    def make_value_button(
        self,
        parent,
        row: int,
        column: int,
        component: mes.Component,
        element: mes.Element,
        value_press: typing.Optional[typing.Union[bool, str, int, float]] = None,
        value_release: typing.Optional[typing.Union[bool, str, int, float]] = None,
        text: typing.Optional[str] = None,
        image_path: typing.Optional[str] = None,
        **kwargs
    ) -> ctk.CTkButton:

        if image_path:
            image = Image.open(image_path).resize((20, 20), Image.LANCZOS)
            photo_image = ctk.CTkImage(image)
        else:
            photo_image = None

        btn = ctk.CTkButton(parent, text=text, image=photo_image, **kwargs)
        btn.grid(row=row, column=column, padx=10, pady=10)
        btn.bind(
            "<ButtonPress-1>",
            lambda event: self.value_button_send(
                component=component,
                element=element,
                press_release=mes.PressRelease.PRESS,
                value=value_press,
            ),
        )
        btn.bind(
            "<ButtonRelease-1>",
            lambda event: self.value_button_send(
                component=component,
                element=element,
                press_release=mes.PressRelease.RELEASE,
                value=value_release,
            ),
        )

        return btn
