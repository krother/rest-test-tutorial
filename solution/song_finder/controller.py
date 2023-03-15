
from song_finder.entity import SongRequest, SongResponse
from song_finder.repository import SongRepository

import json
import os


def execute_query(query: SongRequest) -> SongResponse:
    """Finds a song with the given query parameters"""
    repo = SongRepository()
    if query.name[0] in "1234567890":
        result = repo.find_song_by_id(int(query.name))
    else:
        result = repo.find_song_by_name(query.name)
    return SongResponse(**result)
