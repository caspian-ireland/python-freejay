import pytest


@pytest.fixture
def mock_mp4(tmp_path):
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "test.mp4"
    p.write_text("test")
    return p
