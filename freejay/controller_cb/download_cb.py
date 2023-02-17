"""
Downloader callback functions.

Callback functions are registered with the message handler. The handler
will check the content of incoming messages and call the appropriate callback.

In the case of the downloader, the view can send a message containing a YouTube
URL to rip. The model will send a message containing the file path of the downloaded
file.
"""

import typing
import logging
from freejay.audio_download import ytrip
from freejay.controller_cb import factories
from freejay.message_dispatcher import handler
from freejay.messages import messages as mes
from freejay.tk import tk_download


logger = logging.getLogger(__name__)


def make_download_model_callback(
    download_manager: ytrip.DownloadManager,
) -> typing.Callable[[mes.Message[mes.Button]], None]:
    """Make callback function for download model.

    Args:
        download_manager (DownloadManager): Download manager.

    Returns:
        typing.Callable[[mes.Message[mes.Button]], None]: Callback function.
    """
    callback = factories.make_button_cb(press_cb=download_manager.download)
    return callback


def register_download_model_cb(
    handler: handler.Handler, download_manager: ytrip.DownloadManager
):
    """Register download model callbacks.

    Args:
        handler (Handler): Message handler.
        download_manager (DownloadManager): Download manager.
    """
    handler.register_handler(
        callback=make_download_model_callback(download_manager),
        component=mes.Component.DOWNLOAD,
        element=mes.Element.DOWNLOAD,
    )


def make_download_view_callback(
    download_view: tk_download.TkDownload,
):
    """Make callback function for download view.

    Args:
        download_view (TkDownload): Download view.

    Returns:
        typing.Callable[[mes.Message[mes.Data]], None]: Callback function.
    """

    def callback(message: mes.Message[mes.Data]):
        if message.content.data["status"] == "success":
            file_path = message.content.data["file_path"]
            download_view.file_path = file_path
        elif message.content.data["status"] == "failed":
            # exception = message.content.data["exception"]
            download_view.label_var.set(
                "An error occurred. Please check the URL and try again."
            )

    return callback


def register_download_view_cb(
    handler: handler.Handler,
    download_view: tk_download.TkDownload,
):
    """Register download view callbacks.

    Args:
        handler (Handler): Message handler.
        download_view (TkDownload): Download view.
    """
    handler.register_handler(
        callback=make_download_view_callback(download_view),
        component=mes.Component.DOWNLOAD,
        element=mes.Element.DOWNLOAD,
    )
