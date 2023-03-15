
import pytest

from song_finder.entity import SongRequest, SongResponse


@pytest.fixture
def song_request():
    return SongRequest(name="1")
