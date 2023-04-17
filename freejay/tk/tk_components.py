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

    Attributes:
        +keybindings_active(bool): Are keyboard shortcuts (keybindings) active.
    """

    def __init__(self):
        """Construct TKRoot Object."""
        ctk.CTk.__init__(self)
        self.keybindings_active = False


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
            parent: parent Tk widget.
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
        data: typing.Optional[typing.Dict] = None,
    ) -> None:
        """Construct and send 'Button' message.

        Args:
            component (mes.Component): Message component
            element (mes.Element): Message Element
            press_release (mes.PressRelease): Press/Release
            data (dict, optional): data to send, defaults to None.
        """
        if not data:
            data = {}

        msg = mes.Message(
            sender=mes.Sender(
                source=self.source,
                trigger=mes.Trigger.BUTTON,
            ),
            content=mes.Button(
                press_release=press_release,
                component=component,
                element=element,
                data=data,
            ),
        )
        self.send_message(msg)

    def entry_send(
        self,
        component: mes.Component,
        element: mes.Element,
        data: typing.Dict,
    ) -> None:
        """Construct and send 'Entry' message.

        Args:
            component (mes.Component): Message component
            element (mes.Element): Message Element
            data (typing.Dict): Data to send
        """
        msg = mes.Message(
            sender=mes.Sender(source=self.source, trigger=mes.Trigger.TEXT_ENTRY),
            content=mes.Data(
                component=component,
                element=element,
                data=data,
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
        data_press: typing.Optional[typing.Dict] = None,
        data_release: typing.Optional[typing.Dict] = None,
        text: typing.Optional[str] = None,
        image_path: typing.Optional[str] = None,
        **kwargs
    ) -> ctk.CTkButton:
        """
        Make a button.

        Helper method to initialise and render a button that sends messages.

        Args:
            parent: parent Tk widget
            row (int): grid row for button position
            column (int): grid column for button position
            component (mes.Component): message component
            element (mes.Element): message element
            data_press (dict, optional): Data to send on press.
                Defaults to None.
            data_release (dict, optional): Data to send on release.
                Defaults to None.
            text (typing.Optional[str], optional): Button text. Defaults to None.
            image_path (typing.Optional[str], optional): Path to button icon.
                Defaults to None.
            **kwargs: Named arguments to pass to CTkButton initialiser.

        Returns:
            ctk.CTkButton: Button widget
        """
        # Use image if supplied
        if image_path:
            image = Image.open(image_path).resize((20, 20), Image.LANCZOS)
            photo_image = ctk.CTkImage(image)
        else:
            photo_image = None

        # Create button and configure grid positioning
        btn = ctk.CTkButton(parent, image=photo_image, text=text, **kwargs)
        btn.grid(row=row, column=column, padx=10, pady=10)

        # Add press/release bindings
        btn.bind(
            "<ButtonPress-1>",
            lambda event: self.button_send(
                component=component,
                element=element,
                press_release=mes.PressRelease.PRESS,
                data=data_press,
            ),
        )
        btn.bind(
            "<ButtonRelease-1>",
            lambda event: self.button_send(
                component=component,
                element=element,
                press_release=mes.PressRelease.RELEASE,
                data=data_release,
            ),
        )
        return btn

    def make_entry(
        self,
        parent,
        component: mes.Component,
        element: mes.Element,
        data_callback: typing.Callable[[str], typing.Any],
        drop_focus: bool,
        placeholder_text: typing.Optional[str] = "",
        callback: typing.Optional[typing.Callable] = None,
    ) -> ctk.CTkEntry:
        """Make an Entry Widget.

        Args:
            parent (_type_): parent Tk widget
            component (mes.Component): message component
            element (mes.Element): message element
            data_callback (typing.Callable[[str], typing.Any]): data processing
                callback function. Converts output of ctk.CTkEntry.get() into
                desired format for Entry Message data attribute.
            drop_focus (bool): Drop Entry widget focus on hitting 'enter'.
            placeholder_text (typing.Optional[str], optional): Placeholder text
                to display in entry widget. Defaults to "".
            callback (typing.Optional[typing.Callable], optional): Function to
                call after Entry message sent. Useful for notifying user of status
                update. Defaults to None.

        Returns:
            ctk.CTkEntry: Entry widget.
        """
        entry = ctk.CTkEntry(parent, placeholder_text=placeholder_text)
        entry.bind(
            "<FocusIn>", lambda event: setattr(self.tkroot, "keybindings_active", False)
        )
        entry.bind(
            "<FocusOut>", lambda event: setattr(self.tkroot, "keybindings_active", True)
        )
        entry.bind("<Escape>", lambda event: self.tkroot.focus_set())

        # Add press/release bindings
        entry.bind(
            "<Return>",
            lambda event: self.entry_return_callback(
                component=component,
                element=element,
                data=data_callback(entry.get()),
                drop_focus=drop_focus,
                callback=callback,
            ),
        )

        return entry

    def entry_return_callback(
        self,
        component: mes.Component,
        element: mes.Element,
        data: typing.Any,
        drop_focus: bool,
        callback: typing.Optional[typing.Callable] = None,
    ) -> None:
        """Entry widget 'Return' callback.

        This function is called by the Entry widget when a user hits the return key.

        Args:
            component (mes.Component): message component.
            element (mes.Element): message element.
            data (typing.Any): message data.
            drop_focus (bool): drop entry focus on hitting return.
            callback (typing.Optional[typing.Callable]): Function to
                call after Entry message sent. Useful for notifying user of status
                update. Defaults to None.
        """
        self.entry_send(
            component=component,
            element=element,
            data=data,
        )
        if drop_focus:
            self.tkroot.focus_set()

        if callback:
            callback()


class TkMain(TkComponent):
    """
    Main application frame.

    Keybindings are registered here.
    """

    def __init__(
        self,
        tkroot: TkRoot,
        parent: typing.Any,
        source: mes.Source,
    ):
        """Construct TkMain.

        Args:
            tkroot (TkRoot): Top-level Tk widget.
            parent (any): Parent Tk widget.
            source (mes.Source): Source to use for messages.
        """
        super().__init__(tkroot=tkroot, parent=parent, source=source)
        self.frame = ctk.CTkFrame(self.parent)

        self.tkroot.bind(
            "<KeyPress>",
            lambda event: self.key_event_cb(
                press_release=mes.PressRelease.PRESS, tkevent=event
            ),
        )
        self.tkroot.bind(
            "<KeyRelease>",
            lambda event: self.key_event_cb(
                press_release=mes.PressRelease.RELEASE, tkevent=event
            ),
        )

    def key_event_cb(self, press_release: mes.PressRelease, tkevent: tk.Event) -> None:
        """Key Event Callback.

        Function called on key event. If keybindings are active, then key message
        is sent.

        Args:
            press_release (mes.PressRelease): Is key pressed or released.
            tkevent (tk.Event): Tk keypress event object.
        """
        if self.tkroot.keybindings_active:
            self.key_send(press_release=press_release, tkevent=tkevent)
