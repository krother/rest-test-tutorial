from song_finder.entity import SongResponse

from mongomock import MongoClient
from unittest.mock import patch
from pytest_mock import MockerFixture


def test_song_request():
    assert SongResponse(
        song_id=7, title="Stefania", artist="Kalush Orchestra", year=2022
    )


def test_mock_db(song_request, songs, song_response, mocker: MockerFixture):
    client = MongoClient()
    client["songdb"].songs.insert_many(songs)

    mocker.patch("song_finder.repository.get_client", return_value=client)
    song = find_song(song_request)
    assert song == song_response
