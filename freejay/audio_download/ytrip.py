"""
Rip audio files from youtube.
"""

import os
import logging
from tempfile import gettempdir
from urllib.error import HTTPError
from pytube import YouTube
from pytube.exceptions import VideoUnavailable

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
