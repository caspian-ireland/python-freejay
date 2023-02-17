"""
Rip audio files from youtube.
"""

import os
import logging
import typing
import queue
import threading
from tempfile import gettempdir
from urllib.error import HTTPError
from pytube import YouTube
from pytube.exceptions import VideoUnavailable, RegexMatchError
from freejay.messages import produce_consume as prodcon
import freejay.messages.messages as mes

logger = logging.getLogger(__name__)


def _check_video_available(filepath: str, video_link: str):
    """Check that video is available.

    pytube will sometimes silently fail, downloading a file with stem
    'Video Not Available'. This function raises a VideoUnavailable exception
    in this case.

    Issue raised here https://github.com/pytube/pytube/issues/1428

    Args:
        filepath (str): filepath of downloaded audio file.
        video_link (str): YouTube URL

    Raises:
        VideoUnavailable: If downloaded file has name stem == 'Video Not Available'
    """
    basename = os.path.basename(filepath)
    stem = os.path.splitext(basename)[0]

    if stem == "Video Not Available":
        raise VideoUnavailable(video_id=video_link)


def yt_rip(video_link: str, destination: str | None = None) -> str:
    """Rip audio from YouTube.

    Args:
        video_link (str): YouTube URL
        destination (str | None, optional): Target directory for download. If
            None (the default), will use `tempfile.gettempdir()`.

    Returns:
        str: Filepath to downloaded audio file.
    """
    if not destination:
        destination = gettempdir()
    try:
        logger.info("Downloading audio from %s", video_link)
        video = YouTube(video_link)
        audio = video.streams.get_audio_only()
        filepath = audio.download(output_path=destination)
        _check_video_available(filepath=filepath, video_link=video_link)
        logger.info("Download Completed!")
        return filepath

    except HTTPError:
        logger.error("HTTP Error for video_link '%s'", video_link, exc_info=True)
        raise
    except VideoUnavailable:
        logger.error(
            "Video unavailable, check the link for '%s'", video_link, exc_info=True
        )
        raise
    except RegexMatchError:
        logger.error(
            "Not recognised as a valid link: '%s'",
            video_link,
            exc_info=True,
        )
        raise


class DownloadManager(prodcon.Producer):
    """
    Download Manager.

    Download audio from YouTube, removing old downloads.
    """

    def __init__(
        self,
        source: mes.Source,
        component: mes.Component,
        destination: typing.Optional[str] = None,
    ):
        """Construct Download Manager.

        Args:
            destination (str, optional): Download directory. If None (the default),
            then a temporary directory is used.
        """
        if not destination:
            destination = gettempdir()

        if not os.path.exists(destination):
            logger.error("Directory does not exist.")
            raise FileNotFoundError("Directory does not exist.")

        self.destination = destination
        self.source = source
        self.component = component
        self.downloads: queue.Queue[str] = queue.Queue(3)
        self.current: typing.Optional[str] = None
        self.__lock = threading.Lock()

    def download(self, url: str):
        """Download a track from YouTube.

        Args:
            url (str): YouTube URL.
        """
        t = threading.Thread(target=self.__download_helper, args=(url,))
        t.start()

    def __download_helper(self, url: str):
        with self.__lock:

            try:
                file_path = yt_rip(video_link=url, destination=self.destination)
                self.current = file_path
                # Remove old tracks
                self.__cleanup(file_path)

                # Send message with file path of downloaded file.
                self.send_message(
                    self.make_message(
                        trigger=mes.Trigger.DATA_OUTPUT,
                        element=mes.Element.DOWNLOAD,
                        data={"status": "success", "file_path": self.current},
                    )
                )

            except (HTTPError, VideoUnavailable, RegexMatchError) as exc:
                # Send message with file path of downloaded file.
                self.send_message(
                    self.make_message(
                        trigger=mes.Trigger.EXCEPTION,
                        element=mes.Element.DOWNLOAD,
                        data={"status": "failed", "exception": exc},
                    )
                )

    def __cleanup(self, file_path: str):
        """Cleanup old files.

        Tries to add the latest file to the downloads queue. If the queue
        is full, pop items from the queue and delete corresponding file
        until file can be added.

        Args:
            file_path (str): File path of downloaded track.
        """
        try:
            self.downloads.put(file_path, block=False)
        except queue.Full:
            old_file = self.downloads.get()
            try:
                os.remove(old_file)
            except FileNotFoundError:
                pass
            self.__cleanup(file_path)

    def make_message(
        self, trigger: mes.Trigger, element: mes.Element, data: dict
    ) -> mes.Message:
        """Construct a message.

        Args:
            trigger (Trigger): Message trigger.
            element (Element): Message element.
            data (dict): Data

        Returns:
            Message: Message
        """
        msg = mes.Message(
            sender=mes.Sender(
                source=self.source,
                trigger=trigger,
            ),
            content=mes.Data(
                component=self.component,
                element=element,
                data=data,
            ),
        )
        return msg
