"""
Rip audio files from youtube
"""

import logging
from tempfile import gettempdir
from urllib.error import HTTPError
from pytube import YouTube
from pytube.exceptions import VideoUnavailable

logger = logging.getLogger(__name__)


def yt_rip(video_link: str, destination: str | None = None) -> str:
    """Rip audio from YouTube

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
