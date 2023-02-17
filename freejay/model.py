"""Application Model."""

import logging
import mpv
import typing
from freejay.player.djplayer import DJPlayer
from freejay.player.player import PlayerMpv
from freejay.audio_download.ytrip import DownloadManager
from freejay.messages import messages as mes

logger = logging.getLogger(__name__)


class Model:
    """Model.

    Constructs and contains the model objects.
    """

    def __init__(self, dir: typing.Optional[str] = None):
        """
        Construct Model.

        Args:
            dir (str, optional): Directory to use for application files.
        """
        self.left_deck = DJPlayer(player=PlayerMpv(mpv.MPV()))
        self.right_deck = DJPlayer(player=PlayerMpv(mpv.MPV()))
        self.download = DownloadManager(
            destination=dir,
            source=mes.Source.DOWNLOAD_MODEL,
            component=mes.Component.DOWNLOAD,
        )


def make_model() -> Model:
    """Construct and Configure Model.

    Returns:
        Model
    """
    model = Model(dir="instance")
    return model
