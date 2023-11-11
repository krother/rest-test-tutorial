import json
import os

from mongomock import MongoClient
import pytest
from pytest_mock import MockerFixture

from song_finder.entity import SongRequest, SongResponse


@pytest.fixture
def song_request():
    return SongRequest(name="3")


@pytest.fixture
def song_response():
    return SongResponse(
        song_id=3,
        title="You are the sunshine of my life",
        artist="Stevie Wonder", 
    )

def read_songs():
    """some songs for testing"""
    path = os.path.split(__file__)[0]
    return json.load(open(os.path.join(path, 'songs.json')))


@pytest.fixture(autouse=True)
def db_with_songs(mocker:MockerFixture):
    client = MongoClient()
    mocker.patch("song_finder.repository.get_client", return_value=client)

    db = client.songdb
    db.songs.insert_many(read_songs())
    yield db
    db.songs.delete_many({})
