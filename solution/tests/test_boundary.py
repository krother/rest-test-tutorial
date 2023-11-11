
import pytest

from song_finder.boundary import find_song, SongFinderError
from song_finder.entity import SongRequest, SongResponse


def test_find_song_boundary():
    request = SongRequest(name=3)
    song = find_song(request)
    assert type(song) == SongResponse
    assert song.song_id == 3
    assert song.artist == "Stevie Wonder"
    assert song.title.startswith("You are the sunshine")


def test_find_song(song_request, song_response):
    assert find_song(song_request) == song_response


def test_find_song_error():
    with pytest.raises(SongFinderError):
        request = SongRequest(name="999")
        find_song(request)


def test_mock_db(song_request):
    song = find_song(song_request)
    assert song.song_id == 3
