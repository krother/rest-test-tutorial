
from song_finder.entity import SongRequest, SongResponse
from song_finder.controller import execute_query



def find_song(query: SongRequest) -> SongResponse:
    """Finds a song with the given query parameters"""
    result = execute_query(query)
    if result:
        return result
 
    raise IndexError(f"song {query} not found!")
