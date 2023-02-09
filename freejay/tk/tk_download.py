import typing
import os
import time
import tkinter as tk
import customtkinter as ctk
from freejay.messages import messages as mes
from .tk_components import TkComponent, TkRoot
from freejay.audio_download import ytrip


class TkDownload(TkComponent):
    def __init__(
        self,
        tkroot: TkRoot,
        parent: typing.Any,
    ):

        super().__init__(tkroot=tkroot, parent=parent, source=mes.Source.DOWNLOAD)
        self.component = mes.Component.DOWNLOAD
        self.frame = ctk.CTkFrame(parent)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        self.download_entry = ctk.CTkEntry(
            master=self.frame, placeholder_text="Enter URL"
        )

        self.download_btn = ctk.CTkButton(
            master=self.frame, text="download", command=self.download_cb
        )

        self.download_entry.grid(row=0, column=0, columnspan=4, sticky=(tk.E, tk.W))
        self.download_btn.grid(row=0, column=4, sticky=(tk.E, tk.W))

    def download_cb(self):
        self.button_send(
            component=self.component,
            element=mes.Element.DOWNLOAD,
            press_release=mes.PressRelease.PRESS,
            data={"url": self.download_entry.get()},
        )


if __name__ == "__main__":

    from ..messages.produce_consume import Consumer
    from ..message_dispatcher.handler import Handler
    from ..audio_download.download_cb import register_download_cb
    from ..audio_download.ytrip import DownloadManager

    handler = Handler()
    download_manager = DownloadManager("instance")

    register_download_cb(handler, download_manager)

    class Listener(Consumer):
        def on_message_recieved(self, message):
            handler(message)

    tkroot = TkRoot()
    tkroot.grid_columnconfigure(0, weight=1)
    tkdownload = TkDownload(tkroot=tkroot, parent=tkroot)

    tkdownload.frame.grid(row=0, column=0, padx=30, pady=30, sticky=(tk.E, tk.W))

    listen = Listener()
    listen.listen(tkroot)
    tkroot.mainloop()
