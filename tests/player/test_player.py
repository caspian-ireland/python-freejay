import pytest
import freejay.player.player
import mpv
import logging


@pytest.fixture
def check_file_loaded_f():
    class TestObj:
        def __init__(self):
            self.loaded = True

        @freejay.player.player._check_file_loaded
        def test_method(self):
            return True

    test_obj = TestObj()
    return test_obj


@pytest.fixture
def mpv_f(mocker):
    mocker.patch("mpv.MPV", autospec=True)
    player = mpv.MPV()
    player.path = "some_path"
    return player


def test_check_file_loaded_success(check_file_loaded_f):
    check_file_loaded_f.loaded = True
    assert check_file_loaded_f.test_method() is True


def test_check_file_loaded_fail(check_file_loaded_f):
    check_file_loaded_f.loaded = False
    with pytest.raises(freejay.player.player.FileNotLoaded) as e_info:
        check_file_loaded_f.test_method()


@pytest.mark.parametrize(
    "level,expected",
    [
        ("trace", "DEBUG"),
        ("debug", "DEBUG"),
        ("info", "INFO"),
        ("warn", "WARNING"),
        ("error", "ERROR"),
        ("fatal", "CRITICAL"),
        ("unknown", "ERROR"),
    ],
)
def test_log_handler(level, expected, caplog):
    caplog.set_level(logging.DEBUG)
    freejay.player.player.mpv_log_handler(
        loglevel=level, component="some_comp", message="some_message"
    )
    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == expected
    assert "MPV-some_comp: some_message" in caplog.text


def test_load_success(mpv_f, mock_mp4):
    mpv_f.path = mock_mp4
    playermpv = freejay.player.player.PlayerMpv(mpv_f)
    playermpv.load(mock_mp4)
    mpv_f.play.assert_called_once()
    assert mpv_f.pause is True


def test_load_fail(mpv_f, mock_mp4):
    mpv_f.path = None
    playermpv = freejay.player.player.PlayerMpv(mpv_f)

    with pytest.raises(freejay.player.player.LoadError) as e_info:
        playermpv.load(mock_mp4)


def test_load_file_not_found(mpv_f):
    mpv_f.path = "some_path_not_exists.mp4"
    playermpv = freejay.player.player.PlayerMpv(mpv_f)
    with pytest.raises(FileNotFoundError) as e_info:
        playermpv.load("some_path_not_exists.mp4")


def test_play_pause(mpv_f):
    playermpv = freejay.player.player.PlayerMpv(mpv_f)
    mpv_f.pause = None
    playermpv.play()
    assert mpv_f.pause is False
    playermpv.pause()
    assert mpv_f.pause is True


def test_seek_calls(mpv_f):
    playermpv = freejay.player.player.PlayerMpv(mpv_f)
    playermpv.seek(value=10)
    mpv_f.seek.assert_called_with(amount=10, reference="absolute")


@pytest.mark.parametrize(
    "input", ["absolute", "relative", pytest.param("mistake", marks=pytest.mark.xfail)]
)
def test_seek_reference_vals(mpv_f, input):
    playermpv = freejay.player.player.PlayerMpv(mpv_f)
    playermpv.seek(value=10, reference=input)


def test_set_speed(mpv_f):
    playermpv = freejay.player.player.PlayerMpv(mpv_f)
    mpv_f.speed = 1.2
    assert playermpv.speed == 1.2
    playermpv.speed = 0.9
    assert mpv_f.speed == 0.9


def test_set_volume(mpv_f):
    playermpv = freejay.player.player.PlayerMpv(mpv_f)
    mpv_f.volume = 100
    assert playermpv.volume == 100
    playermpv.volume = 50
    assert mpv_f.volume == 50
