"""
Player callback functions.

Callback functions are registered with the message handler. The handler
will check the content of incoming messages and call the appropriate callback,
changing the state of the audio player as required.
"""

import typing
import logging
from freejay.audio_download import ytrip
from freejay.message_dispatcher import handler_cb
from freejay.message_dispatcher import handler
from freejay.messages import messages as mes


logger = logging.getLogger(__name__)


def make_download_callback(
    download_manager: ytrip.DownloadManager,
) -> typing.Callable[[mes.Message[mes.Button]], None]:

    callback = handler_cb.make_button_cb(press_cb=download_manager.download)
    return callback


def register_download_cb(
    handler: handler.Handler,
    download_manager: ytrip.DownloadManager,
):

    handler.register_handler(
        callback=make_download_callback(download_manager),
        component=mes.Component.DOWNLOAD,
        element=mes.Element.DOWNLOAD,
    )
