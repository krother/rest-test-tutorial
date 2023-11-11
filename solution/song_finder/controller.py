"""
Controller:

Organize processes required to execute an endpoint.
"""
import re

from song_finder.entity import SongRequest, SongResponse
from song_finder.repository import SongRepository


class SongFinderError(Exception): pass


def execute_query(query: SongRequest) -> SongResponse:
    """Finds a song with the given query parameters"""
    repo = SongRepository()
    if re.match(r"^\d+$", query.name):
        result = repo.find_song_by_id(int(query.name))
    else:
        result = repo.find_song_by_name(query.name)
    if result:
        return SongResponse(**result)
 
    raise SongFinderError(f"song {query.name} not found!")
