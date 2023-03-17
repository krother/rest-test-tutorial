import json
import os

import pytest

from song_finder.entity import SongRequest, SongResponse


@pytest.fixture
def song_request():
    return SongRequest(name="3")


@pytest.fixture
def song_response():
    return SongResponse(
        song_id=3, artist="Stevie Wonder", title="You are the sunshine of my life"
    )


@pytest.fixture
def songs():
    path = os.path.split(__file__)[0]
    return json.load(open(os.path.join(path, 'songs.json')))
