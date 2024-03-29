"""Tkinter components for youtube downloader."""

import typing
import tkinter as tk
import customtkinter as ctk
from freejay.messages import messages as mes
from .tk_components import TkComponent, TkRoot
import pathlib


class TkDownload(TkComponent):
    """
    Download View.

    Has a search bar, download button and label to show the
    name of the most recently downloaded track.
    """

    def __init__(
        self,
        tkroot: TkRoot,
        parent: typing.Any,
        source: mes.Source,
        component: mes.Component,
    ):
        """Construct TkDownload.

        Args:
            tkroot (TkRoot): Top-level Tk widget.
            parent: Parent Tk widget.
            source (mes.Source): Message source.
            component (mes.Component): Message Component.
        """
        super().__init__(tkroot=tkroot, parent=parent, source=source)
        self.component = component

        # Configure Tk frame
        self.frame = ctk.CTkFrame(parent)
        self.frame.grid_rowconfigure((0, 1), weight=1)
        self.frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
        self.frame.grid(padx=15, pady=15)

        # Create attributes to store file info
        self.__file_path = ""
        self.__file_name = ""

        # Tk elements
        # Store the file name label
        self.label_var = ctk.StringVar(master=self.frame, value="")

        # Make download entry widget
        self.download_entry = self.make_entry(
            parent=self.frame,
            component=self.component,
            element=mes.Element.DOWNLOAD,
            data_callback=lambda value: {"url": value},
            drop_focus=True,
            placeholder_text="Enter URL",
            callback=lambda: self.label_var.set("Downloading..."),
        )

        # Download Button
        self.download_btn = ctk.CTkButton(
            master=self.frame, text="download", command=self.download_cb
        )

        # Display file name
        self.file_name_lbl = ctk.CTkLabel(
            master=self.frame, textvariable=self.label_var
        )

        # Arrange Tk elements
        self.download_entry.grid(
            row=0, column=0, columnspan=4, padx=5, pady=5, sticky=(tk.E, tk.W)
        )
        self.download_btn.grid(row=0, column=4, padx=5, pady=5, sticky=(tk.E, tk.W))
        self.file_name_lbl.grid(
            row=1, column=0, columnspan=5, padx=5, pady=5, sticky=(tk.E, tk.W)
        )

    @property
    def file_path(self):
        """Get the file path of last downloaded file."""
        return self.__file_path

    @file_path.setter
    def file_path(self, value):
        """Set the file path of last downloaded file."""
        self.__file_path = value
        self.__file_name = pathlib.Path(value).stem
        self.label_var.set(f"Track ready: {self.__file_name}")

    def download_cb(self):
        """Download callback."""
        self.entry_send(
            component=self.component,
            element=mes.Element.DOWNLOAD,
            data={"url": self.download_entry.get()},
        )
        self.tkroot.focus_set()
        self.label_var.set("Downloading...")
