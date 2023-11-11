"""
Boundaries: 

Toplevel functions without the API server.
Isolate the business logic from the API mechanics.
"""
from song_finder.entity import SongRequest, SongResponse
from song_finder.controller import execute_query, SongFinderError


def find_song(query: SongRequest) -> SongResponse:
    """Finds a song with the given query parameters"""
    return execute_query(query)
