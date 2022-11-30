import pytest
from unittest import mock
import freejay.ytrip


def test_yt_rip_calls(mocker):
    """Test yt_rip() makes expected pytest method calls."""
    video_link = "https://www.youtube.com/watch?v=myfavetrack"
    destination = "some_destination"
    m_YouTube_c = mocker.patch("freejay.ytrip.YouTube", autospec=True)
    freejay.ytrip.yt_rip(video_link, destination=destination)
    m_YouTube_c.assert_has_calls(
        [
            mock.call(video_link),
            mock.call().streams.get_audio_only(),
            mock.call().streams.get_audio_only().download(output_path=destination),
        ]
    )


def test_vid_unav_raises():
    with pytest.raises(freejay.ytrip.VideoUnavailable) as e_info:
        freejay.ytrip._check_video_available(
            filepath="Video Not Available.mp4",
            video_link="https://www.youtube.com/watch?v=myfavetrack",
        )


def test_vid_unav_passes():
    try:
        freejay.ytrip._check_video_available(
            filepath="My Favourite Track.mp4",
            video_link="https://www.youtube.com/watch?v=myfavetrack",
        )
    except freejay.ytrip.VideoUnavailable as exc:
        assert False, f"'_check_video_available raised an exception {exc}"
