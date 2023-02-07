import pytest
from freejay.player.player import IPlayer
from freejay.player.djplayer import DJPlayer
from unittest import mock


@pytest.fixture
def player_f(mocker):
    mocker.patch("tests.player.test_djplayer.IPlayer", autospec=True)
    player = IPlayer(mock.Mock())
    player.playing = False
    return player


@pytest.fixture
def loaded_player_f(mocker, mock_mp4):
    mocker.patch("tests.player.test_djplayer.IPlayer", autospec=True)
    player = IPlayer(mock.Mock())
    player.playing = False
    djplayer = DJPlayer(player)
    djplayer.load(filename=mock_mp4)
    return player, djplayer


def test_load_success(player_f, mock_mp4):
    djplayer = DJPlayer(player_f)
    djplayer.load(filename=mock_mp4)
    player_f.load.assert_called_once()


def test_not_load_while_playing(player_f, mock_mp4, caplog):
    djplayer = DJPlayer(player_f)
    player_f.playing = True
    djplayer.load(filename=mock_mp4)
    player_f.load.assert_not_called()
    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == "WARNING"
    assert "Track is still playing!" in caplog.text


def test_load_updates_filename(player_f, mock_mp4, caplog):
    djplayer = DJPlayer(player_f)
    before = djplayer.filename
    djplayer.load(filename=mock_mp4)
    after = djplayer.filename
    assert before != after
    assert after == mock_mp4


def test_play_pause(loaded_player_f):
    player, djplayer = loaded_player_f
    player.playing = False
    player.play.assert_not_called()
    player.pause.assert_not_called()
    djplayer.play_pause()
    player.playing = True
    player.play.assert_called_once()
    player.pause.assert_not_called()
    djplayer.play_pause()
    player.play.assert_called_once()
    player.pause.assert_called_once()


def test_cue_stops_if_playing(loaded_player_f):
    player, djplayer = loaded_player_f
    djplayer.play_pause()
    djplayer.cue_press()
    djplayer.cue_release()
    calls = player.mock_calls
    calls = [i for i in reversed(calls)]
    assert mock.call.play() in calls and mock.call.pause() in calls
    assert calls.index(mock.call.pause()) < calls.index(mock.call.play())


def test_cue_plays_if_not_playing(loaded_player_f):
    player, djplayer = loaded_player_f
    djplayer.cue_press()
    player.play.assert_called_once()
    player.pause.assert_not_called()


def test_cue_stops_on_release(loaded_player_f):
    player, djplayer = loaded_player_f
    player.playing = True
    djplayer.cue_release()
    player.play.assert_not_called()
    player.pause.assert_called_once()


def test_sets_cue_point_if_not_playing(loaded_player_f):
    player, djplayer = loaded_player_f
    player.playing = False
    player.time_pos = 20
    djplayer.cue_press()
    djplayer.cue_release()
    assert djplayer.time_cue == 20


def test_cue_returns_to_cuepoint_if_playing(loaded_player_f):
    player, djplayer = loaded_player_f
    player.playing = False
    player.time_pos = 20
    djplayer.cue_press()
    djplayer.cue_release()
    player.time_pos = 40
    player.playing = True
    djplayer.cue_press()
    djplayer.cue_release()
    player.seek.assert_called_with(value=20, reference="absolute")
    assert player.seek.call_count == 2


def test_play_pause_during_cue_continues(loaded_player_f):
    player, djplayer = loaded_player_f
    player.playing = False
    djplayer.cue_press()
    player.playing = True
    djplayer.play_pause()
    djplayer.cue_release()
    player.play.assert_called()
    player.pause.assert_not_called()


def test_stop_stops_and_returns_to_start(loaded_player_f):
    player, djplayer = loaded_player_f
    player.playing = True
    player.time_start = 0
    player.time_pos = 20
    djplayer.stop()
    player.play.assert_not_called()
    player.pause.assert_called_once()
    player.seek.assert_called_once_with(value=0, reference="absolute")


def test_speed_updates_player_speed(loaded_player_f):
    player, djplayer = loaded_player_f
    player.speed = 1.0
    djplayer.speed = 1.5
    assert player.speed == 1.5


def test_nudge_temp_changes_speed(loaded_player_f):
    player, djplayer = loaded_player_f
    djplayer.speed = 1.0
    djplayer.nudge_press(value=0.15)
    assert djplayer.speed == 1.0
    assert player.speed == 1.15
    djplayer.nudge_release()
    assert djplayer.speed == 1.0
    assert player.speed == 1.0


def test_nudge_relative_to_base(loaded_player_f):
    player, djplayer = loaded_player_f
    djplayer.speed = 2.0
    djplayer.nudge_press(value=0.15)
    assert player.speed == 2.30


@pytest.mark.parametrize("input", [-1, 1])
def test_raises_outside_range(input, loaded_player_f):
    player, djplayer = loaded_player_f
    djplayer.speed = 2.0
    with pytest.raises(ValueError):
        djplayer.nudge_press(value=input)


def test_nudge_updated_if_speed_updated(loaded_player_f):
    player, djplayer = loaded_player_f
    djplayer.speed = 1.0
    djplayer.nudge_press(value=0.15)
    assert djplayer.speed == 1.0
    assert player.speed == 1.15
    djplayer.speed = 2.0
    assert djplayer.speed == 2.0
    assert player.speed == 2.30
    djplayer.nudge_release()
    assert djplayer.speed == 2.0
    assert player.speed == 2.0


def test_jog_does_relative_seek(loaded_player_f):
    player, djplayer = loaded_player_f
    djplayer.jog(20)
    player.seek.assert_called_once_with(value=20, reference="relative")


def test_volume_updates_player_volume(loaded_player_f):
    player, djplayer = loaded_player_f
    player.volume = 100
    djplayer.volume = 50
    assert player.volume == 50
