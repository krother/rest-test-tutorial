import pytest

from song_finder.boundary import find_song
from song_finder.entity import SongRequest, SongResponse
from song_finder.repository import get_client


@pytest.fixture(autouse=True)
def songdb(songs):
    client = get_client()
    coll = client["songdb"].songs
    coll.insert_many(songs)
    yield coll
    coll.delete_many({})


def test_find_song(song_response):
    request = SongRequest(name="3")
    assert find_song(request) == song_response


def test_find_song_by_name(song_response):
    request = SongRequest(name="You are the sunshine of my life")
    assert find_song(request) == song_response


def test_find_song_error():
    with pytest.raises(IndexError):
        request = SongRequest(name="999")
        response = find_song(request)
